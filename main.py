from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock

Window.fullscreen = True

class UrunButton(Button):
    def __init__(self, **kwargs):
        self.is_yarim = kwargs.pop('is_yarim', False)
        self.is_geri = kwargs.pop('is_geri', False)
        super().__init__(**kwargs)
        
        self.background_color = (0, 0, 0, 0)
        
        if self.is_yarim:
            self.color = (1, 1, 1, 1)
            self.font_size = 28
        elif self.is_geri:
            self.color = (1, 1, 1, 1)
            self.font_size = 45  
        else:
            self.color = (0, 0, 0, 1)
            self.font_size = 34
            
        self.bold = True
        self.halign = "center"
        self.valign = "middle"

        with self.canvas.before:
            if self.is_yarim:
                Color(0.05, 0.15, 0.3, 1)  
                self.kart = RoundedRectangle(radius=[25], pos=self.pos, size=self.size)
            elif self.is_geri:
                Color(0.2, 0.2, 0.2, 1)    
                self.kart = Ellipse(pos=self.pos, size=self.size)
            else:
                Color(1, 1, 1, 1)          
                self.kart = RoundedRectangle(radius=[25], pos=self.pos, size=self.size)
            
            if not self.is_geri:
                if self.is_yarim:
                    Color(0.2, 0.5, 0.9, 1)
                else:
                    Color(0.8, 0, 0, 1)
                self.icon = Ellipse(pos=(self.x + 15, self.y + 15), size=(25, 25))

        self.bind(pos=self.guncelle, size=self.guncelle)

    def guncelle(self, *args):
        self.kart.pos = self.pos
        self.kart.size = self.size
        if not self.is_geri:
            self.icon.pos = (self.x + 15, self.y + self.height - 40)

    def on_press(self):
        Animation.cancel_all(self)
        Animation(size=(self.width * 0.94, self.height * 0.94), duration=0.05).start(self)
        Clock.schedule_once(self.geri_animasyon, 0.1)

    def geri_animasyon(self, dt):
        Animation(size=(self.width / 0.94, self.height / 0.94), duration=0.08).start(self)


class PosApp(App):
    def build(self):
        self.toplam = 0
        self.adet = {}
        self.butonlar = {}
        self.islem_gecmisi = []

        ana = BoxLayout(orientation="vertical", padding=20, spacing=15)

        with ana.canvas.before:
            Color(0.85, 0, 0, 1)
            self.arka = RoundedRectangle(pos=ana.pos, size=ana.size)
        
        ana.bind(pos=self.arka_guncelle, size=self.arka_guncelle)

        # Başlık Bölümü
        baslik = Label(text="ETİBEYAZ", font_size=65, bold=True, color=(1, 1, 1, 1), size_hint_y=0.08)
        ana.add_widget(baslik)

        # Toplam Fiyat ve Minimal Geri Butonu Bölümü
        toplam_ve_geri_layout = BoxLayout(orientation="horizontal", spacing=15, size_hint_y=0.12)
        
        self.toplam_label = Label(text="TOPLAM\n0 TL", font_size=60, bold=True, color=(1, 1, 1, 1), size_hint_x=0.75)
        toplam_ve_geri_layout.add_widget(self.toplam_label)
        
        geri_btn = UrunButton(text="<-", is_geri=True, size_hint_x=0.18)
        geri_btn.bind(on_press=self.son_islemi_geri_al)
        toplam_ve_geri_layout.add_widget(geri_btn)
        
        ana.add_widget(toplam_ve_geri_layout)

        # 1. YARIM BUTONLAR
        yarim_grid = GridLayout(cols=2, spacing=18, size_hint_y=0.07)
        yarim_urunler = [("Yarım Sebzeli\n70 TL", 70), ("Yarım Kaşarlı\n85 TL", 85)]
        
        for isim, fiyat in yarim_urunler:
            self.adet[isim] = 0
            btn = UrunButton(text=f"{isim}\n0", is_yarim=True)
            btn.bind(on_press=lambda x, i=isim, f=fiyat, b=btn: self.ekle(i, f, b))
            yarim_grid.add_widget(btn)
            self.butonlar[isim] = btn
        ana.add_widget(yarim_grid)

        # 2. ANA ÜRÜNLER
        grid = GridLayout(cols=2, spacing=18, size_hint_y=0.48)
        urunler = [
            ("Sebzeli Döner\n135 TL", 135), ("Kaşarlı Döner\n170 TL", 170),
            ("Porsiyon\n240 TL", 240), ("Kızartma Dürüm\n100 TL", 100),
            ("Coca-Cola\n70 TL", 70), ("Cola Max Fly\n50 TL", 50),
            ("Açık Ayran\n25 TL", 25), ("Kapalı Ayran\n30 TL", 30)
        ]
        
        for isim, fiyat in urunler:
            self.adet[isim] = 0
            btn = UrunButton(text=f"{isim}\n0")
            btn.bind(on_press=lambda x, i=isim, f=fiyat, b=btn: self.ekle(i, f, b))
            grid.add_widget(btn)
            self.butonlar[isim] = btn
        ana.add_widget(grid)

        # 3. ŞALGAM VE SU GRID YAPISI
        alt_grid = GridLayout(cols=2, spacing=18, size_hint_y=0.1)
        alt_urunler = [
            ("Şalgam\n35 TL", 35),
            ("Su\n15 TL", 15)
        ]
        
        for isim, fiyat in alt_urunler:
            self.adet[isim] = 0
            btn = UrunButton(text=f"{isim}\n0")
            btn.bind(on_press=lambda x, i=isim, f=fiyat, b=btn: self.ekle(i, f, b))
            alt_grid.add_widget(btn)
            self.butonlar[isim] = btn
        ana.add_widget(alt_grid)

        # Siparişi Temizle Butonu
        temiz = UrunButton(text="SİPARİŞİ TEMİZLE", size_hint_y=0.1)
        temiz.bind(on_press=self.temizle)
        ana.add_widget(temiz)

        return ana

    def ekle(self, isim, fiyat, btn):
        self.toplam += fiyat
        self.adet[isim] += 1
        self.islem_gecmisi.append((isim, fiyat))
        btn.text = f"{isim}\n{self.adet[isim]}"
        self.toplam_label.text = f"TOPLAM\n{self.toplam} TL"
        self.toplam_label.color = (0, 1, 0, 1)
        Clock.schedule_once(self.normal, 0.3)

    def son_islemi_geri_al(self, x):
        if self.islem_gecmisi:
            son_islem = self.islem_gecmisi.pop()
            isim, fiyat = son_islem
            
            if self.adet[isim] > 0:
                self.toplam -= fiyat
                self.adet[isim] -= 1
                if isim in self.butonlar:
                    self.butonlar[isim].text = f"{isim}\n{self.adet[isim]}"
                
                self.toplam_label.text = f"TOPLAM\n{self.toplam} TL"
                self.toplam_label.color = (1, 0, 0, 1)
                Clock.schedule_once(self.normal, 0.3)

    def normal(self, dt):
        self.toplam_label.color = (1, 1, 1, 1)

    def temizle(self, x):
        self.toplam = 0
        self.islem_gecmisi.clear()
        for i in self.adet:
            self.adet[i] = 0
            if i in self.butonlar:
                self.butonlar[i].text = f"{i}\n0"
        self.toplam_label.text = "TOPLAM\n0 TL"

    def arka_guncelle(self, *args):
        self.arka.pos = self.root.pos
        self.arka.size = self.root.size


if __name__ == "__main__":
    PosApp().run()
