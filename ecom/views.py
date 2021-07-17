from django.shortcuts import render, redirect
from . import forms, models
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from math import ceil
from .models import Product, Orders
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Sum
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View, TemplateView
from rest_framework.authtoken.models import Token
import os
from django.shortcuts import get_object_or_404, redirect, reverse
import json
from django.views import generic


def home_view(request):
    products = models.Product.objects.all().order_by('-id')[:12]
    categoria = models.Categoria.objects.all()
    products_slider = models.Product.objects.all().order_by('-id')
    productods_total = models.Product.objects.all()
    proveedores = models.Proveedor.objects.all()

    allProds = []
    cats = {3}
    for cat in cats:
        prod = models.Product.objects.filter()
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}

    if 'product_ids' in request.COOKIES:

        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')

    return render(request, 'ecom/index.html',
                  {'products': products, 'proveedores': proveedores, 'categoria': categoria, 'allProds': allProds,
                   'products_slider': products_slider,
                   'product_count_in_cart': product_count_in_cart, 'productods_total': productods_total})


# para mostrar el botón de inicio de sesión para el administrador (por sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def customer_signup_view(request):
    customerForm = forms.CustomerForm()
    mydict = {'customerForm': customerForm}
    if request.method == 'POST':
        usuario = request.POST.get("usuario")
        contrasena = request.POST.get("contraseña")
        nombres = request.POST.get("nombres")
        apellidos = request.POST.get("apellidos")
        customerForm = forms.CustomerForm(request.POST, request.FILES)
        if customerForm.is_valid():
            user = models.User(username=usuario, password=contrasena, first_name=nombres, last_name=apellidos)
            user.set_password(user.password)
            user.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            t = Token.objects.create(user=user)
            t.save()

        return HttpResponseRedirect('customerlogin')
    return render(request, 'ecom/customersignup.html', context=mydict)


def eleccion_registro_view(request):
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0
    return render(request, 'ecom/eleccion_registro.html', {"product_count_in_cart": product_count_in_cart})

# -----------para comprobar el usuario -> is_administrador
def is_administrador(user):
    return user.groups.filter(name='Administrador').exists()


# -----------para comprobar el usuario -> iscustomer
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


# -----------para comprobar el usuario -> isclienteempresarial
def is_customer_empresarial(user):
    return user.groups.filter(name='CUSTOMEREMPRESARIAL').exists()


# -----------para comprobar el usuario -> isdistribuidor
def is_distribuidor(user):
    return user.groups.filter(name='DISTRIBUIDOR').exists()


# ---------DESPUÉS DE INTRODUCIR LAS CREDENCIALES, COMPROBAMOS SI EL NOMBRE DE USUARIO Y LA CONTRASEÑA ES DE ADMIN, CLIENTE, DISTRIBUIDOR, CLIENTE EMPRESARIAL
def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-home')
    elif is_distribuidor(request.user):
        return redirect('distribuidor-home')
    elif is_customer_empresarial(request.user):
        return redirect('customer-empresarial-home')
    else:
        return redirect('admin-dashboard')


# ---------------------------------------------------------------------------------
# ------------------------ INICIO DE VISTAS RELACIONADAS CON ADMIN ------------------------------
# ---------------------------------------------------------------------------------

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    # para tarjetas en el tablero
    customercount = models.Customer.objects.all().count()
    productcount = models.Product.objects.all().count()
    ordercount = models.Orders.objects.all().count()
    categoria = Product.objects.values('categoria').annotate(Count('categoria'))
    feedback = models.Feedback.objects.all().count()
    feedbacks2 = models.Feedback.objects.all().filter(estado="Pendiente")
    # para tablas de pedidos recientes
    orders = models.Orders.objects.all()
    ordered_products = []
    ordered_bys = []
    for order in orders:
        ordered_product = models.Product.objects.all().filter(id=order.product.id)
        ordered_by = models.Customer.objects.all().filter(id=order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)

    mydict = {
        'customercount': customercount,
        'productcount': productcount,
        'ordercount': ordercount,
        'distribuidorcount': models.Distribuidor.objects.all().count(),
        'categoria': categoria,
        'feedback': feedback,
        'feedbacks2': feedbacks2,
        'data': zip(ordered_products, ordered_bys, orders),
    }
    return render(request, 'ecom/admin_dashboard.html', context=mydict)


from django.db.models import Func


# Dashboard detalles --------------------------------------------------


