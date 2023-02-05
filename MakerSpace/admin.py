from django.contrib import admin
# from .models import MakerSpace
from .models import * 


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Category, CategoryAdmin)


class PromptBaseAdmin(admin.ModelAdmin):
    list_display = ['category','keyword']
    list_filter = ['category','keyword']
    list_editable = ['keyword']
admin.site.register(PromptBase, PromptBaseAdmin)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class BookAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['bookID']

class ImageAdmin(admin.ModelAdmin):
    list_display = ['book','page_number']

admin.site.register(Book, BookAdmin)
admin.site.register(Image,ImageAdmin)
