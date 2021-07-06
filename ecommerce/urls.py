from django.contrib import admin
from django.urls import path
from ecom import views
from ecom.categoria import view_categoria
from ecom.proveedor import view_proveedor
from ecom.servicios import view_servicio_rest
from ecom.paquetes import view_paquete
from ecom.customer_empresarial import view_customerempresarial
from ecom.distribuidor import view_distribuidor
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name=''),
    path('detalle-producto/<int:pk>/', views.detalle_producto_DetailView.as_view(), name='detalle-producto'),
    path('detalle-orden/<int:pk>/', views.detalle_order_DetailView.as_view(), name='detalle-orden'),

    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='ecom/logout.html'), name='logout'),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view, name='contactus'),
    path('search', views.search_view, name='search'),
    path('search_categoria', views.search_view_categorias, name='search_categoria'),
    path('search_proveedores', views.search_view_proveedores, name='search_proveedores'),
    path('send-feedback', views.send_feedback_view.as_view(), name='send-feedback'),
    path('buscar-categoria-kardex', views.buscar_producto_kardex.as_view(), name='buscar-categoria-kardex'),

    path('view-feedback', views.view_feedback_view, name='view-feedback'),
    path('responder_feedback_view/<int:pk>/', views.responder_feedback_view, name='responder_feedback_view'),
    path('Actualziar-cantidad-producto/<int:pk>/', views.Actualizar_producto_kardex_view, name='Actualziar-cantidad-producto'),
    path('kardex-view', views.kardex_view, name='kardex-view'),
    path('kardex_opciones', views.kardex_opciones, name='kardex_opciones'),
    path('Paquetes_opciones', views.Paquete_opciones, name='Paquetes_opciones'),
    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='ecom/adminlogin.html'), name='adminlogin'),

    # dashboards
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
    path('data', views.pivot_data, name='pivot_data'),
    path('dashboard_general', views.dashboard_with_pivot, name='dashboard_with_pivot'),
    path('admin-dashboard_detalle', views.admin_dashboard_detalle, name='admin-dashboard_detalle'),
    path('admin_fecha_ordenes', views.admin_fecha_ordenes.as_view(), name='admin_fecha_ordenes'),
    path('admin_pagos', views.admin_pagos_view, name='admin_pagos'),




    path('paquete', view_paquete.paquetes, name='paquete'),
    path('view-customer', views.view_customer_view, name='view-customer'),
    path('Ver-paquete', view_paquete.paquete_view.as_view(), name='Ver-paquete'),
    path('Actualizar-paquete/<slug:pk>/', view_paquete.Actualizar_paquete.as_view(), name='Actualizar-paquete'),

    path('Agregar-paquete', view_paquete.Agregar_paquete_view.as_view(), name='Agregar-paquete'),
    path('Asignar-distribuidor/<int:pk>/', view_distribuidor.Asignar_Distribuidor_entrega_view, name='Asignar-distribuidor'),

    path('delete-customer/<int:pk>', views.delete_customer_view, name='delete-customer'),
    path('delete-customerempresarial/<int:pk>', views.delete_customerempresarial_view, name='delete-customerempresarial'),
    path('update-customer/<int:pk>', views.update_customer_view, name='update-customer'),
    path('editCliente/<int:pk>', views.editCliente, name='editCliente'),
    path('editProduct/<int:pk>', views.editProduct, name='editProduct'),
    path('update-customerempresarial/<int:pk>', views.update_customerempresarial_view, name='update-customerempresarial'),

    path('admin_distribuidor', views.admin_distribuidor, name='admin_distribuidor'),
    path('admin-products', views.admin_products_view, name='admin-products'),
    path('admin-add-product', views.admin_add_product_view, name='admin-add-product'),
    path('delete-product/<int:pk>', views.delete_product_view, name='delete-product'),
    path('update-product/<int:pk>', views.update_product_view, name='update-product'),

    path('admin-view-booking', views.admin_view_booking_view, name='admin-view-booking'),
    path('delete-order/<int:pk>', views.delete_order_view, name='delete-order'),
    path('update-order/<int:pk>', views.update_order_view, name='update-order'),

    path('customersignup', views.customer_signup_view),
    path('eleccion-registro', views.eleccion_registro_view, name='eleccion-registro'),

    path('customerempresarialsignup', view_customerempresarial.customer_empresarial_singup.as_view()),
    path('customerlogin', LoginView.as_view(template_name='ecom/customerlogin.html'), name='customerlogin'),
    path('distribuidorlogin', LoginView.as_view(template_name='ecom/distribuidor/distribuidorlogin.html'), name='distribuidorlogin'),
    path('customerempresariallogin', LoginView.as_view(template_name='ecom/customerlogin.html'), name='customerempresariallogin'),

    path('customer-home', views.customer_home_view, name='customer-home'),
    path('distribuidor-home', view_distribuidor.distribuidor_home_view, name='distribuidor-home'),
    path('customerempresarial-home', view_customerempresarial.customerempresarial_home_view, name='customer-empresarial-home'),

    path('my-order', views.my_order_view, name='my-order'),
    path('my-profile', views.my_profile_view, name='my-profile'),
    path('edit-profile', views.edit_profile_view, name='edit-profile'),
    path('download-invoice/<int:orderID>/<int:productID>', views.download_invoice_view, name='download-invoice'),

    path('add-to-cart/<int:pk>', views.add_to_cart_view, name='add-to-cart'),
    path('cart', views.cart_view, name='cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart_view, name='remove-from-cart'),
    path('añadir_cantidad_cart_view/<int:pk>/<int:price>/', views.añadir_cantidad_cart_view,
         name='añadir_cantidad_cart_view'),
    path('disminuir_cantidad_cart_view/<int:pk>/<int:price>/', views.disminuir_cantidad_cart_view,
         name='disminuir_cantidad_cart_view'),
    path('customer-address', views.customer_address_view, name='customer-address'),
    path('confirmar_payment', views.confirmar_payment, name='confirmar_payment'),

    path('payment-success', views.payment_success_view.as_view(), name='payment-success'),
    path('prueba', views.prueba, name='prueba'),
    path('prueba2', views.prueba2, name='prueba2'),

    # Django Ajax CRUD Operaciones Categoria
    path('categoria_admin/', view_categoria.CrudView.as_view(), name='crud_ajax'),
    path('ajax/crud/create/', view_categoria.CreateCrudUser.as_view(), name='crud_ajax_create'),
    path('ajax/crud/delete/', view_categoria.DeleteCrudUser.as_view(), name='crud_ajax_delete'),
    path('ajax/crud/update/', view_categoria.UpdateCrudUser.as_view(), name='crud_ajax_update'),

    # Django Ajax CRUD Operaciones Proveedor
    path('admin_proveedor/', view_proveedor.CrudView_Proveedor.as_view(), name='crud_ajax_proveedor'),
    path('ajax/crud/create_proveedor/', view_proveedor.CreateCrudUser_proveedor.as_view(),
         name='crud_ajax_create_proveedor'),
    path('ajax/crud/delete_proveedor/', view_proveedor.DeleteCrudUser_proveedor.as_view(),
         name='crud_ajax_delete_proveedor'),
    path('ajax/crud/update_proveedor/', view_proveedor.UpdateCrudUser_proveedor.as_view(),
         name='crud_ajax_update_proveedor'),






    path('api/products/', view_servicio_rest.ProductView.as_view()),
    path('api/crearproducts/', view_servicio_rest.ProductoCreateApi.as_view()),
    path('api/crud/', view_servicio_rest.CRUCAPIView.as_view()),
    path('api/updateproducts/<int:pk>/', view_servicio_rest.ProductoUpdateApi.as_view(), name='updateproducts'),
    path('api/deleteproducts/<int:pk>/', view_servicio_rest.ProductoDeleteApi.as_view(), name='deleteproducts'),
    path('api/login/', obtain_auth_token),
    path('api/register/', view_servicio_rest.RegisterView.as_view()),


]

