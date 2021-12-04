from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Avg, Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, ListView, DeleteView

from .forms import MyWordForm
from .models import User, Course, Lesson, Word, MyWord

from django_pandas.io import read_frame
import pandas as pd
from collections import Counter

import random


class IndexView(LoginRequiredMixin, ListView):
    """Show All Lesson the Current User Has Taken"""
    template_name = 'students/index.html'
    model = Lesson
    paginate_by = 20
    
    def get_queryset(self):
        current_user = self.request.user
        return Lesson.objects.filter(student=current_user.id)


def myChart(request):
    """Summary of Achievement"""
    # data from models
    current_user = request.user
    queryset = Lesson.objects.filter(student=current_user.id)
    tasks = queryset.count()
    completed = Lesson.objects.filter(student=current_user.id, completed=True).count()

    # data from django-pandas
    df = read_frame(queryset, fieldnames=['student', 'course', 'teacher', 'textbook', 'page', 'score', 'comment', 'created', 'updated', 'completed'])
    teachers = df.teacher
    teacher_count = dict(Counter(teachers))
    textbooks = df.textbook
    textbook_count = dict(Counter(textbooks))
    ave_score = df.score.mean()
    max_score = df.score.max()
    words = Word.objects.all()
    word = random.choice(words)
  
    return render(request, 'students/mychart.html', {
        'tasks': tasks,
        'completed': completed,
        'ave_score': ave_score,
        'max_score': max_score,
        'teacher_count': teacher_count,
        'textbook_count': textbook_count,
        'word': word
    })


def mywordlist(request):
    """Individual Student has Personal MyWordList"""
    form = MyWordForm()
    current_user = request.user
    qs = MyWord.objects.filter(student=current_user.id)
    return render(request, 'students/myword.html', {
        'form': form,
        'qs': qs,
    })


def save_data(request):
    """Add and Save New Word Using Ajax"""
    if request.method == "POST":
        form = MyWordForm(request.POST)
        if form.is_valid():
            editid = request.POST.get('editid')
            new_word = request.POST['new_word']
            meaning = request.POST['meaning']
            if(editid == ''):
                myword = MyWord(new_word=new_word, meaning=meaning, student=request.user)
            else:
                myword = MyWord(id=editid, new_word=new_word, meaning=meaning, student=request.user)
            myword.save()
            current_user = request.user
            qs = MyWord.objects.filter(student=current_user.id)
            save_qs = qs.values()
            # print(save_qs)
            qs_data = list(save_qs)

            return JsonResponse({'status':'Save', 'qs_data': qs_data})
        else:
            return JsonResponse({'status':0})


def delete_data(request):
    """Delete Word form MyWord Using Ajax"""
    if request.method == "POST":
        id = request.POST.get('sid')
        print(id)
        pi = MyWord.objects.get(pk=id)
        pi.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})
            

def edit_data(request):
    if request.method == "POST":
        id = request.POST.get('sid')
        print(id)
        myword = MyWord.objects.get(pk=id)
        myword_data = {"id": myword.id, "new_word": myword.new_word, "meaning": myword.meaning}
        return JsonResponse(myword_data)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "students/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "students/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "students/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "students/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "students/register.html")


    

