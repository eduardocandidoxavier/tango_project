from django.shortcuts import render, redirect
from django.http import HttpResponse
from rango.models import Category, Page, UserProfile
from django.contrib.auth.models import User
from rango.forms import PageForm, CategoryForm, UserForm, UserProfileForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from rango.helper import send_confirmation_email, verify_confirmation_token
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from rango.decorators import user_email_confirmed, user_email_confirmed2

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,
                    'pages_list': pages_list}
    return render(request, 'rango/index.html', context_dict)

def about(request):
    context_dict = {'author': 'Eduardo C Xavier'}
    return render(request, 'rango/about.html', context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/show_category.html', context_dict)

@login_required
@user_email_confirmed2
def add_page(request, category_name_slug=None):
    form = PageForm(category_name_slug)
    if request.method == 'POST':
        form = PageForm(category_name_slug, request.POST)
        if form.is_valid():
            page = Page()
            page.title = form.cleaned_data['title']
            page.url = form.cleaned_data['url']
            page.category = Category.objects.filter(name=form.cleaned_data['category'])[0]
            page.save()
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_page.html', {'form': form})


def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = Category()
            cat.name = form.cleaned_data['name']
            cat.save()
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and user_profile_form.is_valid():
            user = User()
            user.email = user_form.cleaned_data['email']
            user.username = user.email
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            user_profile = UserProfile()
            user_profile.user = user
            user_profile.website = user_profile_form.cleaned_data['website']
            if 'picture' in request.FILES:
                user_profile.picture = request.FILES['picture']
            user_profile.save()
            registered = True
            login(request, user)
            send_confirmation_email(request, user)
            messages.success(request,'Registration successfully happened. Now confirm your email.')
            return redirect('index')
        else:
            print(user_form.errors, user_profile_form.errors)
    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()

    context_dict ={ 'user_form': user_form,
                    'user_profile_form': user_profile_form,
                    'registered': registered}
    return render(request,'auth/register.html', context_dict)

def confirm_email(request, uidb64, token):
    user = verify_confirmation_token(request, uidb64, token)
    if user:
        login(request, user)
        messages.success(request, 'Your successfully confirmed your account. Welcome!')
        return redirect('index')
    else:
        return HttpResponse('Activation link is invalid or expired!')

def login_page(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            username = request.POST.get('email')
            password = request.POST.get('password')
            print(username, password)
            user = authenticate(username=username, password=password)
            print(user)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'You are now logged in.')
                    return redirect('index')
                else:
                    messages.error(request, 'Your account is disabled.')
        else:
            messages.error('Invalid username or password.')
    else:
        login_form = LoginForm()
    context_dict = {'login_form': login_form}
    return render(request,'auth/login_page.html', context_dict)

def logout_page(request):
    logout(request)
    messages.success(request,'Your are now logged out!')
    return redirect('index')