@login_required(login_url='adminlogin')
def admin_dashboard_detalle(request):
    camara = Product.objects.filter(categoria__categoria__icontains='camara').count()
    pc = Product.objects.filter(categoria__categoria__icontains='PC').count()
    impresora = Product.objects.filter(categoria__categoria__icontains='impresora').count()
    clientes_registrados = User.objects.all().filter(groups__name='CUSTOMER').count()

    # -----------------   USUARIO - GRUPOS   -----------------------
    total_usuarios = User.objects.all().count()
    total_grupos = Group.objects.all().count()
    r = Product.objects.all().aggregate(Sum('price'))
    t = r.get("price__sum")
    # y = ''.join(map(str, r))

    # -----------------   ORDENES   -----------------------
    orders = models.Orders.objects.all().filter(status__contains='pendiente').order_by('-id')[:3]
    ordered_products = []
    ordered_bys = []
    for order in orders:
        ordered_product = models.Product.objects.all().filter(id=order.product.id)
        ordered_by = models.Customer.objects.all().filter(id=order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)

    orders2 = models.Orders.objects.all().filter(status__contains='Orden Confirmada').order_by('-id')[:3]
    ordered_products2 = []
    ordered_bys2 = []

    for order2 in orders2:
        ordered_product2 = models.Product.objects.all().filter(id=order2.product.id)
        ordered_by2 = models.Customer.objects.all().filter(id=order2.customer.id)
        ordered_products2.append(ordered_product2)
        ordered_bys2.append(ordered_by2)

    mydict = {
        'camara': camara,
        'pc': pc,
        'data': zip(ordered_products, ordered_bys, orders),
        'data2': zip(ordered_products2, ordered_bys2, orders2),
        'impresora': impresora,
        'customercount': models.Customer.objects.all().count(),
        'productcount': models.Product.objects.all().count(),
        'ordercount': models.Orders.objects.all().count(),
        'total_grupos': total_grupos,
        'total_usuarios': total_usuarios,
        'cliente_registrado': clientes_registrados,
        'total_ordenes_pendientes': Orders.objects.filter(status__contains='Pendiente').count(),
        'total_ordenes_confirmadas': Orders.objects.filter(status__contains='Orden Confirmada').count(),
        'total_ordenes_delivery': Orders.objects.filter(status__contains='Fuera para entregar').count(),
        'total_ordenes_entregada': Orders.objects.filter(status__contains='Entregada').count(),
        'total_productos_precio': t,
        'distribuidorcount': models.Distribuidor.objects.all().count(),

    }

    return render(request, 'ecom/dashboard/dashboard_detalle.html', context=mydict)


###########----------PAGOS-----------##############################
# administrador ver tabla de pagos
@login_required(login_url='adminlogin')
def admin_pagos_view(request):
    pagos = models.Payment.objects.all().order_by('-id')
    return render(request, 'ecom/admin/admin_pagos.html', {'pagos': pagos})


from django.utils.decorators import method_decorator


def admin_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.groups.filter(name='Administrador').exists():
            return redirect('/')
        return function(request, *args, **kwargs)

    return wrap

