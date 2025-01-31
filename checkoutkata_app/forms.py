from django import forms
from .models import *
from .const import ALPHABET_CHOICES, CSS_FORM_CLASS


# form for signup 
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs=CSS_FORM_CLASS))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs=CSS_FORM_CLASS), label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_shop_owner', 'password']
        widgets = {
            'username': forms.TextInput(attrs=CSS_FORM_CLASS),
            'email': forms.EmailInput(attrs=CSS_FORM_CLASS),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    
#form for making items 
class ItemForm(forms.ModelForm):
    DISCOUNT_CHOICES = [('', 'None')] + [(discount.id, f"{discount.quantity} items for {discount.price}") for discount in Discount.objects.all()]
    
    discounts = forms.MultipleChoiceField(
        choices=DISCOUNT_CHOICES,
        widget=forms.SelectMultiple(attrs=CSS_FORM_CLASS)
    )

    name = forms.ChoiceField(choices=ALPHABET_CHOICES, widget=forms.Select(attrs=CSS_FORM_CLASS))

    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'discounts']
        widgets = {
            'description': forms.Textarea(attrs=CSS_FORM_CLASS),
            'price': forms.NumberInput(attrs=CSS_FORM_CLASS),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['discounts'].choices = [('', 'None')] + [(discount.id, f"{discount.quantity} items for {discount.price}") for discount in Discount.objects.all()]

    def clean_discounts(self):
        selected_discounts = self.cleaned_data.get('discounts')
        if not selected_discounts or selected_discounts == ['']:
            return []
        return selected_discounts
    
#form for discount 
class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['quantity', 'price']
        widgets = {
            'quantity': forms.NumberInput(attrs=CSS_FORM_CLASS),
            'price': forms.NumberInput(attrs=CSS_FORM_CLASS),
        }


