from django.http import JsonResponse
import cv2
import numpy as np
import base64
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from PIL import Image

@csrf_exempt
def process_frame(request):
    if request.method == 'POST':
        # Get the base64 frame from frontend
        data = request.POST.get('frame')
        
        # Decode the base64 frame
        img_data = base64.b64decode(data.split(',')[1])  # Remove "data:image/jpeg;base64,"
        img = Image.open(BytesIO(img_data))
        img = np.array(img)  # Convert to numpy array

        # Convert image from RGB to BGR (OpenCV format)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Draw a green box on the frame
        start_point = (100, 100)
        end_point = (500, 400)
        color = (0, 255, 0)  # Green color
        thickness = 3
        img_with_box = cv2.rectangle(img, start_point, end_point, color, thickness)

        # Convert back to base64
        _, buffer = cv2.imencode('.jpg', img_with_box)
        processed_frame = base64.b64encode(buffer).decode('utf-8')

        return JsonResponse({'processedFrame': f"data:image/jpeg;base64,{processed_frame}"})
    return JsonResponse({'error': 'Invalid request'}, status=400)
