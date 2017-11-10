from django import template
from rango.models import Category, UserProfile

register = template.Library()

@register.inclusion_tag('rango/cats.html')
def get_category_list(category=None):
    return {'cats': Category.objects.all(),
            'active_cat': category}


@register.inclusion_tag('rango/user_profile.html')
def get_user_profile(user=None):
    aux = UserProfile.objects.filter(user=user)
    if aux.exists():
        return {'user_profile': aux[0]}

