#!/usr/bin/env python3
"""
DergiPark OAI-PMH Türkçe Makale Toplayıcı (429 Too Many Requests Korumalı)
"""

import csv
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

# --- KULLANICI AYARLARI ---
JOURNALS = {
    "bilgisayar_bilimleri": ["adyujsci", "adyumbd", "akufemubid", "apjes"],
    "saglik": ["marumj", "adiyamansaglik", "adj", "anadoluklin", "anatomy", "ataunihem"],
    "tarih": ["mulkiye", "iuoba", "ankuayd", "atauniad"],
    "spor": ["ataunibesyo"],
    "finans": ["marubsed", "marufacd", "muiibd", "akuiibfd"],
}

MIN_CHARS = 300       # Özet için asgari karakter sayısı
SLEEP_TIME = 2.5      # İstekler arası bekleme süresi artırıldı (Sunucuyu yormamak için)

BASE_URL = "https://dergipark.org.tr/api/public/oai/"
DATA_DIR = Path("data2")
OUTPUT_FILE = DATA_DIR / "dataset.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Turkce-Metin-Siniflandirma-Akademik)",
    "Accept": "application/xml,text/xml",
}
NS = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
}
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"

TR_WORDS = {"ve", "bir", "bu", "ile", "için", "olarak", "da", "de", "gibi", "ancak"}
EN_WORDS = {"the", "of", "and", "to", "in", "is", "for", "this", "study"}


def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&[a-z]+;", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def is_turkish(text, lang_attr=None):
    if lang_attr:
        l = lang_attr.lower()
        if l.startswith("tr"):
            return True
        if l.startswith("en"):
            return False
    words = re.findall(r"[a-zçğıöşüÇĞİÖŞÜ]+", text.lower())
    if not words:
        return False
    tr = sum(w in TR_WORDS for w in words)
    en = sum(w in EN_WORDS for w in words)
    return tr >= en


def fetch_xml_with_retry(url, params=None, retries=5):
    """429 veya sunucu hatalarında akıllıca bekleyip tekrar deneme mekanizması."""
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    
    for attempt in range(1, retries + 1):
        wait = SLEEP_TIME * (2 ** (attempt - 1)) # 2.5s, 5s, 10s, 20s... katlanarak artar
        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                return ET.fromstring(response.read())
        except urllib.error.HTTPError as e:
            # 429: Too Many Requests, 5xx: Sunucu hataları
            if e.code in (429, 500, 502, 503, 504):
                print(f"  [Uyarı] HTTP {e.code} alındı. {wait:.1f} saniye bekleyip tekrar deneniyor ({attempt}/{retries})...")
                time.sleep(wait)
                continue
            raise RuntimeError(f"HTTP {e.code}: {url}") from e
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            print(f"  [Ağ Hatası] {e}. {wait:.1f} saniye bekleniyor...")
            time.sleep(wait)
            continue
            
    raise RuntimeError(f"İstek başarısız oldu (Maksimum deneme aşıldı): {url}")


def load_existing_records():
    seen_keys = set()
    if OUTPUT_FILE.exists():
        try:
            with OUTPUT_FILE.open("r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    abstract = row.get("abstract", "")
                    if abstract:
                        key = re.sub(r"\W+", "", abstract.lower())
                        seen_keys.add(key)
        except Exception as e:
            print(f"Mevcut dosya okunurken uyarı: {e}")
    return seen_keys


def main():
    DATA_DIR.mkdir(exist_ok=True)
    
    seen_abstracts = load_existing_records()
    file_exists = OUTPUT_FILE.exists() and OUTPUT_FILE.stat().st_size > 0
    
    mode = "a" if file_exists else "w"
    with OUTPUT_FILE.open(mode, newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["category", "journal", "title", "abstract"])
            
    total_saved = 0
    total_skipped = 0

    for category, slugs in JOURNALS.items():
        print(f"\n--- Kategori: {category} ---")
        for slug in slugs:
            print(f"İşleniyor: {slug}...")
            url = f"{BASE_URL}{slug}/"
            params = {"verb": "ListRecords", "metadataPrefix": "oai_dc"}
            
            journal_count = 0
            try:
                while True:
                    root = fetch_xml_with_retry(url, params)
                    
                    for rec in root.findall("oai:ListRecords/oai:record", NS):
                        header = rec.find("oai:header", NS)
                        if header is None or header.get("status") == "deleted":
                            continue
                            
                        meta = rec.find("oai:metadata/oai_dc:dc", NS)
                        if meta is None:
                            continue
                            
                        titles = [(clean_text(t.text), t.get(XML_LANG)) for t in meta.findall("dc:title", NS)]
                        descs = [(clean_text(d.text), d.get(XML_LANG)) for d in meta.findall("dc:description", NS)]
                        
                        title_tr = next((t for t, l in titles if t and is_turkish(t, l)), "")
                        abstract_tr = next((d for d, l in descs if d and len(d) >= MIN_CHARS and is_turkish(d, l)), "")
                        
                        if title_tr and abstract_tr:
                            abstract_key = re.sub(r"\W+", "", abstract_tr.lower())
                            if abstract_key in seen_abstracts:
                                total_skipped += 1
                                continue
                            
                            seen_abstracts.add(abstract_key)
                            with OUTPUT_FILE.open("a", newline="", encoding="utf-8-sig") as f:
                                writer = csv.writer(f)
                                writer.writerow([category, slug, title_tr, abstract_tr])
                            
                            journal_count += 1
                            total_saved += 1

                    # Sayfalama token kontrolü
                    tok = root.find("oai:ListRecords/oai:resumptionToken", NS)
                    if tok is None or not (tok.text or "").strip():
                        break
                    params = {"verb": "ListRecords", "resumptionToken": tok.text.strip()}
                    time.sleep(SLEEP_TIME) # Her sayfa arası ek bekleme
                    
            except Exception as e:
                print(f"  [Hata] ({slug}): {e}")
                
            print(f"  -> {slug} dergisinden {journal_count} yeni makale eklendi.")
            time.sleep(SLEEP_TIME) # Dergiler arası ek bekleme
            
    print(f"\nİşlem Tamamlandı!")
    print(f"  - Eklenen yeni makale: {total_saved}")
    print(f"  - Atlanan kopya: {total_skipped}")
    print(f"  - Kayıt yeri: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()