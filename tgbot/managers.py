from django.db.models import Manager


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