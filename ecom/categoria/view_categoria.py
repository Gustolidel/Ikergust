from django.shortcuts import render
from django.views.generic import View, CreateView, TemplateView
from django.http import JsonResponse
from ecom.models import Categoria


class CrudView(TemplateView):
    template_name = 'ecom/admin_categoria.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = Categoria.objects.all()
        context['categorias'] = Categoria.objects.all().count()
        return context

    def get_object(self, **kwargs):
        assignment = Categoria.objects.all()
        return assignment


class CreateCrudUser(View):
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
    def  get(self, request):
        id1 = request.GET.get('id', None)
        Categoria.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class UpdateCrudUser(View):
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

