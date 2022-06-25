from .serializers import (ImageSerializer, RegisterSerializer)
from backend.settings import model, ABS_PATH
from django.contrib.auth.models import User
from ebird.api import get_observations
from inspects.models import Image
from pathlib import Path
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import ast
import base64
import json as json
import wikipedia

apiKey = "b6q411p270si"

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': 'api/routes/'},
        {'GET': 'api/images/'},
        {'POST': 'api/users/tokens/'},
        {'POST': 'api/users/register/'},
        {'POST': 'api/imageSearch/'},
    ]
    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getImages(request):
    images = Image.objects.all()
    serialize = ImageSerializer(images, many=True)
    return Response(serialize.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def imageSearch(request):
    request_data = (request.body).decode('utf-8')
    serializer   = ImageSerializer(data=ast.literal_eval(request_data))
    if serializer.is_valid():
        model = serializer.save()
        filePath = getClassifiedBirdImage(model.image.url)
        with open(filePath, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read())
        resp = {"image_base64_encoded": b64_string}
        # return Response(serializer.data, status=201)
        return Response(resp, status=201)
    return Response(serializer.errors, status=400)

def getClassifiedBirdImage(path):
    results = model(ABS_PATH + path)
    results.save(save_dir=(ABS_PATH + '/api/images/result'))
    file_dir = Path(path).parts
    file_name = file_dir[-1]
    return (ABS_PATH + '/api/images/result/' + file_name)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def nameSearch(request):
    data = (request.body).decode('utf-8')
    parsed_dict = json.loads(data)
    print(wikipedia.search(parsed_dict['name']))
    return Response({"title": parsed_dict, "summary": wikipedia.summary(parsed_dict['name']), "content": (wikipedia.page(parsed_dict['name'])).content}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    data = (request.body).decode('utf-8')
    parsed_dict = json.loads(data)
    username = parsed_dict['username']
    model = User.objects.get(username = username)
    return Response({"username": model.username, "email": model.email}, status = 200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def locationSearch(request):
    data = (request.body).decode('utf-8')
    parsed_dict = json.loads(data)
    location = parsed_dict['location']
    print(location)
    response = get_observations(apiKey, location, max_results = 4)
    print(response)
    return Response(response, status = 200)