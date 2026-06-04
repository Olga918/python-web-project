from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.timezone import now

from .models import *
from .forms import ProductForm, UserChangeForm, UserCreationForm

# admin.site.register(Product)

# admin.site.register(MyUser)

@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    model = MyUser
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ('id', 'email', 'full_name', 'is_active' ,'is_staff', 'is_superuser')
    ordering=('id', )
    fieldsets =(
        ('Дані для входу', {"fields": ("email", "password")}),
        ('Подробиці про користувача', {"fields": ("first_name", "last_name", "birth_date")}),
        ('Статус на сайті та ролі', {
            "classes":('collapsed',),
            "fields": ("is_staff","is_superuser", "is_active")}),
        ('Групи та дозволи', {"fields":("groups", "user_permissions")})
    )
    
    add_fieldsets =(
        ('Дані для входу', {"fields": ("email", "password1", "password2")}),
        ('Подробиці про користувача', {"fields": ("first_name", "last_name", "birth_date")}),
        ('Статус на сайті та ролі', {
            "classes":('collapsed',),
            "fields": ("is_staff","is_superuser", "is_active")}),
        ('Групи та дозволи', {"fields":("groups", "user_permissions")})
    )
    
    def full_name(self, user:MyUser):
        return f"{user.first_name} {user.last_name}"
    
    full_name.short_description = "Повне ім'я"


#region Client site models

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('id', 'name', 'price', 'description', 'created_at','deleted_at', 'category__name', 'product_tags')
    list_filter = ('price', 'name', 'category__name', 'tags__name')
    fields = [
        ('name', 'price'),
        ('description',),
        'category',
        'tags'
    ]
    
    # filter_horizontal = ('tags',)
    filter_vertical = ('tags',)
    
    
    
    @admin.display(description='Теги')
    def product_tags(self, product:Product):
        if product.tags:
            return ",".join([i.name for i in product.tags.all()])
        return '-'
    
    @admin.action(description="Архівувати товари")
    def archive_products(self, request, queryset):
        queryset.update(deleted_at=now())
        
    @admin.action(description="Повернути товари")
    def restore_products(self, request, queryset):
        queryset.update(deleted_at=None)
        
    actions = [archive_products, restore_products]
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.has_perm('core.my_permission'):
            return actions
        del actions["archive_products"]
        del actions["restore_products"]
        
        return actions

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'deleted_at', 'product_count')
    
    def product_count(self, category:Category):
        return category.product_set.count()
    
    product_count.short_description = 'Кількість продуктів'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

#endregion