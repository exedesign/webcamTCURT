# OBS Browser Source Kullanımı (Kolay Yöntem)

## 🎥 Virtual Camera Yerine Browser Source Kullanın

Virtual camera driver sorunu varsa, **OBS Browser Source** daha kolay ve stabil bir çözüm.

---

## 🚀 Adım Adım Kurulum

### 1. FaceFusion Başlatın
```
http://127.0.0.1:7860
Browser'da webcam'i başlatın
```

### 2. OBS'de Browser Source Ekleyin
```
OBS Studio'da:

1. Sources (Kaynaklar) → + (Ekle)
2. Browser (Tarayıcı)
3. İsim: "FaceFusion Webcam"
4. OK

Ayarlar:
- URL: http://127.0.0.1:7860
- Width: 640
- Height: 480
- FPS: 30
- ✓ Shutdown source when not visible
- ✓ Refresh browser when scene becomes active

5. OK
```

### 3. Tam Ekran CSS (Opsiyonel)
```css
Custom CSS:
body { margin: 0px auto; overflow: hidden; }
```

---

## 📺 Ekran Görüntüsüne Göre Sorun

Sizin ekran görüntünüzde:
- "Sanal Kamera" ayarları açık ✓
- "Çıkış Seçimi: FAceFusion" seçili ✓
- Ancak görüntü gelmiyor ✗

**Sorun**: OBS Virtual Camera driver çalışmıyor

**Çözüm**: Browser Source kullanın (yukarıdaki adımlar)

---

## 🛠️ Alternatif: OBS Virtual Cam Plugin

Eğer gerçekten Virtual Camera istiyorsanız:

```
1. OBS Virtual Camera Plugin indir:
   https://obsproject.com/forum/resources/obs-virtualcam.539/

2. Kur ve OBS'i yeniden başlat

3. Tools → VirtualCam → Start

4. FaceFusion'ı yeniden başlat
```

---

## ✅ En Kolay Yöntem: Browser Source

**Artıları:**
- ✅ Kolay kurulum (5 dakika)
- ✅ Driver gerektirmez
- ✅ Daha stabil
- ✅ Düşük latency
- ✅ Doğrudan FaceFusion browser output

**Eksileri:**
- ⚠️ Sadece OBS'de kullanılabilir (Zoom/Teams'de değil)

---

## 🎬 Sonuç

**Browser Source ile:**
```
FaceFusion Webcam → Browser (http://127.0.0.1:7860)
                    ↓
                OBS Browser Source
                    ↓
            Canlı Yayın / Kayıt
```

**Bu yöntem %100 çalışır!**
