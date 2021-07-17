from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, TemplateView
from django.http import JsonResponse
from ecom.models import Categoria

from django.utils.decorators import method_decorator


def admin_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.groups.filter(name='Administrador').exists():
            return redirect('')
        return function(request, *args, **kwargs)

    return wrap

class CrudView(TemplateView):
    template_name = 'ecom/admin_categoria.html'


    @method_decorator(admin_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CrudView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = Categoria.objects.all()
        context['categorias'] = Categoria.objects.all().count()
        return context

    def get_object(self, **kwargs):
        assignment = Categoria.objects.all()
        return assignment


class CreateCrudUser(View):


    @method_decorator(admin_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateCrudUser, self).dispatch(request, *args, **kwargs)


    def  get(self, request):
        name1 = request.GET.get('Categoria', None)


        obj = Categoria.objects.create(
            categoria = name1,

        )

        user = {'id':obj.id,'Categoria':obj.categoria}

        data = {
            'user': user
        }
        return JsonResponse(data)

class DeleteCrudUser(View):

    @method_decorator(admin_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteCrudUser, self).dispatch(request, *args, **kwargs)


    def  get(self, request):
        id1 = request.GET.get('id', None)
        Categoria.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class UpdateCrudUser(View):

    @method_decorator(admin_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateCrudUser, self).dispatch(request, *args, **kwargs)

    def  get(self, request):
        id1 = request.GET.get('id', None)
        name1 = request.GET.get('Categoria', None)


        obj = Categoria.objects.get(id=id1)
        obj.categoria = name1
        obj.save()

        user = {'id':obj.id,'Categoria':obj.categoria}

        data = {
            'user': user
        }
        return JsonResponse(data)

