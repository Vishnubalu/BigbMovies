import json
import django
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import os
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from API import events
from django.http import JsonResponse


@api_view(['GET'])
@csrf_exempt
def popular_rating(request):
    data = {
        "movies": events.popular().to_dict(orient="records")
    }
    return (JsonResponse(data))


@api_view(['GET'])
@csrf_exempt
def recent_movies(request):
    data = {
        "movies": events.recent()
    }
    return (JsonResponse(data))


@api_view(['POST'])
@csrf_exempt
def category_movies(request):
    try:
        requested = json.load(request)
        print(requested['category'],requested['type'], requested['number'])
        data = {
            "movies": events.category_sort(requested['category'],requested['type'], requested['number'])
        }
        return JsonResponse(data)

    except ValueError as e:
        print(e.args[0], status.HTTP_400_BAD_REQUEST)
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def genre_movies(request):
    try:
        requested = json.load(request)
        data = events.genres(requested['genre'], requested['dataset'])
        return JsonResponse(data)

    except ValueError as e:
        print(e.args[0], status.HTTP_400_BAD_REQUEST)
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def movie_videoId(request):
    try:
        requested = json.load(request)
        id = events.video_links(requested['imdbId'])
        return JsonResponse(id)

    except ValueError as e:
        print(e.args[0], status.HTTP_400_BAD_REQUEST)
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
