from os import system as komut
class Banka():
    def __init__(self,isim):
        self.isim = isim


class Musteri():
    bakiye = 0
    def __init__(self,ad,soyad,tc,id):
        self.ad = ad
        self.soyad = soyad
        self.tc = tc
        self.id = id



class MusteriBilgileri():
    bilgiler = []




def main():
    banka = Banka("Akbank Direkt")
    while True:
        komut("cls")


        print("""
            
            [1] Müşteri Ol
            [2] Hesabım Var
        """)
        secim = input("Seçiminizi Yazınız: ")
        if  secim == "1":
            Musteri.ad = input("Lütfen Adınızı Giriniz: ")
            Musteri.soyad = input("Lütfen Soyadınızı Giriniz: ")
            Musteri.tc = input("Tc Kimlik Numaranızı Giriniz: ")
            Musteri.id = input("İd Numaranızı Giriniz : ")

            if Musteri.ad and Musteri.soyad and Musteri.tc and Musteri.id:
                MusteriBilgileri.bilgiler.append([Musteri.ad,Musteri.soyad,Musteri.tc,Musteri.id])
                print(MusteriBilgileri.bilgiler)
                input("Ana Menüye dönmek için lütfen 'ENTER'e basınız!")
        elif secim == "2":
            tc = input("Tc Kimlik Numaranızı Giriniz: ")
            id = input("İd Numaranızı Giriniz : ")

            while True:
                komut("cls")
                if tc == Musteri.tc and id == Musteri.id:
                    print("Hoşgeldiniz {} {}".format(Musteri.ad,Musteri.soyad))
                    print("""
                        [A] Para Yatırma
                        [B] Para Çekme
                        [C] Hesap Bilgileri
                        [Q] Çıkış
                    """)

                    secim = input("Lütfen yapmak istediğiniz işlemi yazınız: ")

                    if secim == "A" or secim == " A":
                        miktar = int(input("Yatırmak istediğiniz tutarı giriniz: "))
                        Musteri.bakiye += miktar
                        print("Hesabınıza {} TL yatırılmıştır.".format(miktar))
                        input("Ana Menüye Dönmek İçin Lütfen 'ENTER'e basınız!")

                    elif secim == "B" or secim == " B":
                        miktar = int(input("Çekmek istediğiniz tutarı giriniz: "))
                        if miktar >= Musteri.bakiye:
                            print("Yetersiz Bakiye !")
                            input("Ana Menüye Dönmek İçin Lütfen 'ENTER'e basınız!")

                        elif miktar <= 0:
                            print("Lütfen Doğru bir değer giriniz 0 dan küçük olamaz çekeceğiniz para")
                            input("Ana Menüye Dönmek İçin Lütfen 'ENTER'e basınız!")

                        else:
                            Musteri.bakiye -= miktar
                            print("Hesabınızadan {} TL çekilmiştir. Kalan Bakiyeniz: {}".format(miktar, Musteri.bakiye))
                            input("Ana Menüye Dönmek İçin Lütfen 'ENTER'e basınız!")

                    elif secim == "C" or secim == " C":
                        print("Adınız: {}".format(Musteri.ad))
                        print("Soyadınız: {}".format(Musteri.soyad))
                        print("Tc No: {}".format(Musteri.tc))
                        print("İd No: {}".format(Musteri.id))
                        print("Hesabınızdaki Güncel Bakiye: {}".format(Musteri.bakiye))
                        input("Ana Menüye Dönmek İçin Lütfen 'ENTER'e basınız!")


                    elif secim == "Q" or secim == "q":
                        print("Çıkış yapılıyor...")
                        exit()

                    else:
                        print("Böyle bir işlem bulunmamaktadir!")
                        input("Ana Menüye Dönmek İçin Lütfen 'ENTER'e basınız!")



                else:
                    print("Girdiginiz Bilgiler Hatalı!")
                    input("Ana Menüye Dönmek İçin Lütfen 'ENTER'e basınız!")




if __name__ == "__main__":
    main()




