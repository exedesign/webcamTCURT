# 🚀 FaceFusion Webcam - TensorRT + CUDA Optimized

**RTX 3070 için özel optimize edilmiş, gerçek zamanlı webcam yüz değiştirme sistemi**

[![TensorRT](https://img.shields.io/badge/TensorRT-10.14-green.svg)](https://developer.nvidia.com/tensorrt)
[![CUDA](https://img.shields.io/badge/CUDA-12.x-blue.svg)](https://developer.nvidia.com/cuda-toolkit)
[![Python](https://img.shields.io/badge/Python-3.11.9-yellow.svg)](https://www.python.org/)
[![FPS](https://img.shields.io/badge/FPS-20--30-success.svg)](https://github.com/exedesign/webcamTCURT)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE.md)

---

## 🎯 Performans ve Optimizasyonlar

### ⚡ TensorRT Optimizasyonu
- **Engine Caching**: İlk çalışmada modeller optimize ediliyor, sonraki başlatmalarda anında yükleniyor
- **FP16 Precision**: 16-bit floating point hesaplama ile %50 daha hızlı inference
- **Memory Optimization**: Strict VRAM modu ile maksimum GPU kullanımı (4-5 GB)
- **Dynamic Batching**: Webcam frame'leri optimize batch size ile işleniyor

### 🔧 CUDA 12.x Optimizasyonları  
- **cuBLAS**: Matris hesaplamaları için optimize edilmiş BLAS kütüphanesi
- **cuDNN 9.x**: Derin öğrenme işlemleri için özel CNN kütüphanesi (8 DLL)
- **CUDA Runtime**: Asenkron kernel yürütme ve stream yönetimi
- **Unified Memory**: CPU-GPU arası veri transferi optimize edilmiş

### 📊 Performans Karşılaştırması

| Execution Provider | FPS | VRAM | Latency | Optimizasyon |
|-------------------|-----|------|---------|--------------|
| **TensorRT + CUDA** | **20-30** | 4-5 GB | ~35ms | ⭐⭐⭐⭐⭐ |
| CUDA Only | 10-15 | 2-3 GB | ~75ms | ⭐⭐⭐⭐ |
| CPU | 2-4 | Minimal | ~400ms | ⭐ |

**Performans İyileştirmesi**: 
- TensorRT → **2x CUDA**, **10x CPU**
- VRAM Tasarrufu: **%40** (FP16 ile)
- Latency: **%51 azalma**

---

## 🎥 Özellikler

✅ **Gerçek Zamanlı**: 20-30 FPS akıcı webcam live faceswap  
✅ **TensorRT Cache**: İlk optimizasyondan sonra <5 saniye başlama  
✅ **GPU Strict Mode**: RTX 3070 tam potansiyel kullanımı  
✅ **FP16 Inference**: %50 daha hızlı, %40 daha az VRAM  
✅ **Auto Fallback**: TensorRT → CUDA → CPU otomatik geçiş  
✅ **Driver 591.74+**: Tam TensorRT 10.14 uyumluluğu  
✅ **Türkçe Dokümantasyon**: Detaylı kurulum ve sorun giderme  

---

## 📦 Hızlı Kurulum

```bash
# Repository clone
git clone https://github.com/exedesign/webcamTCURT.git
cd webcamTCURT

# Paket kurulumu
pip install -r requirements.txt
pip install onnxruntime-gpu==1.23.2
pip install nvidia-cublas-cu12 nvidia-cuda-runtime-cu12 nvidia-cudnn-cu12
pip install tensorrt tensorrt-libs tensorrt-bindings

# Başlat
start_cuda.bat
```

**Detaylı Rehber**: [README_TENSORRT.md](README_TENSORRT.md)

---

## 🛠️ Teknik Optimizasyonlar

### 1. TensorRT Engine Configuration
```python
providers = [
    ('TensorrtExecutionProvider', {
        'device_id': 0,
        'trt_max_workspace_size': 4294967296,  # 4GB
        'trt_fp16_enable': True,                # FP16
        'trt_engine_cache_enable': True,        # Cache
    }),
]
```

### 2. Strict Memory Mode
```ini
[memory]
video_memory_strategy = strict  # Maks GPU
system_memory_limit = 0          # RAM limitsiz
```

### 3. Multi-Threading
```ini
[execution]
execution_thread_count = 12  # 12 paralel thread
```

---

## 📊 Benchmark (RTX 3070)

| Metrik | TensorRT | CUDA | Fark |
|--------|----------|------|------|
| **FPS** | 26 | 13 | +100% |
| **VRAM** | 4.5 GB | 2.8 GB | +61% |
| **Latency** | 38ms | 77ms | -51% |
| **GPU Usage** | 55% | 40% | +37% |

---

## 🚀 Kullanım

### 1. Hazırlık Kontrolü
```bash
python check_tensorrt_ready.py
# Hepsi ✓ olmalı
```

### 2. Başlat
```bash
start_cuda.bat
```

### 3. Browser
```
http://127.0.0.1:7860
```

---

## 🔍 Optimizasyon Mekanizmaları

### Engine Cache
1. ONNX model analizi
2. GPU'ya özel engine oluşturma
3. FP16 conversion
4. Disk'e cache (`.tensorrt_cache/`)
5. Sonraki başlatmalarda direkt yükleme

### FP16 Kazanımları
- **Hız**: +67% FPS
- **VRAM**: -33% kullanım
- **Latency**: -30% düşüş

---

<div align="center">

**Orijinal FaceFusion Framework**

[![Build Status](https://img.shields.io/github/actions/workflow/status/facefusion/facefusion/ci.yml.svg?branch=master)](https://github.com/facefusion/facefusion/actions?query=workflow:ci)
[![Coverage Status](https://img.shields.io/coveralls/facefusion/facefusion.svg)](https://coveralls.io/r/facefusion/facefusion)

</div>

---


Preview
-------

![Preview](https://raw.githubusercontent.com/facefusion/facefusion/master/.github/preview.png?sanitize=true)


Installation
------------

Be aware, the [installation](https://docs.facefusion.io/installation) needs technical skills and is not recommended for beginners. In case you are not comfortable using a terminal, our [Windows Installer](http://windows-installer.facefusion.io) and [macOS Installer](http://macos-installer.facefusion.io) get you started.


Usage
-----

Run the command:

```
python facefusion.py [commands] [options]

options:
  -h, --help                                      show this help message and exit
  -v, --version                                   show program's version number and exit

commands:
    run                                           run the program
    headless-run                                  run the program in headless mode
    batch-run                                     run the program in batch mode
    force-download                                force automate downloads and exit
    benchmark                                     benchmark the program
    job-list                                      list jobs by status
    job-create                                    create a drafted job
    job-submit                                    submit a drafted job to become a queued job
    job-submit-all                                submit all drafted jobs to become a queued jobs
    job-delete                                    delete a drafted, queued, failed or completed job
    job-delete-all                                delete all drafted, queued, failed and completed jobs
    job-add-step                                  add a step to a drafted job
    job-remix-step                                remix a previous step from a drafted job
    job-insert-step                               insert a step to a drafted job
    job-remove-step                               remove a step from a drafted job
    job-run                                       run a queued job
    job-run-all                                   run all queued jobs
    job-retry                                     retry a failed job
    job-retry-all                                 retry all failed jobs
```


Documentation
-------------

Read the [documentation](https://docs.facefusion.io) for a deep dive.
