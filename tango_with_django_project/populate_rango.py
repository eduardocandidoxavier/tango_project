import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page
#This lines above makes the Django environment available so that we can use the models

def populate():
    pages1 = [
        {'title': 'Eduardo C. Xavier',
        'url': 'http://www.ic.unicamp.br/~eduardo'},

        {'title': 'Zanoni Dias',
         'url': 'http://www.ic.unicamp.br/~zanoni'},
    ]

    pages2 = [
        {'title': 'Folha de São Paulo',
         'url': 'http://www.folha.uol.com.br'},

        {'title': 'Estado de São Paulo',
         'url': 'http://www.estadao.com.br'
        },
    ]

    cats = { 'Professores IC': {'pages': pages1, 'views': 10, 'likes': 5},
              'Jornais': {'pages': pages2, 'views': 10, 'likes': 5},
             }

    for cat in cats.keys():
        c = add_category(cat, cats[cat])
        for page in cats[cat]['pages']:
            add_page(c, page['title'],page['url'])
    print_categories_pages()

def print_categories_pages():
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print('Category {0}, Page {1}'.format(str(c),str(p)))

def add_category(cat, info):
    c = Category.objects.get_or_create(name=cat)[0]
    c.views = info['views']
    c.likes = info['likes']
    c.save()
    return c

def add_page(category, title, url, views=0):
    p = Page.objects.get_or_create(category=category, title=title, url=url, views=views)[0]
    p.save()
    return p

if __name__ == '__main__':
    print('Populating rango models....')
    populate()