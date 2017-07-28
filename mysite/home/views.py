from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import User, Item, Tags

def index(request):
    latest_item_list = Item.objects.order_by('-pub_date')
    latest_tag_list = Tags.objects.all()
    context = {'latest_item_list': latest_item_list,
              'latest_tag_list': latest_tag_list,
              }
    return render(request, 'home/home.html', context)


def profile(request, username_id):
    user = get_object_or_404(User, pk=username_id)
    latest_item_list = Item.objects.order_by('-pub_date')
    latest_tag_list = Tags.objects.all()
    context = {'user':user,
               'latest_item_list': latest_item_list,
               'latest_tag_list': latest_tag_list,
              }
    return render(request, 'home/profile.html', context)
