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
        data = request.POST.get('frame')
        
    
        img_data = base64.b64decode(data.split(',')[1]) 
        img = Image.open(BytesIO(img_data))
        img = np.array(img) 

        
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        
        start_point = (100, 100)
        end_point = (500, 400)
        color = (0, 255, 0) 
        thickness = 3
        img_with_box = cv2.rectangle(img, start_point, end_point, color, thickness)

        
        _, buffer = cv2.imencode('.jpg', img_with_box)
        processed_frame = base64.b64encode(buffer).decode('utf-8')

        return JsonResponse({'processedFrame': f"data:image/jpeg;base64,{processed_frame}"})
    return JsonResponse({'error': 'Invalid request'}, status=400)
