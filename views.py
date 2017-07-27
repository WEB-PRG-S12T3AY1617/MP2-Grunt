from django.http import Http404
from django.shortcuts import render
from .models import User, Item, Tags

def index(request):
    latest_item_list = Item.objects.order_by('-pub_date')
    # context = {'latest_item_list': latest_item_list}
    return render(request, 'home/header.html', {'latest_item_list': latest_item_list})

def profile(request, username_id):
    # return HttpResponse("<h2>This is the profile page of user: " + str(username_id) + "</h2>")
    try:
        user = User.objects.get(pk=username_id)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    return render(request, 'home/profile.html', {'user': user})

