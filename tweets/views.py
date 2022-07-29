from ast import Return
import re
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from tweetme2.settings import ALLOWED_HOSTS
from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


def tweet_detail_view_django(request, tweet_id, *args, **kwargs):
    data = {
        "id": tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content
    except:
        data["message"] = "Not Found"
        status = 404

    return JsonResponse(data, status=status)


def tweet_list_view_django(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweet_list = [x.serialize() for x in qs]
    data = {"isUser": False, "response": tweet_list}
    return JsonResponse(data)

@api_view(['POST']) ## HTTP request client  == POST
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication])
def tweet_create_view(request, *args, **kwargs): 
    serializer = TweetSerializer(data = request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user = request.user)
        return Response(serializer.data, status = 201)
    return Response({}, status = 400)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, status = 200)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        Return({}, status = 404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status = 200)

@api_view(['GET','DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        Return({}, status = 404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message":"You cannot delete this tweet"}, status = 401)
    obj = qs.first()
    obj.delete()
    return Response({"message":"Tweet Removed"}, status = 200)

def tweet_create_view_pure_django(request, *args, **kwargs): 
    print(request.user or None)
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if (request.headers.get('x-requested-with') == 'XMLHttpRequest'
        or request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'): 
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid(): 
        obj = form.save(commit=False)
        obj.user = user
        obj.save()   
        if (request.headers.get('x-requested-with') == 'XMLHttpRequest'
        or request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'):
            return JsonResponse(obj.serialize(), status = 201) 
        if next_url != None and url_has_allowed_host_and_scheme(
            next_url, ALLOWED_HOSTS
            ): 
           return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if (request.headers.get('x-requested-with') == 'XMLHttpRequest'
        or request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'):
            return JsonResponse(form.errors, status = 400) 

    return render(request, "components/form.html", context={"form": form})
