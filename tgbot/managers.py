from django.db.models import Manager


class CategoryManager(Manager):

    def get_parent_categories(self, lvl=0):
        return self.get_queryset().filter(is_active=True, level=lvl)
    
    
    def sub_ctg(self, id):
        return self.get_queryset().filter(is_active=True, parent_id=id)