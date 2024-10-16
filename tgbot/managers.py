from django.db.models import Manager
from django.db.models import F, ExpressionWrapper, DecimalField

class CategoryManager(Manager):

    def get_parent_categories(self, lvl=0):
        return self.get_queryset().filter(is_active=True, level=lvl)
    
    
    def sub_ctg(self, id):
        return self.get_queryset().filter(is_active=True, parent_id=id)
    
    
    
class ProductManager(Manager):
    def get_ctg_products(self, category_id):
        return (self.get_queryset().filter(is_active=True, category_id=category_id).select_related('category','category__parent')
                    .values('id', 'name', 'price', 'image', 'description', 'discount', 'category__name','category_id', 'category__level', 'category__parent_id', )
        )
        
class OrderItemManager(Manager):
    def items(self, cart_id):
        return (self.get_queryset().filter(order_id=cart_id).select_related('product').prefetch_related('items')
                    .values('id', 'product__name', 'product__price', 'product__image', 'product__description', 'quantity')
                    .annotate(
                        total_price=ExpressionWrapper(
                            F('product__price') * F('quantity'),
                            output_field=DecimalField(),
                        ))
        )

class OrderManager(Manager):
    def user_active_order(self, user):
        # First, get the last active order
        last_order = self.get_queryset().filter(user=user, status="active").last()
        print(last_order)
        if last_order:
            # Fetch related items without total_price since it's a computed field
            return (self.get_queryset().filter(pk=last_order.pk)
                    .prefetch_related('items')
                    .values('id', 'status', 'delivery', 'items__id', 'items__product__name', 'items__product__price', 'items__quantity'))
        return None
    
    def get_full_order(self, id):
        order_full = (self.get_queryset().filter(id=id)
                      .select_related('branch')
                      .values('id', 'location', 'full_name', 'phone', 'address', 'addention', 'delivery', 'status', 'branch__name', 'branch__location'))
        return order_full
        