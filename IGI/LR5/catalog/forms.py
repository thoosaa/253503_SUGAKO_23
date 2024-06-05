from django import forms
from .models import Customer, CustomerProfile, Feedback
from .validators import validate_phone_number_format

class CustomerRegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    phonenumber = forms.CharField(max_length=21, validators=[validate_phone_number_format])
    city = forms.CharField(max_length=50)
    address = forms.CharField(max_length=200, widget=forms.Textarea)
    is_18 = forms.BooleanField(label='Есть ли 18?', required=False)

    class Meta:
        model = Customer
        fields = ['username', 'password', 'name', 'phonenumber', 'city', 'address', 'is_18']

class SaleForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
    completion_date = forms.DateField(input_formats = ['%d/%m/%Y'])
    promo_code = forms.CharField(max_length=100, required=False)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['text', 'toy', 'rate']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 50}),  # Виджет для текстового поля
        }

    def __init__(self, *args, **kwargs):
        toys = kwargs.pop('toys', None)  # Получаем список игрушек из kwargs
        super(FeedbackForm, self).__init__(*args, **kwargs)
        if toys:
            self.fields['toy'].queryset = toys



