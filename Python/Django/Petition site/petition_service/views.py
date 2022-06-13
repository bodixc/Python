import datetime

from django.shortcuts import render, reverse, redirect

from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.utils import timezone

from .models import Petition, Signature, Category, Status
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from petition_service.forms import *

from django.contrib.postgres import *

def Home(request):
    categories = Category.objects.all()
    return render(request, 'petitions/home.html', {'categories': categories})

def Petition_list(request, category=''):
    categories = Category.objects.all()
    if request.path.__contains__('all'):
        petitions = Petition.objects.all()
        header = 'Усі петиції'
    elif category == 'random':
        category_name = categories.order_by('?')[0].name
        petitions = Petition.objects.filter(category__name=category_name, deleted=False)
        header = 'Петиції. Випадкова категорія: ' + category_name
    elif request.path.__contains__('overdue'):
        petitions = Petition.objects.filter(overdue=False)
        for petition in petitions:
            if petition.creation_date < (timezone.now().date() - timezone.timedelta(days=14)) and petition.status.value == 'Збір підписів':
                status_id = Status.objects.get(value='Збір прострочено').id
                petition.status_id = status_id
                petition.overdue = True
                petition.save()
        petitions = Petition.objects.filter(overdue=True, deleted=False)
        header = 'Прострочені петиції'
    elif request.path.__contains__('my-petitions'):
        petitions = Petition.objects.filter(author=request.user, deleted=False)
        header = 'Мої петиції'
    else:
        petitions = Petition.objects.filter(category__url=category, deleted=False)
        header = 'Петиції. Категорія: ' + str(Category.objects.get(url=category))
    return render(request, 'petitions/petition_list.html', {'categories': categories, 'header': header, 'petition_list': petitions})

def PetitionDetail(request, id):
    categories = Category.objects.all()
    petition = Petition.objects.get(id=id)
    if petition.creation_date < (timezone.now().date() - timezone.timedelta(days=14)) and petition.status.value == 'Збір підписів':
        status_id = Status.objects.get(value='Збір прострочено').id
        petition.status_id = status_id
        petition.overdue = True
        petition.save()
    signers = Signature.objects.filter(petition_id=id)
    already_sign = Signature.objects.filter(petition_id=petition.id, signer__username=request.user.username)
    already = 'true'
    if already_sign.count() != 0:
        already = 'false'
    delete = 'false'
    if petition.author == request.user:
        delete = 'true'
    return render(request, 'petitions/petition_detail.html', {'categories': categories, 'petition': petition,
                                                              'signers': signers, 'already': already, 'delete': delete})
def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('profile'))
                else:
                    form.add_error(None, 'Недійсний аккаунт!')
            else:
                form.add_error(None, 'Неправильний логін або пароль!')
    else:
        form = LoginForm()
    return render(request, 'petitions/login.html', {'form': form})

def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def Sign(request, id):
    petition = Petition.objects.get(id=id)
    sign = ''
    if request.method != 'POST':
        header = ''
        if request.user.username == "":
            header = 'Для підпису петиції потрібно авторизуватися!'
        else:
            sign = Signature.objects.filter(signer__username=request.user.username, petition_id=id)
            if len(sign) == 0:
                header = 'Підписати від імені користувача: ' + request.user.username
            else:
                header = 'Ви вже підписали дану петицію'
        return render(request, 'petitions/sign.html', {'petition': petition, 'header': header})
    else:
        if len(sign) == 0:
            Signature(signer_id=request.user.id, petition_id=id).save()
            if Signature.objects.filter(petition_id=id).count() == 5:
                new_status = Status.objects.get(value='На розгляді').id
                new_petition = Petition.objects.get(id=id)
                new_petition.status_id = new_status
                new_petition.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')[0:-5])

def Delete(request, id):
    petition = Petition.objects.get(id=id)
    sign = ''
    if request.method != 'POST':
        header = ''
        if request.user.username == "":
            header = 'Для видалення петиції потрібно авторизуватися!'
        else:
            header = f'{request.user.last_name} {request.user.first_name}! Ви дійсно бажаєте видалити дану петицію?'
        return render(request, 'petitions/delete.html', {'petition': petition, 'header': header})
    else:
        petition.deleted = True
        petition.save()
        return redirect('profile')

def Registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'petitions/registration.html', {'form': form})

def Profile(request):
    user_petitions = Petition.objects.filter(author__username=request.user.username, deleted=False)
    user_petitions_on_signing = user_petitions.filter(status__value="Збір підписів")
    user_petitions_on_consideration = user_petitions.filter(status__value="На розгляді")
    user_petitions_is_considerated = user_petitions.filter(status__value="Розглянуто")
    user_petitions_signatures = Signature.objects.filter(petition__in=user_petitions)
    user_signatures = Signature.objects.filter(signer__username=request.user.username)
    user_petitions_overdue = user_petitions.filter(creation_date__lt=(timezone.now() - timezone.timedelta(days=14)))
    user_petitions_deleted = Petition.objects.filter(author__username=request.user.username, deleted=True)
    return render(request, 'petitions/profile.html', {'user_petitions': user_petitions,
                                                      'user_petitions_signatures': user_petitions_signatures,
                                                      'user_signatures': user_signatures,
                                                      'user_petitions_on_signing': user_petitions_on_signing,
                                                      'user_petitions_on_consideration': user_petitions_on_consideration,
                                                      'user_petitions_is_considerated': user_petitions_is_considerated,
                                                      'user_petitions_overdue': user_petitions_overdue,
                                                      'user_petitions_deleted': user_petitions_deleted,
                                                      })

def CreatePetition(request):
    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data.get('category')
            title = form.cleaned_data.get('title')
            text = form.cleaned_data.get('text')
            get_category_id = Category.objects.get(name=category).id
            get_status_id = Status.objects.get(value='Збір підписів').id
            new_petition = Petition(category_id=get_category_id, title=title, text=text, author_id=request.user.id,
                                    creation_date=datetime.date.today(), status_id=get_status_id)
            new_petition.save()
            return redirect('../'+ str(new_petition.id))
    else:
        form = CreationForm()
    return render(request, 'petitions/create.html', {'form': form})

def Search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            select = form.cleaned_data.get('select')
            search = form.cleaned_data.get('field').lower()
            all_petitions = Petition.objects.filter(deleted=False)
            petitions = set()
            if select == '1':
                user = form.cleaned_data.get('field')
                userr = User.objects.filter(username=user)
                petitions = Petition.objects.filter(author__username=user, deleted=False)
                if userr.count() == 0:
                    form.add_error(None, 'Користувач ' + str(user) + ' - не знайдений!')
            elif select == '2':
                for petition in all_petitions:
                    if petition.title.lower().__contains__(search):
                        petitions.add(petition)
            elif select == '3':
                for petition in all_petitions:
                    if petition.text.lower().__contains__(search):
                        petitions.add(petition)
            if select != '1':
                if len(petitions) == 0:
                    form.add_error(None, 'Петиції не знайдені!')
            return render(request, 'petitions/search.html', {'form': form, 'petitions': petitions})
    else:
        form = SearchForm()
        return render(request, 'petitions/search.html', {'form': form })

