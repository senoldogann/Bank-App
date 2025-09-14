from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Optional


# Basit log yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("banka")


DATA_FILE = Path(__file__).with_name("data.json")


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pause(msg: str = "Ana menüye dönmek için ENTER'a basınız...") -> None:
    try:
        input(msg)
    except EOFError:
        pass


def prompt_non_empty(prompt_text: str) -> str:
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Boş bırakılamaz. Lütfen tekrar deneyin.")


def prompt_amount(prompt_text: str) -> int:
    while True:
        raw = input(prompt_text).strip().replace(" ", "")
        if not raw.isdigit():
            print("Lütfen geçerli bir tam sayı giriniz.")
            continue
        amount = int(raw)
        if amount <= 0:
            print("Tutar 0'dan büyük olmalıdır.")
            continue
        return amount


@dataclass
class Musteri:
    ad: str
    soyad: str
    tc: str
    musteri_id: str
    bakiye: int = 0


class Banka:
    def __init__(self, isim: str) -> None:
        self.isim = isim
        self.musteriler: Dict[str, Musteri] = {}

    # Veri işlemleri
    def kaydet(self) -> None:
        data = {tc: asdict(m) for tc, m in self.musteriler.items()}
        DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.debug("Veriler kaydedildi: %s", DATA_FILE)

    def yukle(self) -> None:
        if DATA_FILE.exists():
            try:
                raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
                self.musteriler = {tc: Musteri(**info) for tc, info in raw.items()}
                logger.info("%d müşteri yüklendi.", len(self.musteriler))
            except Exception as exc:
                logger.exception("Veri yüklenirken hata: %s", exc)
                self.musteriler = {}

    # İş mantığı
    def musteri_ekle(self, ad: str, soyad: str, tc: str, musteri_id: str) -> Musteri:
        if tc in self.musteriler:
            raise ValueError("Bu TC ile kayıt zaten var.")
        yeni = Musteri(ad=ad, soyad=soyad, tc=tc, musteri_id=musteri_id, bakiye=0)
        self.musteriler[tc] = yeni
        self.kaydet()
        logger.info("Yeni müşteri eklendi: %s %s (%s)", ad, soyad, tc)
        return yeni

    def musteri_bul(self, tc: str, musteri_id: str) -> Optional[Musteri]:
        musteri = self.musteriler.get(tc)
        if musteri and musteri.musteri_id == musteri_id:
            return musteri
        return None

    def para_yatir(self, musteri: Musteri, miktar: int) -> None:
        musteri.bakiye += miktar
        self.kaydet()
        logger.info("%s için %s TL yatırıldı. Yeni bakiye: %s", musteri.tc, miktar, musteri.bakiye)

    def para_cek(self, musteri: Musteri, miktar: int) -> None:
        if miktar > musteri.bakiye:
            raise ValueError("Yetersiz bakiye.")
        musteri.bakiye -= miktar
        self.kaydet()
        logger.info("%s için %s TL çekildi. Yeni bakiye: %s", musteri.tc, miktar, musteri.bakiye)


def menu_ana(banka: Banka) -> None:
    while True:
        clear_screen()
        print(f"\n{banka.isim} - Ana Menü\n")
        print("[1] Müşteri Ol")
        print("[2] Hesabım Var")
        print("[Q] Çıkış")
        secim = input("Seçiminizi yazınız: ").strip().lower()

        if secim == "1":
            ad = prompt_non_empty("Adınız: ")
            soyad = prompt_non_empty("Soyadınız: ")
            tc = prompt_non_empty("TC Kimlik Numaranız: ")
            musteri_id = prompt_non_empty("Müşteri ID (şifre gibi): ")
            try:
                musteri = banka.musteri_ekle(ad, soyad, tc, musteri_id)
                print(f"Hoşgeldiniz {musteri.ad} {musteri.soyad}. Kayıt tamamlandı.")
            except ValueError as exc:
                print(str(exc))
            pause()

        elif secim == "2":
            tc = prompt_non_empty("TC Kimlik Numaranız: ")
            musteri_id = prompt_non_empty("Müşteri ID'niz: ")
            musteri = banka.musteri_bul(tc, musteri_id)
            if not musteri:
                print("Bilgiler hatalı veya hesap bulunamadı.")
                pause()
                continue
            menu_hesap(banka, musteri)

        elif secim == "q":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim.")
            pause()


def menu_hesap(banka: Banka, musteri: Musteri) -> None:
    while True:
        clear_screen()
        print(f"Hoşgeldiniz {musteri.ad} {musteri.soyad}\n")
        print("[A] Para Yatırma")
        print("[B] Para Çekme")
        print("[C] Hesap Bilgileri")
        print("[R] Çıkış Yap (Hesaptan)")
        print("[Q] Programdan Çık")
        secim = input("İşleminiz: ").strip().lower()

        if secim == "a":
            miktar = prompt_amount("Yatırmak istediğiniz tutar: ")
            banka.para_yatir(musteri, miktar)
            print(f"Hesabınıza {miktar} TL yatırıldı.")
            pause()

        elif secim == "b":
            miktar = prompt_amount("Çekmek istediğiniz tutar: ")
            try:
                banka.para_cek(musteri, miktar)
                print(f"Hesabınızdan {miktar} TL çekildi. Kalan bakiye: {musteri.bakiye}")
            except ValueError as exc:
                print(str(exc))
            pause()

        elif secim == "c":
            print(f"Ad: {musteri.ad}")
            print(f"Soyad: {musteri.soyad}")
            print(f"TC: {musteri.tc}")
            print(f"Müşteri ID: {musteri.musteri_id}")
            print(f"Bakiye: {musteri.bakiye} TL")
            pause()

        elif secim == "r":
            print("Hesaptan çıkılıyor...")
            pause()
            break

        elif secim == "q":
            print("Çıkış yapılıyor...")
            raise SystemExit

        else:
            print("Geçersiz seçim.")
            pause()


def main() -> None:
    banka = Banka("Akbank Direkt")
    banka.yukle()
    try:
        menu_ana(banka)
    except SystemExit:
        pass


if __name__ == "__main__":
    main()




