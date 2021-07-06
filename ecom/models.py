from django.contrib.auth.decorators import login_required
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User, Group
from cloudinary.models import CloudinaryField
# Create your models here.


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True,default="static/default.png")
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return str(self.user)

class Distribuidor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DistribuidorProfilePic/',null=True,blank=True,default="static/default.png")
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return str(self.user)

class CustomerEmpresarial(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    ruc = models.CharField(max_length=80)
    razonsocial = models.CharField(max_length=300)
    estado = models.CharField(max_length=20)
    condicion = models.CharField(max_length=20)
    direccion = models.CharField(max_length=30)
    departamento = models.CharField(max_length=20)
    provincia= models.CharField(max_length=20)
    distrito =  models.CharField(max_length=20)
    ubigeo = models.CharField(max_length=20)
    capital = models.CharField(max_length=100)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id


    def __str__(self):
        return str(self.user)

class Proveedor(models.Model):
    telefono =  models.IntegerField( validators=[
           MinValueValidator(0),
            MaxValueValidator(999999999)
        ])

    direccion= models.CharField(max_length=40)
    proveedor_nombre= models.CharField(max_length=40)

    def __str__(self):
        return self.proveedor_nombre

class Categoria(models.Model):
    categoria = models.CharField(max_length=40)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.categoria


class Product(models.Model):
    ESTADO = (
        ('Oferta', 'Oferta'),
        ('Disponible', 'Disponible'),
        ('Agotado', 'Agotado'),
    )
    name=models.CharField(max_length=300)
    product_image= CloudinaryField('image')
    codigo_fabrica = models.CharField(max_length=50, null=True)
    price = models.IntegerField()
    description=models.CharField(max_length=300)
    garantia = models.CharField(max_length=50, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE,null=True)
    marca =models.CharField(max_length=40)
    stock = models.IntegerField( validators=[
           MinValueValidator(0)
        ])
    estado = models.CharField(max_length=50,null=True,choices=ESTADO)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True)
    product_precio_discuento = models.IntegerField()

    def _get_total(self):
        return "{:.2f}".format(self.price - self.product_precio_discuento /1)
    total = property(_get_total)

    @property
    def get_price(self):
        return "{:.2f}".format(self.price / 1)


    def __str__(self):
        return self.name

class ProductDetails(models.Model):

    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    title_details=models.CharField(max_length=255)
    is_active=models.IntegerField(default=1)


class Orders(models.Model):
    STATUS =(
        ('Pendiente','Pendiente'),
        ('Orden Confirmada','Orden Confirmada'),
        ('Fuera para entregar','Fuera para entregar'),
        ('Entregada','Entregada'),
    )

    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    product=models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=20,null=True)
    order_date= models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)
    delivery_zona = models.CharField(max_length=40)
    distrito= models.CharField(max_length=40)
    dni= models.CharField(max_length=9)
    distribuidor=models.ForeignKey(Distribuidor, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_producto(self):
        return self.product.name

    @property
    def get_cliente(self):
        return self.customer.user.first_name + " " + self.customer.user.last_name

    @property
    def get_direccion(self):
        return self.address + " (" + self.distrito + ") "

    @property
    def get_precio(self):
        return self.product.price


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    tipo = models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    descripcion_solucion = models.CharField(max_length=300)
    estado = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Kardex(models.Model):
    producto_id = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
    descripcion=models.CharField(max_length=200)
    ingreso = models.IntegerField(validators=[
        MinValueValidator(0)
    ])
    salida = models.IntegerField(validators=[
        MinValueValidator(0)
    ])
    dia = models.DateField(auto_now_add=True, null=True)
    hora = models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.descripcion

class Paquete(models.Model):
    producto_id = models.ManyToManyField(Product)
    titulo = models.CharField(max_length=100)
    precio = models.IntegerField(validators=[
        MinValueValidator(0)
    ])
    paquete_imagen = models.ImageField(upload_to='paquete_image/',null=True,blank=True,default="static/paquete.png")

    def __str__(self):
        return str(self.id)



class Payment(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=(
        ('Paypal','Paypal'),
    ))
    timestamp = models.DateTimeField(auto_now_add=True,null=True)
    succesful = models.BooleanField(default=False)
    amount = models.FloatField()
    raw_response = models.TextField()

    def __str__(self) :
        return self.reference_number

    @property
    def reference_number(self):
        return f"PAYMENT-{self.order}-{self.pk}"
