from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin
from tgbot.models import User as TelegramUser, BotAdmin, Category, Product, About, Branch, Order, OrderItem


@admin.register(TelegramUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "username", "telegram_id", 'is_active')
    fields = ("full_name", "username", "telegram_id", )
    search_fields = ("full_name", "username", "telegram_id", )
    list_per_page = 50


@admin.register(BotAdmin)
class BotAdminsAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'user', 'is_active', 'created_at', 'account')
    list_editable = ('is_active',)
    list_display_links = ('id', 'telegram_id')

    def telegram_id(self, obj):
        return str(obj.user.telegram_id)
    
    def account(self, obj):
        return format_html(f'<button><a class="button" href="https://t.me/{obj.user.username}">View Telegram</a></bitton>'  )
    account.short_description = 'Account'
    account.allow_tags = True
    
    

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    # 'related_products_count', 'related_products_cumulative_count'
                    )
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # # Add cumulative product count
        # qs = Category.objects.add_related_count(
        #         qs,
        #         Product,
        #         'category',
        #         'products_cumulative_count',
        #         cumulative=True)

        # # Add non cumulative product count
        # qs = Category.objects.add_related_count(qs,
        #          Product,
        #          'categories',
        #          'products_count',
        #          cumulative=False)
        return qs

    # def related_products_count(self, instance):
    #     return instance.products_count
    # related_products_count.short_description = 'Related products (for this specific category)'

    # def related_products_cumulative_count(self, instance):
    #     return instance.products_cumulative_count
    # related_products_cumulative_count.short_description = 'Related products (in tree)'
    
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'is_active')
    list_editable = ('is_active',)
    list_display_links = ('id', 'name')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'is_active')
    list_per_page = 50
    list_select_related = ('category',)
    ### TO DO: Kategoriyalarni childrenlarini ko'rsatish kerak
    
    
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'about', 'is_active')
    
    def about(self, obj):
        return format_html(obj.description)
    about.short_description = 'Donar House haqida'

    
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'address', 'working_hours', 'is_active')
    list_editable = ('is_active',)
    list_display_links = ('id', 'name')
    list_per_page = 50
    

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'total_price')
    readonly_fields = ('total_price',)
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_display_links = ('id', 'user')
    list_filter = ('status',)
    list_per_page = 50
    search_fields = ('user__full_name', 'user__username', 'user__telegram_id')