class admin_fecha_ordenes(View):

    @method_decorator(admin_required)
    def dispatch(self, request, *args, **kwargs):
        return super(admin_fecha_ordenes, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        return render(request, 'ecom/admin/admin_buscar_fecha_ordenes.html')

    def post(self, request, *args, **kwargs):
        fecha = request.POST.get("fecha")
        fecha2 = request.POST.get("fecha2")
        ordenes = Orders.objects.raw(
            'select id AS id, order_date, address from ecom_orders where order_date between "' + fecha + '"and"' + fecha2 + '"')
        return render(request, 'ecom/admin/admin_buscar_fecha_ordenes.html',
                      {"ordenes": ordenes})


# -------------------------------------------------------------------------

# administrador ver tabla de clientes
@login_required(login_url='adminlogin')
def view_customer_view(request):
    customers = models.Customer.objects.all()
    clientesempresarial = models.CustomerEmpresarial.objects.all()
    return render(request, 'ecom/view_customer.html',
                  {'customers': customers, 'clientesempresarial': clientesempresarial})


# administrador eliminar cliente
@login_required(login_url='adminlogin')
def delete_customer_view(request, pk):
    customer = models.Customer.objects.get(id=pk)
    user = models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('view-customer')


# administrador eliminar cliente-empresarial
@login_required(login_url='adminlogin')
def delete_customerempresarial_view(request, pk):
    customerempresarial = models.CustomerEmpresarial.objects.get(id=pk)
    user = models.User.objects.get(id=customerempresarial.user_id)
    user.delete()
    customerempresarial.delete()
    return redirect('view-customer')


# administrador actualizar cliente
@login_required(login_url='adminlogin')
def update_customer_view(request, pk):
    customer = models.Customer.objects.get(id=pk)
    user = models.User.objects.get(id=customer.user_id)
    userForm = forms.CustomerUserForm(instance=user)
    customerForm = forms.CustomerForm(request.FILES, instance=customer)
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST, instance=user)
        customerForm = forms.CustomerForm(request.POST, instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('view-customer')
    return render(request, 'ecom/admin_update_customer.html', context=mydict)


# administrador actualizar cliente-empresarial
@login_required(login_url='adminlogin')
def update_customerempresarial_view(request, pk):
    customerempresarial = models.CustomerEmpresarial.objects.get(id=pk)
    user = models.User.objects.get(id=customerempresarial.user_id)
    userempresarialForm = forms.CustomerEmpresarialUserForm(instance=user)
    customerempresarialForm = forms.CustomerEmpresarialForm(request.FILES, instance=customerempresarial)
    mydict = {'userempresarialForm': userempresarialForm, 'customerempresarialForm': customerempresarialForm}
    if request.method == 'POST':
        userempresarialForm = forms.CustomerEmpresarialUserForm(request.POST, instance=user)
        customerempresarialForm = forms.CustomerEmpresarialForm(request.POST, instance=customerempresarial)
        if userempresarialForm.is_valid() and customerempresarialForm.is_valid():
            user = userempresarialForm.save()
            user.set_password(user.password)
            user.save()
            customerempresarialForm.save()
            return redirect('view-customer')
    return render(request, 'ecom/admin/admin_update_clienteempresarial.html', context=mydict)

@login_required(login_url='adminlogin')
def editProduct(request, pk):
    prod = models.Product.objects.get(id=pk)

    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(prod.product_image) > 0:
                os.remove(prod.product_image.path)
            prod.product_image = request.FILES['product_image']
        prod.save()
        messages.success(request, "Product Updated Successfully")
        return redirect('admin-products')

    context = {'prod': prod}
    return render(request, 'ecom/admin/admin_actualizar_producto_imagen.html', context)

@login_required(login_url='adminlogin')
def editCliente(request, pk):
    prod = models.Customer.objects.get(id=pk)

    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(prod.profile_pic) > 0:
                os.remove(prod.profile_pic.path)
            prod.profile_pic = request.FILES['profile_pic']
        prod.address = request.POST.get('address')
        prod.movile = request.POST.get('mobile')
        prod.save()
        messages.success(request, "Product Updated Successfully")
        return redirect('view-customer')

    context = {'prod': prod}
    return render(request, 'ecom/admin/admin_actualizar_cliente_imagen.html', context)


# administrador ver el producto
@login_required(login_url='adminlogin')
def admin_products_view(request):
    products = models.Product.objects.all()

    if products.filter(stock__lte=10):
        messages.info(request, 'Cuidado el stock de algunos productos ha bajado!')

    elif products.filter(stock__gte=15):
        messages.success(request, 'Tu stock esta correcto!')
    elif products.filter(stock__exact=0):
        messages.error(request, 'El stock de tus productos se ha acabado :(')
    else:
        messages.warning(request, '¡¡Hey!!, uno de tus productos su stock se ha acabado!')
    return render(request, 'ecom/admin_products.html', {'products': products})


# admin agregue producto haciendo clic en el botón flotante
@login_required(login_url='adminlogin')
def admin_add_product_view(request):
    productForm = forms.ProductForm()
    if request.method == 'POST':
        productForm = forms.ProductForm(request.POST, request.FILES)

        if productForm.is_valid():
            productForm.save()

        return HttpResponseRedirect('admin-products')
    return render(request, 'ecom/admin_add_products.html', {'productForm': productForm})


@login_required(login_url='adminlogin')
@user_passes_test(is_administrador)
def delete_product_view(request, pk):
    product = models.Product.objects.get(id=pk)
    product.delete()
    return redirect('admin-products')


class update_product_view(UpdateView):
    model = Product
    fields = "__all__"
    template_name = 'ecom/admin_update_product.html'
    success_url = '/admin-products'

    @method_decorator(admin_required)
    def dispatch(self, request, *args, **kwargs):
        return super(update_product_view, self).dispatch(request, *args, **kwargs)



# --------------------------------------------
# ------------- ORDENES ----------------------
# --------------------------------------------

@login_required(login_url='adminlogin')
def admin_view_booking_view(request):
    producto = models.Product.objects.all()
    orders = models.Orders.objects.all().order_by('-id')
    ordered_products = []
    ultima_ordenes = []
    ordered_bys = []

    for order in orders:
        ordered_product = models.Product.objects.all().filter(id=order.product.id).order_by('-id')
        ordered_by = models.Customer.objects.all().filter(id=order.customer.id).order_by('-id')
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)
        ultima_orden = models.Customer.objects.all().filter(id=order.customer.id).order_by('-id')
        ultima_ordenes.append(ultima_orden)

    return render(request, 'ecom/admin_view_booking.html',
                  {'data': zip(ordered_products, ordered_bys, orders), "producto": producto})


