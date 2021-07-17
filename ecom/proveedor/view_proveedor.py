from django.shortcuts import redirect
from django.views.generic import View, CreateView, TemplateView
from django.http import JsonResponse
from ecom.models import Proveedor

from django.utils.decorators import method_decorator


def admin_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.groups.filter(name='Administrador').exists():
            return redirect('')
        return function(request, *args, **kwargs)
    return wrap

class CrudView_Proveedor(TemplateView):
    template_name = 'ecom/admin_proveedor.html'

    @method_decorator(admin_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CrudView_Proveedor, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = Proveedor.objects.all()
        return context




class CreateCrudUser_proveedor(View):

    @method_decorator(admin_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateCrudUser_proveedor, self).dispatch(request, *args, **kwargs)

    def  get(self, request):
        name1 = request.GET.get('proveedor_nombre', None)
        direccion = request.GET.get('direccion', None)
        telefono = request.GET.get('telefono', None)

        obj = Proveedor.objects.create(
            proveedor_nombre=name1,
            direccion = direccion,
            telefono = telefono)

        user = {'id':obj.id,'proveedor_nombre':obj.proveedor_nombre,'direccion':obj.direccion,'telefono':obj.telefono}

        data = {
            'user': user
        }
        return JsonResponse(data)

class DeleteCrudUser_proveedor(View):

    @method_decorator(admin_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteCrudUser_proveedor, self).dispatch(request, *args, **kwargs)

    def  get(self, request):
        id1 = request.GET.get('id', None)
        Proveedor.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class UpdateCrudUser_proveedor(View):

    @method_decorator(admin_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateCrudUser_proveedor, self).dispatch(request, *args, **kwargs)

    def  get(self, request):
        id1 = request.GET.get('id', None)
        name1 = request.GET.get('proveedor_nombre', None)
        direccion1 = request.GET.get('direccion', None)
        telefono1 = request.GET.get('telefono', None)


        obj = Proveedor.objects.get(id=id1)
        obj.proveedor_nombre = name1
        obj.direccion = direccion1
        obj.telefono = telefono1
        obj.save()

        user = {'id':obj.id,'proveedor_nombre':obj.proveedor_nombre,'direccion':obj.direccion,'telefono':obj.telefono}

        data = {
            'user': user
        }
        return JsonResponse(data)

