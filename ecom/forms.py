from django import forms
from django.contrib.auth.models import User
from . import models
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
#cliente
class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class':'form-control','type':'password', 'name': 'password','placeholder':'Password'})
        }

class PaqueteForm(ModelForm):
    class Meta:
        model = models.Paquete
        fields = "__all__"
        widgets = {
            'producto_id': forms.CheckboxSelectMultiple()
        }

from django.core.validators import MinLengthValidator
class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['address', 'mobile', 'profile_pic']



#cliente-empresarial
class CustomerEmpresarialUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class':'form-control','type':'password', 'name': 'password','placeholder':'Password'})
        }

class CustomerEmpresarialForm(forms.ModelForm):
    class Meta:
        model = models.CustomerEmpresarial
        fields = '__all__'



#productos
class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'




#productos
class ProductsinimagenForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'



class Detalle_ProductForm(forms.ModelForm):
    class Meta:
        model = models.ProductDetails
        fields = ['title', 'title_details']


class A├▒adirproductokardexForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['stock']


# address of shipment
from django.core.validators import RegexValidator

from django.core.exceptions import ValidationError
def only_int(value):
    if value.isdigit() == False:
        raise ValidationError('ID contains characters')

class AddressForm(forms.Form):
    locales = (
        ('Lima Centro', 'Lima Centro'),
        ('Lima Sur', 'Lima Sur'),
        ('Lima Este', 'Lima Este'),
        ('Lima Norte', 'Lima Norte'),
    )
    distritos = (
        ('Anc├│n', 'Anc├│n'),
        ('Ate Vitarte', 'Ate Vitarte'),
        ('Barranco', 'Barranco'),
        ('Bre├▒a', 'Bre├▒a'),
        ('Carabayllo', 'Carabayllo'),
        ('Chorrillos', 'Chorrillos'),
        ('Cieneguilla', 'Cieneguilla'),
        ('Comas', 'Comas'),
        ('El Agustino', 'El Agustino'),
        ('Independencia', 'Independencia'),
        ('Jes├║s Mar├şa', 'Jes├║s Mar├şa'),
        ('La Molina', 'La Molina'),
        ('La Victoria', 'La Victoria'),
        ('Lima', 'Lima'),
        ('Lur├şn', 'Lur├şn'),
        ('Miraflores', 'Miraflores'),
        ('Pachacamac', 'Pachacamac'),
        ('Puente Piedra', 'Puente Piedra'),
        ('San Bartolo', 'San Bartolo'),
        ('San Isidro', 'San Isidro'),
        ('San Juan de Lurigancho', 'San Juan de Lurigancho'),
        ('San Juan de Miraflores	', 'San Juan de Miraflores	'),
        ('San Luis', 'San Luis'),
        ('San Miguel', 'San Miguel'),
        ('Surquillo', 'Surquillo'),
        ('Villa El Salvador', 'Villa El Salvador'),
    )
    numeric = RegexValidator(r'^[0-9+]', 'Only digit characters.')
    Email = forms.EmailField()
    Mobile = forms.CharField(max_length=9, min_length=7, validators=[only_int], error_messages={
               'required': 'Por favor ingresar 9 digitos numericos'
                })
    Address = forms.CharField(max_length=400)
    Dni = forms.CharField(max_length=9)
    Distrito = forms.ChoiceField(choices=distritos)
    localidad = forms.ChoiceField(choices=locales)



class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.Feedback
        fields = ['name', 'feedback']


# for updating status of order
class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Orders
        fields = ['status']


# for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = models.Orders
        fields = ['delivery_zona']


# address of shipment
class PersonalizacionForm(forms.Form):
    locales = (
        ('Lima Centro', 'Lima Centro'),
        ('Lima Sur', 'Lima Sur'),
        ('Lima Este', 'Lima Este'),
        ('Lima Norte', 'Lima Norte'),
    )
    Email = forms.EmailField()
    Mobile = forms.IntegerField()
    Address = forms.CharField(max_length=500)
    localidad = forms.ChoiceField(choices=locales)

class ResponderFeedbackForm(forms.Form):
   descripcion_solucion=forms.CharField(max_length=200)

