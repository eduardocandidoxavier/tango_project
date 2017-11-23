import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page, UserProfile
from django.contrib.auth.models import User
#This lines above makes the Django environment available so that we can use the models

def populate():
    users = [  {'email': 'eduardo@ic.unicamp.br'+str(i),
                'password': 'teste'+str(i),
                'website': 'www.example.com'
                }  for i in range(100)
            ]
    pages_professores = [
        {'title': 'Eduardo C. Xavier'+str(i),
        'url': 'http://www.ic.unicamp.br/~eduardo',
         'views': i} for i in range(100)

    ]


    pages_professores2 = [
        {'title': 'Eduardo C. Xavier2'+str(i),
        'url': 'http://www.ic.unicamp.br/~eduardo',
         'views': i} for i in range(100)

    ]

    pages_jornais = [
        {'title': 'Folha de São Paulo'+str(i),
         'url': 'http://www.folha.uol.com.br',
         'views': i} for i in range(100)
    ]

    cats = { 'Professores IC': {'pages': pages_professores, 'views': 1000, 'likes': 500},
              'Jornais': {'pages': pages_jornais, 'views': 10000, 'likes': 500},
             }

    cats2 = {'Cat'+str(i): {'pages': pages_professores2, 'views': i, 'likes': i} for i in range(1,100)}


    add_categories(cats)
    add_categories(cats2)
    add_users(users)

def add_users(users):
    for user in users:
        add_user(user)

def add_categories(cats):
    for cat in cats.keys():
        c = add_category(cat, cats[cat])
        for page in cats[cat]['pages']:
            add_page(c, page['title'],page['url'], page['views'])

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
    try:
        p = Page.objects.get(title=title)
    except Page.DoesNotExist:
        p = Page()
    p.title = title
    p.category = category
    p.url = url
    p.views = views
    p.save()
    return p

def add_user(user):
    try:
        u = User.objects.get(username=user['email'])
    except User.DoesNotExist:
        u = User()
    u.email = user['email']
    u.username = user['email']
    u.set_password(user['password'])
    u.save()
    try:
        user_profile = UserProfile.objects.get(user__username=user['email'])
    except UserProfile.DoesNotExist:
        user_profile = UserProfile()
    user_profile.user = u
    user_profile.website = user['website']
    user_profile.save()

if __name__ == '__main__':
    print('Populating rango models....')
    populate()

