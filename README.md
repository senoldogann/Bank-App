# Banka CLI (Akbank Direkt - Örnek Uygulama)

Basit ve profesyonel bir banka CLI uygulaması. Müşteri kaydı, giriş, para yatırma/çekme ve bakiye görüntüleme içerir. Veriler `data.json` dosyasında saklanır.

## Gereksinimler
- Python 3.8+

## Çalıştırma
```bash
python deneme.py
```
İlk çalıştırmada `data.json` otomatik oluşturulur.

## Özellikler
- Müşteri oluşturma (TC + Müşteri ID)
- Güvenli giriş (TC + Müşteri ID eşleşmesi)
- Para yatırma / para çekme
- Bakiye görüntüleme
- JSON ile kalıcı veri

## Dosyalar
- `deneme.py`: Uygulama ve iş mantığı
- `data.json`: Müşteri verileri (otomatik)

## Notlar
- Tutarlar pozitif tam sayı olmalıdır.
- Yetersiz bakiye durumunda işlem engellenir.