from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import PageForm, CategoryForm

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


def add_page(request):
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
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
