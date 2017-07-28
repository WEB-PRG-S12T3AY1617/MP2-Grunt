from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from .models import User, Item, Tags
from .forms import UserForm


def home(request):
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
    context = {'user': user,
               'latest_item_list': latest_item_list,
               'latest_tag_list': latest_tag_list,
               }
    return render(request, 'home/profile.html', context)


class ItemCreate(CreateView):
    model = Item
    fields = ['userName', 'name', 'photo', 'quantity', 'condition', 'itemType', 'courseName', 'pub_date']


class ItemUpdate(UpdateView):
    model = Item
    fields = ['userName', 'name', 'photo', 'quantity', 'condition', 'itemType', 'courseName', 'pub_date']


class ItemDelete(DeleteView):
    model = Item
    success_url = reverse_lazy('home:home')


class UserFormView(View):
    form_class = UserForm
    template_name = 'home/registration_form.html'

    # display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def get(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # clean (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if correct credentials
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('home:home')

        return render(request, self.template_name, {'form': form})


