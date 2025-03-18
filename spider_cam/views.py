from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import StreamingHttpResponse
from threading import Thread
import cv2
import time


class VideoCamera:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        # Set camera properties for better performance
        self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.camera.set(cv2.CAP_PROP_FPS, 60)  # Request 30 FPS
        self.success, self.frame = self.camera.read()
        self.running = True
        self.thread = Thread(target=self.update_frame, daemon=True)
        self.thread.start()

    def update_frame(self):
        """Continuously capture frames in the background."""
        while self.running:
            self.success, self.frame = self.camera.read()
            # Remove sleep delay to maximize frame rate
            
    def get_frame(self):
        """Encode frame as JPEG and return."""
        if not self.success:
            return None
        # Optimize JPEG encoding with lower quality for better speed
        _, buffer = cv2.imencode('.jpg', self.frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        return buffer.tobytes()

    def stop(self):
        """Stop the camera thread and release resources."""
        self.running = False
        self.thread.join()
        self.camera.release()

# Create a single shared camera instance
video_camera = VideoCamera()

def gen_frames():
    """Yield frames from the shared camera instance."""
    while True:
        frame = video_camera.get_frame()
        if frame is None:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


# Create your views here.
class SpiderCamView(TemplateView):
    template_name = 'spider_cam.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Spider Cam'
        return context
    
class FunnySpiderView(TemplateView):
    template_name = 'funny_spider.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Funny Spider'
        return context