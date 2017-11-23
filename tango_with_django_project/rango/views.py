from django.shortcuts import render
from rango.models import Category, Page, UserProfile
from rango.forms import PageForm, CategoryForm, UserForm, LoginForm, UpdateUserForm
from django.contrib import messages
from django.shortcuts import redirect
from rango.helper import visitor_cookie_handler, return_cookie_value
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rango.helper import verify_confirmation_token, send_confirmation_email
from django.contrib.auth.decorators import login_required
from rango.decorators import user_email_confirmed
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    visits = return_cookie_value(request, 'visits', '1')
    context_dict = {'categories': category_list,
                    'pages_list': pages_list,
                    'visits': visits}
    response = render(request, 'rango/index.html', context_dict)
    visitor_cookie_handler(request)
    return response


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

@login_required(login_url='user_login')
@user_email_confirmed
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
            messages.success(request, 'Page successfully included in category '+page.category.name)
            return redirect('index')
        else:
            messages.error(request, 'Page not included, invalid form!')
            print(form.errors)
    return render(request, 'rango/add_page.html', {'form': form})

@login_required(login_url='user_login')
@user_email_confirmed
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = Category()
            cat.name = form.cleaned_data['name']
            cat.save()
            messages.success(request, 'Category '+cat.name+' successfully included! ')
            return redirect('index')
        else:
            messages.error(request, 'Category not included, invalid form!')
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = User()
            user.email = user_form.cleaned_data['email']
            user.username = user.email
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            user_profile = UserProfile()
            user_profile.user = user
            user_profile.website = user_form.cleaned_data['website']
            if 'picture' in request.FILES:
                user_profile.picture = request.FILES['picture']
            user_profile.save()
            login(request, user)
            send_confirmation_email(request, user)
            messages.success(request,'Registration successfully happened. Now confirm your email.')
            return redirect('index')
        else:
            print(user_form.errors)
            messages.error(request,'Check out your data, invalid form!.')
    else:
        user_form = UserForm()
    context_dict ={ 'user_form': user_form,}
    return render(request,'auth/register.html', context_dict)


def confirm_email(request, uidb64, token):
    user = verify_confirmation_token(request, uidb64, token)
    if user:
        login(request, user)
        messages.success(request, 'You successfully confirmed your account. Welcome!')
        return redirect('index')
    else:
        messages.error(request, 'Activation link is invalid or expired!')
        return redirect('index')


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
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
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        login_form = LoginForm()
    context_dict = {'login_form': login_form}
    return render(request,'auth/user_login.html', context_dict)


@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    messages.success(request,'Your are now logged out!')
    return redirect('index')


@login_required(login_url='user_login')
def confirm_user_email(request):
    return render(request, 'auth/confirm_user_email.html', {})

@login_required(login_url='user_login')
def resend_confirmation_email(request, uid):
    aux = User.objects.filter(id=uid)
    if aux.exists() > 0:
        user = aux[0]
        send_confirmation_email(request, user)
        messages.success(request,'Confirmation email sent!')
    else:
        messages.error(request,'User not found!')
    return redirect('index')


@login_required(login_url='user_login')
def update_user_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(data=request.POST, user=request.user)
        if user_form.is_valid():
            changed_email = False
            fields_changed = []
            user = request.user
            if(user_form.cleaned_data['email'] != request.user.email):
                print(request.user.email)
                user.email = user_form.cleaned_data['email']
                user.username = user.email
                changed_email = True
                fields_changed.append('email')
            if(user_form.cleaned_data['password'] != ''):
                user.set_password(user_form.cleaned_data['password'])
                fields_changed.append('password')
            user.save()
            user_profile = UserProfile.objects.get(user=user)
            if(user_form.cleaned_data['website'] != user_profile.website):
                user_profile.website = user_form.cleaned_data['website']
                fields_changed.append('website')
            if 'picture' in request.FILES:
                user_profile.picture = request.FILES['picture']
                fields_changed.append('picture')
            if changed_email:
                user_profile.confirmed = False
                send_confirmation_email(request, user)
            user_profile.save()
            messages.success(request,'You successfully changed your data: ' + ', '.join(fields_changed)+ '.')
            return redirect('index')
        else:
            print(user_form.errors)
            messages.error(request,'Check out your data, invalid form!')
    else:
        user_form = UpdateUserForm(user=request.user)
    context_dict ={ 'update_user_form': user_form,}
    return render(request,'auth/update_user_profile.html', context_dict)


def show_all_categories(request):
    all_categories = Category.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_categories, 10)
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    context_dic = {'categories': categories}
    return render(request, 'rango/show_all_categories.html', context_dic)


@login_required(login_url='user_login')
def show_all_users(request):
    if request.method == 'POST':
        search_username = request.POST['search_username']
        print(search_username)
        all_users = UserProfile.objects.filter(user__username__icontains=search_username)
    else:
        all_users = UserProfile.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_users, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    context_dic = {'users': users}
    return render(request, 'rango/show_all_users.html', context_dic)