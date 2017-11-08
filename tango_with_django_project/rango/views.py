from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import PageForm, CategoryForm
from django.contrib import messages
from django.shortcuts import redirect
from rango.helper import visitor_cookie_handler, return_cookie_value

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
