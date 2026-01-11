"""
TensorRT Readiness Check - Sürücü güncellemesi sonrası kontrol
"""
import sys
import subprocess

def check_nvidia_driver():
    """NVIDIA sürücü versiyonunu kontrol et"""
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=driver_version', '--format=csv,noheader'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            version_num = float('.'.join(version.split('.')[:2]))
            print(f"✓ NVIDIA Driver: {version}")
            if version_num >= 580.0:
                print(f"  └─ TensorRT 10.14 için uygun (≥580.0)")
                return True
            else:
                print(f"  └─ TensorRT için yetersiz (gerekli: ≥580.0)")
                return False
        else:
            print("✗ nvidia-smi çalıştırılamadı")
            return False
    except Exception as e:
        print(f"✗ Driver kontrolü başarısız: {e}")
        return False

def check_tensorrt_libs():
    """TensorRT kütüphanelerini kontrol et"""
    try:
        import os
        tensorrt_path = r"C:\Users\FE\AppData\Local\Programs\Python\Python311\Lib\site-packages\tensorrt_libs"
        
        if os.path.exists(tensorrt_path):
            dlls = [f for f in os.listdir(tensorrt_path) if f.endswith('.dll')]
            print(f"\n✓ TensorRT DLLs: {len(dlls)} dosya")
            
            # Ana DLL'leri kontrol et
            required_dlls = ['nvinfer_10.dll', 'nvinfer_plugin_10.dll', 'nvonnxparser_10.dll']
            all_found = True
            for dll in required_dlls:
                found = dll in dlls
                symbol = "✓" if found else "✗"
                print(f"  {symbol} {dll}")
                if not found:
                    all_found = False
            return all_found
        else:
            print("✗ TensorRT libs dizini bulunamadı")
            return False
    except Exception as e:
        print(f"✗ TensorRT kontrol hatası: {e}")
        return False

def check_cuda_libs():
    """CUDA kütüphanelerini kontrol et"""
    try:
        import os
        cuda_base = r"C:\Users\FE\AppData\Local\Programs\Python\Python311\Lib\site-packages\nvidia"
        
        required_modules = ['cublas', 'cuda_runtime', 'cudnn']
        print(f"\n✓ CUDA Libraries:")
        all_found = True
        
        for module in required_modules:
            module_path = os.path.join(cuda_base, module, 'bin')
            if os.path.exists(module_path):
                dll_count = len([f for f in os.listdir(module_path) if f.endswith('.dll')])
                print(f"  ✓ {module}: {dll_count} DLLs")
            else:
                print(f"  ✗ {module}: eksik")
                all_found = False
        
        return all_found
    except Exception as e:
        print(f"✗ CUDA kontrol hatası: {e}")
        return False

def check_onnxruntime():
    """ONNX Runtime ve TensorRT provider'ı kontrol et"""
    try:
        import onnxruntime as ort
        version = ort.__version__
        providers = ort.get_available_providers()
        
        print(f"\n✓ onnxruntime-gpu: {version}")
        
        has_tensorrt = 'TensorrtExecutionProvider' in providers
        has_cuda = 'CUDAExecutionProvider' in providers
        
        if has_tensorrt:
            print(f"  ✓ TensorrtExecutionProvider")
        else:
            print(f"  ✗ TensorrtExecutionProvider (eksik)")
        
        if has_cuda:
            print(f"  ✓ CUDAExecutionProvider")
        else:
            print(f"  ✗ CUDAExecutionProvider (eksik)")
        
        return has_tensorrt and has_cuda
    except ImportError:
        print("✗ onnxruntime yüklü değil")
        return False
    except Exception as e:
        print(f"✗ ONNX Runtime kontrol hatası: {e}")
        return False

def test_tensorrt_session():
    """TensorRT ile session oluşturmayı test et"""
    try:
        import onnxruntime as ort
        import os
        
        model_path = r".assets\models\inswapper_128_fp16.onnx"
        if not os.path.exists(model_path):
            print(f"\n⚠ Model bulunamadı: {model_path}")
            return False
        
        print(f"\n🔧 TensorRT Session Test...")
        print(f"   (CUDA init error 35 alırsan driver güncelleme gerekli)")
        
        providers = [
            ('TensorrtExecutionProvider', {
                'device_id': 0,
                'trt_max_workspace_size': 4294967296,  # 4GB
                'trt_fp16_enable': True,
            }),
            ('CUDAExecutionProvider', {'device_id': 0})
        ]
        
        sess = ort.InferenceSession(model_path, providers=providers)
        actual_providers = sess.get_providers()
        
        if 'TensorrtExecutionProvider' in actual_providers:
            print(f"  ✓ TensorRT session başarılı!")
            print(f"  └─ Active providers: {actual_providers}")
            return True
        else:
            print(f"  ✗ TensorRT aktif değil")
            print(f"  └─ Fallback: {actual_providers}")
            return False
            
    except Exception as e:
        error_msg = str(e)
        if "error: 35" in error_msg or "CUDA initialization failure" in error_msg:
            print(f"  ✗ CUDA init error 35 - Driver güncelleme gerekli!")
            return False
        else:
            print(f"  ✗ Test hatası: {e}")
            return False

def main():
    print("="*60)
    print("  TENSORRT READINESS CHECK")
    print("="*60)
    
    checks = {
        "NVIDIA Driver": check_nvidia_driver(),
        "TensorRT DLLs": check_tensorrt_libs(),
        "CUDA Libraries": check_cuda_libs(),
        "ONNX Runtime": check_onnxruntime(),
        "TensorRT Session": test_tensorrt_session()
    }
    
    print("\n" + "="*60)
    print("  SONUÇ")
    print("="*60)
    
    all_passed = all(checks.values())
    
    for check, passed in checks.items():
        status = "✓ TAMAM" if passed else "✗ HATA"
        print(f"{status:10} | {check}")
    
    print("="*60)
    
    if all_passed:
        print("\n🎉 SİSTEM HAZIR! TensorRT çalışmaya hazır.")
        print("   start_cuda.bat ile başlatabilirsiniz.")
        return 0
    else:
        print("\n⚠️  SORUN VAR:")
        if not checks["NVIDIA Driver"]:
            print("   → NVIDIA driver'ı 580+ sürümüne güncelleyin")
            print("   → https://www.nvidia.com/Download/index.aspx")
        if not checks["TensorRT Session"]:
            print("   → Driver güncellemesinden sonra sistemi yeniden başlatın")
        return 1

if __name__ == "__main__":
    sys.exit(main())
