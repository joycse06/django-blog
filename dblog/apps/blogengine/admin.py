from django.contrib import admin
from django.contrib.auth.models import User
from dblog.apps.blogengine.models import Post, Category, Tag
# Register your models here.
from django.db import models
from redactor.widgets import AdminRedactorEditor


class PostAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'title', 'slug', 'author', 'site', 'pub_date')
    prepopulated_fields = {"slug": ("title",)}
    # exclude = ('id_author', )
    list_filter = ('pub_date', )
    search_fields = ('title', 'slug',)
    readonly_fields = ('author',)

    formfield_overrides = {
        models.TextField: {'widget': AdminRedactorEditor},
    }

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

    def queryset(self, request):
        """Limit Pages to those that belong to the request's user."""
        qs = super(PostAdmin, self).queryset(request)
        if request.user.is_superuser:
            # It is mine, all mine. Just return everything.
            return qs
        # Now we just add an extra filter on the queryset and
        # we're done. Assumption: Page.owner is a foreignkey
        # to a User.
        return qs.filter(author=request.user)

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