@login_required(login_url='adminlogin')
def delete_order_view(request, pk):
    order = models.Orders.objects.get(id=pk)
    order.delete()
    return redirect('admin-view-booking')


# para cambiar el estado del pedido (pendiente, entregado ...)
@login_required(login_url='adminlogin')
def update_order_view(request, pk):
    order = models.Orders.objects.get(id=pk)
    orderForm = forms.OrderForm(instance=order)
    if request.method == 'POST':
        orderForm = forms.OrderForm(request.POST, instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('admin-view-booking')
    return render(request, 'ecom/update_order.html', {'orderForm': orderForm})


# administrador ver los comentarios
@login_required(login_url='adminlogin')
def view_feedback_view(request):
    feedbacks = models.Feedback.objects.all().filter(estado="Pendiente").order_by('-id')
    return render(request, 'ecom/view_feedback.html', {'feedbacks': feedbacks})


@login_required(login_url='adminlogin')
def responder_feedback_view(request, pk):
    responderFeedback = forms.ResponderFeedbackForm()
    if request.method == 'POST':
        responder = forms.ResponderFeedbackForm(request.POST)
        if responder.is_valid():
            enquiry_x = models.Feedback.objects.get(id=pk)
            enquiry_x.descripcion_solucion = responder.cleaned_data['descripcion_solucion']
            enquiry_x.estado = "Respondido"
            enquiry_x.save()
        else:
            print("El formulario es invalido")
        return HttpResponseRedirect('/view-feedback')
    return render(request, 'ecom/admin/admin_responder_feedback.html', {'responderFeedback': responderFeedback})


# ---------------------------------------------------------------------------------
# ------------------------ INICIO DE VISTAS RELACIONADAS CON CLIENTES PÚBLICOS ----
# ---------------------------------------------------------------------------------

class detalle_producto_DetailView(DetailView):
    # Detalle de producto
    model = Product

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['categoria'] = models.Categoria.objects.all()
        return context


class detalle_order_DetailView(DetailView):
    # Para ver el detalle de las ordenes
    model = Orders
    template_name = 'ecom/detalle-orden.html'


def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products = models.Product.objects.all().filter(name__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0

    # La variable de palabra se mostrará en html cuando el usuario haga clic en el botón de búsqueda
    word = "Resultados de la Busqueda :"

    if request.user.is_authenticated:
        return render(request, 'ecom/customer_home.html',
                      {'products': products, 'word': word, 'product_count_in_cart': product_count_in_cart})
    return render(request, 'ecom/index.html',
                  {'products': products, 'word': word, 'product_count_in_cart': product_count_in_cart})


def search_view_categorias(request):
    # cualquier usuario que escriba en el cuadro de búsqueda, obtenemos en la consulta
    query = request.GET['query']
    products = models.Product.objects.all().filter(categoria__categoria__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0

    # La variable de palabra se mostrará en html cuando el usuario haga clic en el botón de búsqueda
    word = "Resultados de la Busqueda :"
    categoria = models.Categoria.objects.all()
    proveedores = models.Proveedor.objects.all()
    if request.user.is_authenticated:
        return render(request, 'ecom/customer_home.html',
                      {'products': products, 'categoria': categoria, 'proveedores': proveedores, 'word': word,
                       'product_count_in_cart': product_count_in_cart})
    return render(request, 'ecom/index.html',
                  {'products': products, 'categoria': categoria, 'proveedores': proveedores, 'word': word,
                   'product_count_in_cart': product_count_in_cart})


def search_view_proveedores(request):
    # cualquier usuario que escriba en el cuadro de búsqueda, obtenemos en la consulta
    query = request.GET['query']

    products = models.Product.objects.all().filter(proveedor_id=query)

    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0

    # La variable de palabra se mostrará en html cuando el usuario haga clic en el botón de búsqueda
    word = "Resultados de la Busqueda :"
    categoria = models.Categoria.objects.all()
    proveedores = models.Proveedor.objects.all()
    if request.user.is_authenticated:
        return render(request, 'ecom/customer_home.html',
                      {'products': products, 'categoria': categoria, 'proveedores': proveedores, 'word': word,
                       'product_count_in_cart': product_count_in_cart})
    return render(request, 'ecom/index.html',
                  {'products': products, 'categoria': categoria, 'proveedores': proveedores, 'word': word,
                   'product_count_in_cart': product_count_in_cart})


# cualquiera puede agregar un producto al carrito, sin necesidad de iniciar sesión
def add_to_cart_view(request, pk):
    products = models.Product.objects.all().order_by('-id')[:12]
    # para el contador de carritos, obteniendo ID de productos agregados por el cliente desde las cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 1

    response = render(request, 'ecom/index.html',
                      {'products': products, 'product_count_in_cart': product_count_in_cart})

    # agregar ID de producto a las cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids == "":
            product_ids = str(pk)
        else:
            product_ids = product_ids + "|" + str(pk)
        response.set_cookie('product_ids', product_ids)
    else:
        response.set_cookie('product_ids', pk)

    product = models.Product.objects.get(id=pk)
    messages.info(request, product.name + ' Agregado al carro exitosamente!')

    return response


# para pagar el carrito
def cart_view(request):
    # para contador de carritos
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']

        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0
        word = "No has agregado ningun producto"

    # fetching product details from db whose id is present in cookie
    products = None
    total = 0
    descuento = 0
    word = "No has agregado ningun producto"
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']

        if product_ids != "":
            product_id_in_cart = product_ids.split('|')
            products = models.Product.objects.all().filter(id__in=product_id_in_cart)
            productos = models.Product.objects.all().filter(id__in=product_id_in_cart)
            # for total price shown in cart

            for p in products:
                if p.estado == "Agotado":
                    total = 0
                else:
                    descuento = descuento + p.product_precio_discuento
                    total = total + p.price - p.product_precio_discuento
        else:
            word = "No has agregado ningun producto"
    else:
        word = "No has agregado ningun producto"

    return render(request, 'ecom/cart.html',
                  {'products': products, 'total': total, 'descuento': descuento, 'word': word,
                   'product_count_in_cart': product_count_in_cart})


def remove_from_cart_view(request, pk):
    # for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0

    # removing product id from cookie
    total = 0
    descuento = 0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart = product_ids.split('|')
        product_id_in_cart = list(set(product_id_in_cart))
        product_id_in_cart.remove(str(pk))
        products = models.Product.objects.all().filter(id__in=product_id_in_cart)
        # for total price shown in cart after removing product
        for p in products:
            descuento = descuento + p.product_precio_discuento
            total = total + p.price - descuento

        #  for update coookie value after removing product id in cart
        value = ""
        for i in range(len(product_id_in_cart)):
            if i == 0:
                value = value + product_id_in_cart[0]
            else:
                value = value + "|" + product_id_in_cart[i]
        response = render(request, 'ecom/cart.html',
                          {'products': products, 'total': total, 'descuento': descuento,
                           'product_count_in_cart': product_count_in_cart})
        if value == "":
            response.delete_cookie('product_ids')
        response.set_cookie('product_ids', value)
        return response


def añadir_cantidad_cart_view(request, pk, price):
    if 'product_ids' in request.COOKIES:

        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0

    # removing product id from cookie
    total = 0
    descuento = 0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart = product_ids.split('|')
        product_id_in_cart = list(set(product_id_in_cart))
        product_id_in_cart.append(str(pk))
        products = models.Product.objects.all().filter(id__in=product_id_in_cart)

        # for total price shown in cart after añadir producto

        for p in products:
            if p.pk == pk:
                if p.price == price:
                    p.price += price
                    total = total + p.price

            else:

                total = total + p.price
    response = render(request, 'ecom/cart.html',
                      {'products': products, 'descuento': descuento, 'total': total,
                       'product_count_in_cart': product_count_in_cart})
    response.set_cookie('price', price)
    return response


def disminuir_cantidad_cart_view(request, pk, price):
    # for counter in cart
    if 'product_ids' in request.COOKIES:

        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))

    else:
        product_count_in_cart = 0

    # removing product id from cookie
    total = 0
    descuento = 0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']

        product_id_in_cart = product_ids.split('|')
        product_id_in_cart = list(set(product_id_in_cart))
        product_id_in_cart.remove(str(pk))
        products = models.Product.objects.all().filter(id__in=product_id_in_cart)

        # for total price shown in cart after removing product
        for p in products:
            descuento = descuento + p.product_precio_discuento
            p.price = price - p.price
            total = total + p.price - descuento

    return render(request, 'ecom/cart.html',
                  {'products': products, 'descuento': descuento, 'total': total,
                   'product_count_in_cart': product_count_in_cart})


def send_feedback_view(request):
    feedbackForm = forms.FeedbackForm()
    if request.method == 'POST':
        feedbackForm = forms.FeedbackForm(request.POST)
        if feedbackForm.is_valid():
            feedbackForm.save()
            return render(request, 'ecom/feedback_sent.html')
    return render(request, 'ecom/send_feedback.html', {'feedbackForm': feedbackForm})


# ---------------------------------------------------------------------------------
# ------------------------  INICIO DE VISTAS RELACIONADAS CON EL CLIENTE ------------------------------
# ---------------------------------------------------------------------------------

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_home_view(request):
    products = models.Product.objects.all().order_by('-id')[:12]
    categoria = models.Categoria.objects.all()
    proveedores = models.Proveedor.objects.all()
    products_slider = models.Product.objects.all().order_by('-id')
    productods_total = models.Product.objects.all()
    allProds = []
    cats = {3}
    for cat in cats:
        prod = models.Product.objects.filter()
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0
    return render(request, 'ecom/customer_home.html',
                  {'products': products, 'productods_total': productods_total, 'categoria': categoria,
                   'proveedores': proveedores, 'product_count_in_cart': product_count_in_cart, 'allProds': allProds,
                   'products_slider': products_slider})


# dirección de envío antes de realizar el pedido
@login_required(login_url='customerlogin')
def customer_address_view(request):
    # esto es para verificar si el producto está presente en el carrito o no
    # Si no hay ningún producto en el carrito, no mostraremos el formulario de dirección.
    product_in_cart = False
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_in_cart = True
    # para mostrador en carrito
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0

    CALLBACK_URL = request.build_absolute_uri(reverse("confirmar_payment"))
    contraseñapaypal = "AWbVCrW02zFBo9VMpZ0OlGNNRGMktkD92xCM4qInm0uPPKy4n8SezOpANRsxzOsahrIKvvgFeSUo9UR1"
    addressForm = forms.AddressForm()
    if request.method == 'POST':
        addressForm = forms.AddressForm(request.POST)
        if addressForm.is_valid():
            # aquí estamos tomando la dirección, el correo electrónico, el teléfono móvil al momento de realizar el pedido
            # no lo tomamos de la tabla de cuentas del cliente porque
            # estas cosas pueden ser cambios
            email = addressForm.cleaned_data['Email']
            mobile = addressForm.cleaned_data['Mobile']
            address = addressForm.cleaned_data['Address']
            dni = addressForm.cleaned_data['Dni']
            distrito = addressForm.cleaned_data['Distrito']
            localidad = addressForm.cleaned_data['localidad']

            # para mostrar el precio total en la página de pago ... acceder a la identificación de las cookies y luego obtener el precio del producto de db
            total = 0

            if 'product_ids' in request.COOKIES:
                product_ids = request.COOKIES['product_ids']
                if product_ids != "":
                    product_id_in_cart = product_ids.split('|')
                    products = models.Product.objects.all().filter(id__in=product_id_in_cart)
                    for p in products:
                        total = total + p.price

            response = render(request, 'ecom/payment.html', {'total': total, 'CALLBACK_URL': CALLBACK_URL, 'contraseña': contraseñapaypal})
            response.set_cookie('email', email)
            response.set_cookie('mobile', mobile)
            response.set_cookie('address', address)
            response.set_cookie('localidad', localidad)
            response.set_cookie('dni', dni)
            response.set_cookie('distrito', distrito)
            return response
        else:
            messages.error(request, "el telefono no es correcto")
    return render(request, 'ecom/customer_address.html',
                  {'addressForm': addressForm, 'product_in_cart': product_in_cart,'contraseña': contraseñapaypal,
                   'product_count_in_cart': product_count_in_cart})


def confirmar_payment(request):
    return render(request, 'ecom/payment_success.html')


class payment_success_view(generic.View):

    def post(self, request, *args, **kwargs):
        # Aquí haremos el pedido | después del pago exitoso
        # buscaremos el móvil del cliente, la dirección, el correo electrónico
        # Obtendremos la identificación del producto de las cookies y luego los detalles respectivos de la base de datos.
        # luego crearemos objetos de pedido y los almacenaremos en db
        # después de eso, eliminaremos las cookies porque después de realizar el pedido ... el carrito debe estar vacío
        customer = models.Customer.objects.get(user_id=request.user.id)
        products = None
        kardexs = None
        email = None
        mobile = None
        address = None
        localidad = None
        distrito = None
        dni = None

        if 'product_ids' in request.COOKIES:
            product_ids = request.COOKIES['product_ids']
            if product_ids != "":
                product_id_in_cart = product_ids.split('|')
                products = models.Product.objects.all().filter(id__in=product_id_in_cart)
                kardexs = models.Product.objects.all().filter(id__in=product_id_in_cart)
                # Aquí obtenemos una lista de productos que serán pedidos por un cliente a la vez.

        # estas cosas se pueden cambiar así que accediendo en el momento de realizar el pedido ...
        if 'email' in request.COOKIES:
            email = request.COOKIES['email']
        if 'mobile' in request.COOKIES:
            mobile = request.COOKIES['mobile']
        if 'address' in request.COOKIES:
            address = request.COOKIES['address']
        if 'localidad' in request.COOKIES:
            localidad = request.COOKIES['localidad']
        if 'distrito' in request.COOKIES:
            distrito = request.COOKIES['distrito']
        if 'dni' in request.COOKIES:
            dni = request.COOKIES['dni']

        # here we are placing number of orders as much there is a products
        # suppose if we have 5 items in cart and we place order....so 5 rows will be created in orders table
        # there will be lot of redundant data in orders table...but its become more complicated if we normalize it

        # para guardar los productos seleccionados en la tabla orden
        for product in products:
            o = models.Orders(customer=customer, product=product, status='Pendiente', email=email,
                              mobile=mobile, address=address, delivery_zona=localidad,
                              distribuidor=models.Distribuidor.objects.get(id=1), distrito=distrito,
                              dni=dni)
            o.save()

        send_email(email, distrito, address, o.id)

        # para guardar los productos seleccionados en la tabla Kardex
        for product in kardexs:
            k = models.Kardex(ingreso=0, descripcion="Reducción del producto", salida=1,
                              producto_id=product)
            k.save()

            product.stock -= 1
            product.save()

        body = json.loads(request.body)
        payment = models.Payment(
            order=o,
            succesful=True,
            raw_response=json.dumps(body),
            amount=float(body["purchase_units"][0]["amount"]["value"]),
            payment_method='Paypal'
        )

        payment.save()

        # después de realizar el pedido, las cookies deben eliminarse
        response = HttpResponseRedirect('confirmar_payment')

        response.delete_cookie('product_ids')
        response.delete_cookie('email')
        response.delete_cookie('mobile')
        response.delete_cookie('address')
        response.delete_cookie('localidad')
        response.delete_cookie('distrito')
        response.delete_cookie('dni')
        return response


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_order_view(request):
    categorias = models.Categoria.objects.all()
    product_in_cart = False
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_in_cart = True
    # para mostrador en carrito
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0
    customer = models.Customer.objects.get(user_id=request.user.id)
    orders = models.Orders.objects.all().filter(customer_id=customer).order_by('-id')[:6]
    ordered_products = []
    for order in orders:
        ordered_product = models.Product.objects.all().filter(id=order.product.id)
        ordered_products.append(ordered_product)

    return render(request, 'ecom/my_order.html',
                  {'data': zip(ordered_products, orders, ), "product_count_in_cart": product_count_in_cart,
                   "categoria": categorias})


# --------------para descargar e imprimir la factura del paciente al alta (pdf)
import io
from xhtml2pdf import pisa
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def download_invoice_view(request, orderID, productID):
    order = models.Orders.objects.get(id=orderID)
    product = models.Product.objects.get(id=productID)
    mydict = {
        'orderDate': order.order_date,
        'customerName': request.user,
        'customerEmail': order.email,
        'customerMobile': order.mobile,
        'shipmentAddress': order.address,
        'orderStatus': order.status,

        'productName': product.name,
        'productImage': product.product_image,
        'productPrice': product.price,
        'productDescription': product.description,

    }
    return render_to_pdf('ecom/download_invoice.html', mydict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_profile_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    return render(request, 'ecom/my_profile.html', {'customer': customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_profile_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    user = models.User.objects.get(id=customer.user_id)
    userForm = forms.CustomerUserForm(instance=user)
    customerForm = forms.CustomerForm(request.FILES, instance=customer)
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST, instance=user)
        customerForm = forms.CustomerForm(request.POST, instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('my-profile')
    return render(request, 'ecom/edit_profile.html', context=mydict)


# ---------------------------------------------------------------------------------
# ------------------------ ABOUT US AND CONTACT US VIEWS START --------------------
# ---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request, 'ecom/aboutus.html')


def contactus_view(request):

    if request.method == 'POST':
        mail= request.POST.get('gmail')
        nombre =request.POST.get('nombre')
        celular = request.POST.get('celular')
        mensaje = request.POST.get('mensaje')
        send_email_contacto(mail=mail,nombre=nombre, celular=celular, mensaje=mensaje)
        return HttpResponseRedirect('/')
    return render(request, 'ecom/contactus.html')


from django.conf import settings
from django.shortcuts import render
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


def send_email(mail, distrito, address, orden):
    context = {'mail': mail, 'distrito': distrito, 'direccion': address, 'orden': orden}
    template = get_template('ecom/correo.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Mensaje de Empresa Ikergust',
        'Venta realizada',
        settings.EMAIL_HOST_USER,
        [mail],

    )

    email.attach_alternative(content, 'text/html')
    email.send()


def send_email_contacto(mail, nombre, celular, mensaje):
    context = {'mail': mail, 'nombre': nombre, 'celular': celular, 'mensaje': mensaje}
    template = get_template('ecom/email.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Mensaje de Empresa Ikergust',
        'Venta realizada',
         mail,
        ['gakdo4157@gmail.com'],

    )

    email.attach_alternative(content, 'text/html')
    email.send()

class send_feedback_view(View):

    def get(self, request, *args, **kwargs):
        a = Product.objects.all()

        product_in_cart = False
        if 'product_ids' in request.COOKIES:
            product_ids = request.COOKIES['product_ids']
            if product_ids != "":
                product_in_cart = True
        # para mostrador en carrito
        if 'product_ids' in request.COOKIES:
            product_ids = request.COOKIES['product_ids']
            counter = product_ids.split('|')
            product_count_in_cart = len(set(counter))
        else:
            product_count_in_cart = 0

        return render(request, "ecom/send_feedback.html", {"a": a, "product_count_in_cart": product_count_in_cart})

    def post(self, request, *args, **kwargs):
        usuario = request.POST.get("usuario")
        name = request.POST.get("nombre")
        tipoproblema = request.POST.get("tipoproblema")
        feedback = request.POST.get("feedback")

        user = models.User.objects.get(id=usuario)

        feedback = models.Feedback(user=user, name=name, feedback=feedback,
                                   descripcion_solucion="", estado="Pendiente", tipo=tipoproblema)
        feedback.save()
        return render(request, "ecom/send_feedback.html")


#####################################
#             ADMIN  KARDEX       ####
#####################################
def kardex_opciones(request):
    kardex = models.Kardex.objects.all()
    return render(request, 'ecom/admin/admin_opcionKardex.html', {"kardex": kardex})


class buscar_producto_kardex(View):

    @method_decorator(admin_required)
    def dispatch(self, request, *args, **kwargs):
        return super(buscar_producto_kardex, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        categoria = models.Categoria.objects.all()
        return render(request, "ecom/admin/Buscar_producto_kardex.html", {"categoria": categoria})

    def post(self, request, *args, **kwargs):
        categorias = models.Categoria.objects.all()
        productos = models.Product.objects.all()
        categoria = request.POST.get("categoria")
        cat = models.Categoria.objects.get(id=categoria)
        produc = []
        for p in productos:
            produc = models.Product.objects.all().filter(categoria_id=cat)

        return render(request, "ecom/admin/Buscar_producto_kardex.html", {"productos": produc, "categoria": categorias})


def Actualizar_producto_kardex_view(request, pk):
    if request.method == "GET":
        producto_id = models.Product.objects.get(id=pk)
        return render(request, 'ecom/admin/admin_kardex_añadirstock.html', {'producto': producto_id})

    elif request.method == "POST":
        pk = request.POST.get("id_producto")
        stock = request.POST.get("stock")
        producto_id = models.Product.objects.get(id=pk)
        producto_id.stock = int(stock) + producto_id.stock
        producto_id.save()
        kardex = models.Kardex(ingreso=stock, descripcion="Aumento del producto", salida=0, producto_id=producto_id)
        kardex.save()
        categoria = models.Categoria.objects.all()

        return render(request, 'ecom/admin/Buscar_producto_kardex.html', {"categoria": categoria})


def kardex_view(request):
    kardex = models.Kardex.objects.all().order_by('-id')[:10]
    return render(request, 'ecom/admin/admin_kardex.html', {"kardex": kardex})


def admin_distribuidor(request):
    ordenes = models.Orders.objects.all().filter(status="Pendiente")
    return render(request, 'ecom/admin/admin_distribuidor.html', {"ordenes": ordenes})


def admin_distribuidor_agregar(request):
    customerForm = forms.CustomerForm()
    mydict = {'customerForm': customerForm}
    if request.method == 'POST':
        usuario = request.POST.get("usuario")
        contrasena = request.POST.get("contraseña")
        nombres = request.POST.get("nombres")
        apellidos = request.POST.get("apellidos")
        customerForm = forms.CustomerForm(request.POST, request.FILES)
        if customerForm.is_valid():
            user = models.User(username=usuario, password=contrasena, first_name=nombres, last_name=apellidos)
            user.set_password(user.password)
            user.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='DISTRIBUIDOR')
            my_customer_group[0].user_set.add(user)
            Token.objects.create(user=user)

        return HttpResponseRedirect('customerlogin')
    return render(request, 'ecom/customersignup.html', context=mydict)


#####################################
#             ADMIN  PAQUETES      ####
#####################################
def Paquete_opciones(request):
    return render(request, 'ecom/admin/admin_opcionpaquetes.html')


#####################################
#             ERRORES      ####
#####################################
class Error404(TemplateView):
    template_name = 'ecom/error404.html'


def error_404_view(request, exception):
    return render(request,'ecom/error404.html')

def handler500(request, *args, **argv):
    return render(request, 'ecom/error404.html', status=500)

def handler400(request, *args, **argv):
    return render(request, 'ecom/error400.html', status=400)

