import json
import os
from functools import lru_cache

import assemblyai as aai
import openai
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from pytube import YouTube

import api_keys

from .models import BlogPost


# Create your views here.
@login_required
def index(request):
    return render(request, "index.html")


@csrf_exempt
def generate_blog(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            yt_link = data["link"]
            lang = data["lang"]
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid data sent"}, status=400)

        # get yt title
        title = yt_title(yt_link)

        # get transcript
        transcription = get_transcription(yt_link, lang)
        if not transcription:
            return JsonResponse({"error": " Failed to get transcript"}, status=500)

        # use AI to generate the blog
        blog_content = generate_blog_from_transcript_ollama_local(transcription)
        if not blog_content:
            return JsonResponse({"error": " Failed to generate blog article"}, status=500)

        # save blog article to database
        new_blog_article = BlogPost.objects.create(
            user=request.user,
            youtube_title=title,
            youtube_link=yt_link,
            generated_content=blog_content,
        )
        new_blog_article.save()

        # return blog article as a response
        return JsonResponse({"content": blog_content})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title


def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    if video:
        out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + ".mp3"

    try:
        os.rename(out_file, new_file)
    except FileExistsError:
        os.remove(out_file)

    return new_file


@lru_cache
def get_transcription(link, lang):
    audio_file = download_audio(link)

    aai.settings.api_key = api_keys.assemblyai_key
    config = aai.TranscriptionConfig(language_code=lang)

    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(audio_file)

    return transcript.text


def generate_blog_from_transcription_chatgpt(transcription):
    openai.api_key = api_keys.openai_key

    prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"

    response = openai.completions.create(model="text-davinci-003", prompt=prompt, max_tokens=1000)

    generated_content = response.choices[0].text.strip()

    return generated_content


def generate_blog_from_transcript_ollama_local(transcription):
    ollama_host = os.getenv("OLLAMA_HOST_", "localhost")
    ollama_port = os.getenv("OLLAMA_PORT", "11434")
    url = f"http://{ollama_host}:{ollama_port}/api/generate"
    headers = {"Content-Type": "application/json"}
    prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"
    data = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    generated_content = json.loads(response.text)["response"]

    return generated_content


def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, "all-blogs.html", {"blog_articles": blog_articles})


def blog_details(request, pk):
    blog_article_detail = BlogPost.objects.get(id=pk)
    if request.user == blog_article_detail.user:
        return render(request, "blog-details.html", {"blog_article_detail": blog_article_detail})
    else:
        return redirect("/")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            error_message = "Invalid username or password"
            return render(request, "login.html", {"error_message": error_message})

    return render(request, "login.html")


def user_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repeatPassword = request.POST["repeatPassword"]

        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect("/")
            except:
                error_message = "Error creating account"
                return render(request, "signup.html", {"error_message": error_message})
        else:
            error_message = "Password do not match"
            return render(request, "signup.html", {"error_message": error_message})

    return render(request, "signup.html")


def user_logout(request):
    logout(request)
    return redirect("/")
