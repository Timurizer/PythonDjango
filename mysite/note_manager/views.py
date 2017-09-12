# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import django.shortcuts
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import *
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import *


# добавление заметки
# пользователь вводит заголовок, текст и категорию, дата и пользователь определяются автоматически
# при необходимости, категория заносится в базу данных
def add_note(request):
    if request.method == 'POST':
        head = request.POST['aheader']
        body = request.POST['body']
        tag = request.POST['tag']
        selected_tag = Category.objects.filter(category_name=tag)
        if len(selected_tag) == 0:
            selected_tag = Category(category_name=tag)
            selected_tag.save()
        else:
            selected_tag = selected_tag[0]

        if not head or not body or not tag:
            return render(request, 'note_manager/add.html')

        else:

            new_note = Note(note_header=head, note_body=body, category=selected_tag, pub_date=timezone.now(),
                            user=request.user)
            new_note.save()

        return HttpResponseRedirect('/note_manager/')
    else:
        return render(request, 'note_manager/add.html')


# view по умолчанию, заметки упорядочены по дате
class IndexView(generic.ListView):
    template_name = 'note_manager/index.html'
    context_object_name = 'latest_note_list'

    def get_queryset(self):
        return Note.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def find_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': not User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


class IndexViewVarious(generic.ListView):
    template_name = 'note_manager/index.html'
    context_object_name = 'latest_note_list'

    def get_queryset(self):
        # arg = self.kwargs['sort_type']

        print("hereeee")
        print(self.kwargs['sorttype'])
        return Note.objects.filter(pub_date__lte=timezone.now()).order_by('-' + self.kwargs['sorttype'])


# обзор конкретной заметки
# отсюда можно редактировать и удалять заметку (только для ее создателей),
# а так же добавить ее в любимые(избранное)
def detail_view(request, pk):
    if request.method == 'POST':
        elem = get_object_or_404(Note, id=pk)

        elem.delete()
        return HttpResponseRedirect('/note_manager')
    else:
        elem = get_object_or_404(Note, id=pk)
        return render(request, 'note_manager/detail.html', {'note': elem})


# список любимых заметок, тут же можно их удалить
def favourite_list(request):
    if request.method == 'POST':
        note = request.POST['option']
        print("yay111113ref")
        print(note)
        a = Favourite.objects.filter(note_id=note)
        a.delete()
        return HttpResponseRedirect('/note_manager/favourite_list/')
    else:
        favs = set()
        fav_relations = Favourite.objects.filter(user_id=request.user)
        for i in fav_relations:
            favs.add(i.note_id.id)
        favs = Note.objects.filter(id__in=favs)
        return render(request, 'note_manager/favourite_list.html', {'favourite_notes': favs})


# добавление в избранное
def favourite(request, pk):
    elem = get_object_or_404(Note, id=pk)

    selected_fav = Favourite.objects.filter(user_id=request.user, note_id=elem)
    if not selected_fav:
        favour = Favourite(user_id=request.user, note_id=elem)
        favour.save()

    return HttpResponseRedirect('/note_manager')


# реализация поиска по заголовкам и текстам
# Q используется для реализации логического "или"
def search(request):
    if request.GET.get('tosearch'):
        word = request.GET['tosearch']
        notes = Note.objects.filter(Q(note_body__contains=word) | Q(note_header__contains=word))
        print(notes)
        return render(request, 'note_manager/search.html', {'notes': notes})
    else:
        notes = Note.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date')
        return render(request, 'note_manager/search.html', {'notes': notes})


# мои контакты
def contact_us_view(request):
    return render(request, 'note_manager/contacts.html')


# редактирование заметки
def edit_view(request, pk):
    elem = get_object_or_404(Note, id=pk)

    if request.method == 'POST':

        head = request.POST['aheader']
        body = request.POST['body']
        tag = request.POST['tag']
        selected_tag = Category.objects.filter(category_name=tag)
        if not selected_tag:
            selected_tag = Category(category_name=tag)
            selected_tag.save()
        else:
            selected_tag = selected_tag[0]

        if not request.is_ajax():
            elem.note_header = head
            elem.note_body = body
            elem.category = selected_tag

            elem.save()

            return redirect('/note_manager/' + pk + '/')
    else:
        return render(request, 'note_manager/edit.html', {'note': elem})


# регистрация нового пользователя
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/note_manager')
    else:
        form = UserCreationForm()
    return render(request, 'note_manager/signup.html', {'form': form})
