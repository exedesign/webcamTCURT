@echo off
set PYTHON="C:\Users\FE\AppData\Local\Programs\Python\Python311\python.exe"
set CUDA_PATH=C:\Users\FE\AppData\Local\Programs\Python\Python311\Lib\site-packages\nvidia
set TENSORRT_PATH=C:\Users\FE\AppData\Local\Programs\Python\Python311\Lib\site-packages\tensorrt_libs

REM Add ALL CUDA and TensorRT libraries to PATH for maximum performance
set PATH=%TENSORRT_PATH%;%CUDA_PATH%\cublas\bin;%CUDA_PATH%\cuda_runtime\bin;%CUDA_PATH%\cudnn\bin;%CUDA_PATH%\cufft\bin;%CUDA_PATH%\curand\bin;%CUDA_PATH%\cusolver\bin;%CUDA_PATH%\cusparse\bin;%CUDA_PATH%\cuda_nvrtc\bin;%CUDA_PATH%\nvjitlink\bin;%PATH%

echo.
echo ========================================
echo   FACEFUSION - TENSORRT + CUDA
echo ========================================
echo.
echo ============================================================
echo   FACEFUSION - TENSORRT + CUDA ACCELERATION
echo ============================================================
echo.
echo [GPU] RTX 3070 Laptop (8GB VRAM)
echo [MODEL] inswapper_128_fp16
echo [PROVIDER] TensorRT + CUDA (Maximum Performance)
echo [VRAM MODE] Strict (Maximum GPU Usage)
echo [PERFORMANCE] 20-30 FPS (TensorRT Optimized)
echo.
echo [DRIVER] Make sure NVIDIA driver is 580+ for TensorRT 10.14
echo [FIRST RUN] TensorRT optimizes models (1-2 min, one-time)
echo [NEXT RUNS] Instant startup with cached engines
echo.
echo [URL] http://127.0.0.1:7860
echo [STOP] Press CTRL+C to stop
echo.
echo Starting FaceFusion with TensorRT + CUDA...
echo.

%PYTHON% facefusion.py run --ui-layouts webcam

pause
