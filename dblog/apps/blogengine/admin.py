from django.contrib import admin
from django.contrib.auth.models import User
from dblog.apps.blogengine.models import Post, Category, Tag
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'title', 'slug', 'author', 'site')
    prepopulated_fields = {"slug": ("title",)}
    # exclude = ('author', )

    fieldsets = [
        ('Post', {
            'fields': ('title', 'slug', 'site', 'pub_date')
        }),
        ('Post Body', {
            'fields': ('text',)
        }),
        ('Author', {
            'fields': ('author',)
        }),
        ('Category',{
            'fields': ('category',)
        }),
        ('Tags', {
            'fields': ('tags', )
        }
            )
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag,TagAdmin)