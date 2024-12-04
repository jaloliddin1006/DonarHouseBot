from modeltranslation.translator import register, TranslationOptions
from .models import About, Branch, Category, Product

@register(About)
class AboutTranslationOptions(TranslationOptions):
    fields = ('description', )

@register(Branch)
class BranchTranslateOptions(TranslationOptions):
    fields = ('name', 'address')

@register(Category)
class CategoryTranslateOptions(TranslationOptions):
    fields = ('name', 'description')
    
@register(Product)
class ProductTranslateOptions(TranslationOptions):
    fields = ('name', 'description')
    