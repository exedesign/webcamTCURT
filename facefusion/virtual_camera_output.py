"""
Virtual Camera Output Module - OBS Virtual Camera'ya feed gönderme
"""
import cv2
import numpy as np
from typing import Optional
import pyvirtualcam
import threading
import queue
import time

class VirtualCameraOutput:
    """OBS Virtual Camera output manager"""
    
    def __init__(self, width: int = 640, height: int = 480, fps: int = 30):
        self.width = width
        self.height = height
        self.fps = fps
        self.camera: Optional[pyvirtualcam.Camera] = None
        self.frame_queue = queue.Queue(maxsize=2)
        self.running = False
        self.thread: Optional[threading.Thread] = None
        
    def start(self) -> bool:
        """Virtual camera'yı başlat"""
        try:
            # OBS Virtual Camera'yı aç
            self.camera = pyvirtualcam.Camera(
                width=self.width,
                height=self.height,
                fps=self.fps,
                fmt=pyvirtualcam.PixelFormat.RGB
            )
            
            print(f"✓ Virtual Camera başlatıldı: {self.camera.device}")
            print(f"  Çözünürlük: {self.width}x{self.height}")
            print(f"  FPS: {self.fps}")
            print(f"  OBS'de kaynak olarak kullanabilirsiniz!\n")
            
            # Frame gönderme thread'i başlat
            self.running = True
            self.thread = threading.Thread(target=self._send_frames, daemon=True)
            self.thread.start()
            
            return True
            
        except Exception as e:
            print(f"✗ Virtual Camera başlatılamadı: {e}")
            print("\n[FIX] OBS Virtual Camera kurulumu:")
            print("  1. OBS Studio'yu açın")
            print("  2. Tools → Virtual Camera → Start")
            print("  3. Script'i yeniden başlatın\n")
            return False
    
    def send_frame(self, frame: np.ndarray) -> None:
        """Frame'i virtual camera'ya gönder"""
        if not self.running or self.camera is None:
            return
        
        try:
            # BGR'den RGB'ye çevir (OpenCV BGR kullanır)
            if frame.shape[2] == 3:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                frame_rgb = frame
            
            # Boyut kontrolü
            if frame_rgb.shape[:2] != (self.height, self.width):
                frame_rgb = cv2.resize(frame_rgb, (self.width, self.height))
            
            # Queue'ya ekle (eğer dolu değilse)
            if not self.frame_queue.full():
                self.frame_queue.put(frame_rgb, block=False)
                
        except Exception as e:
            print(f"Frame gönderme hatası: {e}")
    
    def _send_frames(self) -> None:
        """Background thread: Queue'dan frame al ve camera'ya gönder"""
        while self.running:
            try:
                # Queue'dan frame al (timeout ile)
                frame = self.frame_queue.get(timeout=0.1)
                
                # Virtual camera'ya gönder
                if self.camera is not None:
                    self.camera.send(frame)
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Frame send thread hatası: {e}")
                time.sleep(0.1)
    
    def stop(self) -> None:
        """Virtual camera'yı durdur"""
        print("\n[STOP] Virtual Camera kapatılıyor...")
        
        self.running = False
        
        if self.thread is not None:
            self.thread.join(timeout=2.0)
        
        if self.camera is not None:
            self.camera.close()
            self.camera = None
        
        print("✓ Virtual Camera kapatıldı\n")
    
    def is_active(self) -> bool:
        """Virtual camera aktif mi?"""
        return self.running and self.camera is not None


# Singleton instance
_virtual_camera: Optional[VirtualCameraOutput] = None

def get_virtual_camera(width: int = 640, height: int = 480, fps: int = 30) -> Optional[VirtualCameraOutput]:
    """Virtual camera instance'ı al (singleton)"""
    global _virtual_camera
    
    if _virtual_camera is None:
        _virtual_camera = VirtualCameraOutput(width, height, fps)
        if not _virtual_camera.start():
            _virtual_camera = None
    
    return _virtual_camera

def stop_virtual_camera() -> None:
    """Virtual camera'yı durdur"""
    global _virtual_camera
    
    if _virtual_camera is not None:
        _virtual_camera.stop()
        _virtual_camera = None
