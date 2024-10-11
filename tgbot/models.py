from django.db import models
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from tgbot.managers import CategoryManager

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class User(BaseModel):
    telegram_id = models.PositiveBigIntegerField(unique=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=128, null=True)
    language_code = models.CharField(max_length=10, null=True, default="uz")
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "telegram_users"


class BotAdmin(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            pass
        super(BotAdmin, self).save(*args, **kwargs)
        
    class Meta:
        db_table = "bot_admins"


class About(BaseModel):
    description = RichTextField(verbose_name="Tavsif")

    def __str__(self):
        return self.description

    class Meta:
        db_table = "about"


class Branch(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Filial nomi")
    phone = models.CharField(max_length=50, verbose_name="Telefon raqami")
    address = models.TextField(verbose_name="Manzil")
    location = models.CharField(max_length=255, verbose_name="Lokatsiya (Yandex Maps Link)")
    working_hours = models.CharField(max_length=255, verbose_name="Ish vaqtlari")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "branches"


class Category(MPTTModel, BaseModel):
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib Raqami")
    name = models.CharField(max_length=255, verbose_name="Kategoriya nomi")
    image = models.ImageField(upload_to='categories', null=True, blank=True, verbose_name="Rasm")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    objects = CategoryManager()
    
    class Meta:
        db_table = "categories"
        
    def __str__(self):
        return self.name
    


class Product(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, verbose_name="Kategoriya", related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    image = models.ImageField(upload_to='products', null=True, blank=True, verbose_name="Rasm")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")
    discount = models.PositiveIntegerField(default=0, verbose_name="Chegirma (%)")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "products"


class Order(BaseModel):
    ORDER_STATUSES = (
        ("active", "Active"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    )
    DELIVERY_TYPES = (
        ("pickup", "Borib olish"),
        ("delivery", "Yetkazish"),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    delivery = models.CharField(max_length=50, choices=DELIVERY_TYPES, default="pickup")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, related_name="orders")
    address = models.TextField(verbose_name="Manzil", null=True, blank=True)
    location = models.CharField(max_length=255, verbose_name="Lokatsiya (Yandex Maps Link)", null=True, blank=True)
    full_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=ORDER_STATUSES, default="active")
    is_paid = models.BooleanField(default=False)
    total_paid_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    

    class Meta:
        db_table = "orders"

    def __str__(self):
        return f"{self.full_name} - {self.status}"
        
    def save(self, *args, **kwargs):
        if not self.pk and not self.full_name:
            self.full_name = self.user.full_name
        
        if not self.location and self.address==self.user.address:
            self.location = self.user.location
        super(Order, self).save(*args, **kwargs)
    
    @property
    def total_price(self):
        return sum([item.total_price for item in self.items.all()])


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product} - {self.quantity}"

    class Meta:
        db_table = "order_items"
    
    @property
    def total_price(self):
        return self.product.price * self.quantity


class PromoCodes(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif (ixtiyoriy)")
    discount = models.PositiveIntegerField(default=0, verbose_name="Chegirma (-so'mda)")
    start_time = models.DateTimeField(auto_now=True, verbose_name="Chegirmaning boshlanish vaqti")
    end_time = models.DateTimeField(verbose_name="Chegirmaning tugash vaqti")
    
    def __str__(self):
        return self.code

    class Meta:
        db_table = "promo_codes"