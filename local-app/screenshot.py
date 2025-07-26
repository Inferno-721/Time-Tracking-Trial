from PIL import ImageGrab
import io
import base64

def take_screenshot():
    img = ImageGrab.grab()
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    byte_data = buf.getvalue()
    # For API: base64 encode
    return base64.b64encode(byte_data).decode('utf-8')