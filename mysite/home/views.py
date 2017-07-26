from django.shortcuts import render
from .models import User, Item, Tags

def index(request):
    latest_item_list = Item.objects.order_by('-pub_date')
    context = {'latest_item_list':latest_item_list,
              }
    return render(request, 'home/header.html', context)