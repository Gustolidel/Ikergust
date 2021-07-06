from django.contrib.auth.decorators import login_required, user_passes_test
from ecom.views import is_distribuidor
from django.shortcuts import render, redirect
from ecom import forms, models

#----------------------------------------------------------------------------------
#------------------------- COLABORADOR DISTRIBUIDOR ------------------------------------------
#----------------------------------------------------------------------------------

@login_required(login_url='distribuidorlogin')
@user_passes_test(is_distribuidor)
def distribuidor_home_view(request):
    id_distribuidor= models.User.objects.get(username=request.user.username)
    entregas = models.Orders.objects.filter(distribuidor=id_distribuidor)

    return render(request, 'ecom/distribuidor/distribuidor_home.html',{"entregas":entregas})


def Asignar_Distribuidor_entrega_view(request,pk):

    if request.method == 'GET':
        orden_id = models.Orders.objects.get(id=pk)
        distribuidores = models.Distribuidor.objects.all()
        return render(request, "ecom/distribuidor/Asignar_Distribuidor_entrega.html",{"di":distribuidores, "orden_id":orden_id})

    elif request.method == "POST":
        pk = request.POST.get("orden_id")

        distribuidor_id = request.POST.get("distribuidor_id")
        distribuidor = models.User.objects.get(id=distribuidor_id)

        orden_id = models.Orders.objects.get(id=pk)
        orden_id.distribuidor = distribuidor
        orden_id.save()
        ordenes = models.Orders.objects.all().filter(status="Pendiente")
        return render(request, 'ecom/admin/admin_distribuidor.html',{"ordenes":ordenes})