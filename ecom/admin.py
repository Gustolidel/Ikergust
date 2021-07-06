from django.contrib import admin
from .models import Customer,Product,Paquete,Orders,Feedback, Categoria, Proveedor, Kardex, CustomerEmpresarial, Distribuidor
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customer, CustomerAdmin)

class CustomerEmpresarialAdmin(admin.ModelAdmin):
    pass
admin.site.register(CustomerEmpresarial, CustomerEmpresarialAdmin)

class DistribuidorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Distribuidor, DistribuidorAdmin)

class KardexAdmin(admin.ModelAdmin):
    pass
admin.site.register(Kardex, KardexAdmin)

class PaqueteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Paquete, PaqueteAdmin)



class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)

admin.site.register(Categoria)

admin.site.register(Proveedor)



class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Orders, OrderAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    pass
admin.site.register(Feedback, FeedbackAdmin)
# Register your models here.
