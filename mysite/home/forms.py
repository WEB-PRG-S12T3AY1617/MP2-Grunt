from django import forms
from .models import User, Item, Offer


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'degree', 'office']

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['itemO', 'cashO', 'message']

        labels = {
            'itemO': 'Item Offer',
            'cashO': 'Cash Offer',
        }

    def __init__(self, user=None, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        if user is not None:
            try:
                user = User.objects.get(id=user)

                try:
                    items = Item.objects.filter(userName=user)
                    self.fields['itemO'] = forms.ModelChoiceField(queryset=items, widget=forms.Select(attrs={'required': False}),
                                                                  label='Item Offer', required=False)
                    self.fields['itemO'].label_from_instance = lambda obj: "%s" % obj.name
                except Item.DoesNotExist:
                    pass
            except User.DoesNotExist:
                pass