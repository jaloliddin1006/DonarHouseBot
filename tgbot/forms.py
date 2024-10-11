from django.forms import ModelForm
from tgbot.models import Product, Category

class ProductAdminForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter categories to show only leaf nodes (categories without children)
        print(list(Product.objects.get_ctg_products(8)))
        self.fields['category'].queryset = Category.objects.filter(children__isnull=True)
        
        
# [{'id': 6, 'created_at': datetime.datetime(2024, 10, 11, 14, 51, 51, 354602, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 10, 11, 14, 51, 51, 354602, tzinfo=datetime.timezone.utc), 'is_active': True, 'name': 'Pepsi, 0.5L', 'category_id': 8, 'price': Decimal('11000.00'), 'image': 'products/pepsi-05l.jpg', 'description': 'Pepsi, 0.5L', 'discount': 0}, 
#  {'id': 7, 'created_at': datetime.datetime(2024, 10, 11, 14, 52, 30, 55361, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 10, 11, 14, 52, 30, 55361, tzinfo=datetime.timezone.utc), 'is_active': True, 'name': 'Pepsi, 1.5L', 'category_id': 8, 'price': Decimal('21000.00'), 'image': 'products/Pepsi_1.5L.jpg', 'description': 'Pepsi lazzatbaxsh sovuq salqinligidan rohatlaning\r\nMiqdorini tanlang yoki kiriting', 'discount': 0}]


# [{'id': 6, 'created_at': datetime.datetime(2024, 10, 11, 14, 51, 51, 354602, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 10, 11, 14, 51, 51, 354602, tzinfo=datetime.timezone.utc), 'is_active': True, 'name': 'Pepsi, 0.5L', 'category_id': 8, 'price': Decimal('11000.00'), 'image': 'products/pepsi-05l.jpg', 'description': 'Pepsi, 0.5L', 'discount': 0}, 
#  {'id': 7, 'created_at': datetime.datetime(2024, 10, 11, 14, 52, 30, 55361, tzinfo=datetime.timezone.utc), 'updated_at': datetime.datetime(2024, 10, 11, 14, 52, 30, 55361, tzinfo=datetime.timezone.utc), 'is_active': True, 'name': 'Pepsi, 1.5L', 'category_id': 8, 'price': Decimal('21000.00'), 'image': 'products/Pepsi_1.5L.jpg', 'description': 'Pepsi lazzatbaxsh sovuq salqinligidan rohatlaning\r\nMiqdorini tanlang yoki kiriting', 'discount': 0}]