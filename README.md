# Türkçe Makalelerin Zemberek-NLP ve Makine Öğrenmesi ile Sınıflandırılması

Bu proje, Türkçe makalelerin içeriklerine göre otomatik olarak ilgili bilim dallarına veya kategorilere sınıflandırılmasını amaçlayan bir Doğal Dil İşleme (NLP) ve Makine Öğrenmesi çalışmasıdır.

Türkçe metinler **Zemberek-NLP** kütüphanesi ile morfolojik analizden geçirilmiş, kelimelerin gerçek kökleri bulunmuş ve ardından TF-IDF vektörleştirme ile **Lojistik Regresyon** modeli eğitilmiştir.

---

## Proje Kapsamı ve İşleyiş Adımları

1. **Veri Ön İşleme:**
   * Akademik makale metinlerindeki noktalama işaretleri, sayılar, özel karakterler ve anlamsız bağlaçların (stopwords) temizlenmesi.
   * Zemberek `TurkishSpellChecker` modülü kullanılarak olası yazım hatalarının normalize edilmesi.

2. **Morfolojik Analiz ve Kök Bulma (Lemmatization):**
   * `JPype1` aracılığıyla Python ortamından Java tabanlı Zemberek kütüphanesine erişim sağlanması.
   * `TurkishMorphology` kullanılarak kelimelerin çekim ve yapım eklerinden arındırılarak sözlük köklerine (lemma) indirgenmesi.

3. **Özellik Çıkarımı ve Modelleme:**
   * Köklerine ayrılmış akademik metinlerin `TF-IDF` (Term Frequency-Inverse Document Frequency) yöntemiyle sayısal matrise dönüştürülmesi.
   * Oluşturulan öznitelik matrisi üzerinde Lojistik Regresyon sınıflandırıcısının eğitilmesi ve test verisi üzerinde doğruluk (Accuracy), kesinlik (Precision), duyarlılık (Recall) ve F1-skoru metrikleriyle değerlendirilmesi.

---

## Kullanılan Teknolojiler

* **Programlama Dili:** Python 3.10
* **Doğal Dil İşleme:** Zemberek-NLP (`zemberek-full.jar`)
* **Python - Java Entegrasyonu:** JPype1 (Java JDK 17)
* **Veri Analizi ve Modelleme:** Scikit-learn, Pandas, NumPy
* **Geliştirme Ortamı:** Jupyter Notebook

---

### Adımlar

1. Depoyu bilgisayarınıza klonlayın:
   ```bash
   git clone [https://github.com/zeyneperdogdu/turkish-document-classification.git](https://github.com/zeyneperdogdu/turkish-document-classification.git)
   cd turkish-document-classification
