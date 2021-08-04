from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from django.core.files.storage import default_storage
import cv2
import numpy as np
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from .models import Image
from .serializers import image_serializers
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from tensorflow.python.keras.models import load_model
def index(request):
    if request.method == 'POST':

        class_name = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                       'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

        # 이미지 업로드
        img = cv2.imdecode(np.fromstring(request.FILES['image'].read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        request.FILES['image'].seek(0)
        # 28x28로 변환
        img = cv2.resize(img, dsize=(28, 28), interpolation=cv2.INTER_AREA)
        img2 = cv2.resize(img, dsize=(280, 280), interpolation=cv2.INTER_AREA)
        img = 1-img/255.0
        # cv2.imshow('img', img2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        #모델 불러오기
        model = load_model('mnistapp/kerasmodel/model.h5')
        # Model 사용하기
        prediction = model.predict(img.reshape(-1, 28, 28, 1))
        label = class_name[np.argmax(prediction)]
        request.data['title'] = label
        serializer = image_serializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return render(request, "mnistapp/insert_img.html", {"predictions": label})
    else:
        return render(request, "mnistapp/insert_img.html")

class MyFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        class_name = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                      'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
        file = request.FILES['image']

        img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        file.seek(0)
        print(file)
        img = cv2.resize(img, dsize=(28, 28), interpolation=cv2.INTER_AREA)
        img = 1 - img / 255.0
        # 모델 불러오기
        model = load_model('mnistapp/kerasmodel/model.h5')
        # Model 사용하기
        prediction = model.predict(img.reshape(-1, 28, 28, 1))
        label = class_name[np.argmax(prediction)]
        request.data['title'] = label
        print(request.data)
        serializer = image_serializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = image_serializers(Image.objects.all(), many=True)
        return Response(serializer.data)