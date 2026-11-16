# 🇹🇷 Turkish Document Classification with Zemberek-NLP

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Java](https://img.shields.io/badge/Java-JDK%2017-orange?logo=openjdk&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-Zemberek-green)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E?logo=scikit-learn&logoColor=white)

Türkçe doğal dil işleme (NLP) alanında sondan eklemeli dil yapısının zorluklarını aşmak amacıyla **Zemberek-NLP** morfolojik analiz kütüphanesi ve **Makine Öğrenmesi** algoritmaları kullanılarak geliştirilmiş uçtan uca doküman sınıflandırma projesi.

---

## 🎯 Projenin Amacı ve Özgünlüğü

Türkçe, sondan eklemeli (agglutinative) yapısı nedeniyle standart kelime bazlı (bag-of-words) yaklaşımlarda yüksek boyutluluk ve anlam kaybı sorunlarına yol açmaktadır. Bu projede:
* Metinler ham halleriyle değil, **Zemberek** aracılığıyla morfolojik çözümleme ve kök bulma (lemmatization/stemming) işlemlerinden geçirilerek anlamlı köklerine indirgenmiştir.
* Yazım hataları (spell checking) ve gürültülü veriler temizlenerek TF-IDF matrisinin temsil gücü artırılmıştır.
* Farklı makine öğrenmesi sınıflandırıcıları (Logistic Regression vb.) kıyaslanarak Türkçe metinler üzerinde en yüksek genelleme başarısı hedeflenmiştir.

---

## 🛠️ Kullanılan Teknolojiler ve Mimari

* **Dil ve Çalışma Ortamı:** Python 3.10, Jupyter Notebook
* **Morfolojik Analiz & NLP:** Zemberek-NLP (`zemberek-full.jar`), JPype1 (Python-JVM Köprüsü, JDK 17)
* **Vektörleştirme:** TF-IDF (Term Frequency-Inverse Document Frequency)
* **Makine Öğrenmesi:** Scikit-learn (Logistic Regression, Model Değerlendirme Metrikleri)
* **Veri İşleme:** Pandas, NumPy

---

## ⚙️ Veri Ön İşleme Hattı (Pipeline)

1. **Veri Temizliği:** Noktalama işaretleri, sayılar, HTML etiketleri ve durak kelimelerinin (stopwords) temizlenmesi.
2. **Yazım Denetimi (Normalization):** Zemberek `TurkishSpellChecker` ile bozuk yazımlı kelimelerin düzeltilmesi.
3. **Morfolojik Analiz ve Kök Bulma:** `TurkishMorphology` kullanılarak kelimelerin gerçek köklerinin (lemma) çıkarılması.
4. **Özellik Çıkarımı:** Temizlenmiş kökler üzerinden TF-IDF ağırlıklandırması.
5. **Model Eğitimi ve Test:** Verinin eğitim/test olarak ayrılması ve sınıflandırma performansının ölçülmesi.

---

## 📊 Model Performansı

| Model | Vektörleştirme | Doğruluk (Accuracy) | F1-Skoru |
| :--- | :---: | :---: | :---: |
| **Logistic Regression** | TF-IDF + Zemberek Kök | **%XX.XX** | **0.XX** |

*(Not: Kendi notebook çıktındaki kesin yüzdeleri buraya ekleyebilirsin.)*

---

## 🚀 Kurulum ve Çalıştırma

### 1. Gereksinimler
* Sistemde **Java JDK 11 veya 17** kurulu olmalıdır.
* Python 3.10+ ortamı önerilir.

### 2. Repoyu Klonlayın
```bash
git clone [https://github.com/zeyneperdogdu/turkish-document-classification.git](https://github.com/zeyneperdogdu/turkish-document-classification.git)
cd turkish-document-classification
