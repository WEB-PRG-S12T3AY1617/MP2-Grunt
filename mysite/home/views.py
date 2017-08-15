from django.core.paginator import Paginator, Page, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from .models import User, Item, Tags, Offer
from .forms import UserForm, LoginForm, OfferForm


def home(request):
    limit = 10
    latest_item_list = Item.objects.order_by('-pub_date')
    latest_tag_list = Tags.objects.all()

    paginator = Paginator(latest_item_list, limit)
    paginatorT = Paginator(latest_tag_list, limit)
    pageNum = 1
    page = paginator.page(1)
    pageT = paginatorT.page(1)

    if 'page' in request.GET:
        pageNum = int(request.GET['page'])
        try:
            page = paginator.page(pageNum)
            pageT = paginatorT.page(pageNum)
        except PageNotAnInteger:
            page = paginator.page(1)
            pageT = paginatorT.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
            pageT = paginatorT.page(paginator.num_pages)

    context = {'latest_item_list': page,
               'latest_tag_list': pageT,
               'page': pageNum,
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

# def ItemCreate(ModelForm):
#
#     class Meta:
#         model = Item

class OfferCreateView(View):
    form_class = OfferForm
    template_name = 'home/offer.html'

    def get(self, request):
        # Offer.objects.all().delete()
        if 'user' in request.session and 'post' in request.GET:
            offer = None
            user = User.objects.get(id=request.session['user'])
            try:
                offer = Offer.objects.get(offerer=user)
                self.form_class = self.form_class = OfferForm(instance=offer, user=request.session['user'])
            except Offer.DoesNotExist:
                self.form_class = OfferForm(user=request.session['user'])

            return render(request, self.template_name, {'form': self.form_class, 'offer': offer})
        else:
            return HttpResponseRedirect('/home/')

    def post(self, request):
        if 'user' in request.session:
            try:
                item = Item.objects.get(name=request.POST['item'])
                user = User.objects.get(id=request.session['user'])

                try:
                    offer = Offer.objects.get(item=item, offerer=user)
                    form = OfferForm(data=request.POST, instance=offer)

                    if form.is_valid():
                        form.save()
                    else:
                        return render(request, self.template_name, {'form': form})
                except Offer.DoesNotExist:
                    offer = OfferForm(data=request.POST)

                    if offer.is_valid():
                        offer = offer.save(commit=False)
                        offer.item = item
                        offer.offerer = user
                        offer.save()
                    else:
                        return render(request, self.template_name, {'form': offer})

                return HttpResponseRedirect('/home/')
            except Item.DoesNotExist:
                return HttpResponseRedirect('/home/')
        else:
            return HttpResponseRedirect('/home/')

def DeleteOffer(request):
    if 'post' in request.GET and 'user' in request.session:
        try:
            user = User.objects.get(id=request.session['user'])
            post = Item.objects.get(name=request.GET['post'])
            offer = Offer.objects.get(item=post, offerer=user)
            offer.delete()

            return HttpResponseRedirect('/home/')
        except User.DoesNotExist or Item.DoesNotExist or Offer.DoesNotExist:
            return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/home/')

class ItemUpdate(UpdateView):
    model = Item
    fields = ['userName', 'name', 'photo', 'quantity', 'condition', 'itemType', 'courseName', 'pub_date']

class ItemDelete(DeleteView):
    model = Item
    success_url = reverse_lazy('home:homepage')

class LoginFormView(View):
    form_class = LoginForm
    template_name = 'home/login.html'

    #display
    def get(self, request):
        form = self.form_class(None)
        if 'user' in request.session:
            return HttpResponseRedirect('/home/')

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

                request.session['user'] = user.id
                return HttpResponseRedirect('/home/')
            except User.DoesNotExist:
                return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form})

class UserFormView(View):
    form_class = UserForm
    template_name = 'home/registration_form.html'

    # display a blank form
    def get(self, request):
        if 'user' in request.session:
            return HttpResponseRedirect('/home/')

        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # clean (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.password = password
            user.save()

            # returns User objects if correct credentials
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    success_url = reverse_lazy('home:homepage')
                    # return redirect('home:homepage')

            return HttpResponseRedirect('/home/login/')

        return render(request, self.template_name, {'form': form})


def logout(request):
    if 'user' in request.session:
        del request.session['user']
    return HttpResponseRedirect('/home/')


def offerAccept(request):
    if 'offer' in request.GET and 'user' in request.session:
        try:
            offer = Offer.objects.get(id=request.GET['offer'])
            offer.reject = False
            offer.accept = True
            offer.save()

            return HttpResponseRedirect('/home/')
        except Offer.DoesNotExist:
            return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/home/')


def offerReject(request):
    if 'offer' in request.GET and 'user' in request.session:
        try:
            offer = Offer.objects.get(id=request.GET['offer'])
            offer.reject = True
            offer.accept = False
            offer.save()

            return HttpResponseRedirect('/home/')
        except Offer.DoesNotExist:
            return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/home/')


def viewOffer(request):
    if 'user' in request.session and 'post' in request.GET:
        post = Item.objects.get(name=request.GET['post'])

        offers_list = Offer.objects.filter(item=post)
        return render(request, 'home/view.html', {'offers_list': offers_list})
    else:
        return HttpResponseRedirect('/home/')