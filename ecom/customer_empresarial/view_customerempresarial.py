from django.contrib.auth.decorators import login_required, user_passes_test
from ecom.views import is_customer_empresarial
from django.shortcuts import render, redirect
from ecom import forms, models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.views.generic import ListView,CreateView,UpdateView,DetailView,View
from datetime import datetime
from rest_framework.authtoken.models import Token
# ---------------------------------------------------------------------------------
# ------------------------ CUSTOMER EMPRESARIAL ------------------------------
# ---------------------------------------------------------------------------------

@login_required(login_url='customerempresariallogin')
@user_passes_test(is_customer_empresarial)
def customerempresarial_home_view(request):
    products = models.Product.objects.all()
    categoria = models.Categoria.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0
    return render(request, 'ecom/customer_home.html',
                  {'products': products, 'categoria': categoria, 'product_count_in_cart': product_count_in_cart})


class customer_empresarial_singup(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'ecom/cliente_empresarial/customer_empresarial_signup.html')

    def post(self, request, *args, **kwargs):
        usuario = request.POST.get("usuario")
        contrasena = request.POST.get("contraseña")
        ruc = request.POST.get("ruc")
        razonSocial= request.POST.get("razon_social")
        estado = request.POST.get("estado")
        condicion =  request.POST.get("condicion")
        direccion = request.POST.get("direccion")
        departamento = request.POST.get("departamento")
        provincia = request.POST.get("provincia")
        distrito = request.POST.get("distrito")
        ubigeo = request.POST.get("ubigeo")
        capital = request.POST.get("capital")



        user = models.User(username=usuario, password=contrasena)
        user.set_password(user.password)
        user.save()
        r = user.set_password(user.password)
        empresa = models.CustomerEmpresarial(user=r, ruc=ruc, razonsocial=razonSocial, estado=estado, condicion=condicion, direccion=direccion, departamento=departamento, provincia=provincia, distrito=distrito, ubigeo=ubigeo, capital=capital)
        empresa.user = user
        empresa.save()
        my_customer_empresarial_group = Group.objects.get_or_create(name='CUSTOMEREMPRESARIAL')
        my_customer_empresarial_group[0].user_set.add(user)
        t = Token.objects.create(user=user)
        t.save()

        return HttpResponseRedirect('customerlogin')

