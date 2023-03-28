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
    list_display = ['title','author','like','book_category','public_status']

class ImageAdmin(admin.ModelAdmin):
    list_display = ['book','page_number','img_location']

admin.site.register(Book, BookAdmin)
admin.site.register(Image,ImageAdmin)

class styleBaseAdmin(admin.ModelAdmin):
    list_display = ['name','styleID','stylePrompt','scale','steps','style_preview']

admin.site.register(Stylebase,styleBaseAdmin)

class BookInline(admin.TabularInline):
    model = Book
    extra = 0

class UserinfoAdmin(admin.ModelAdmin):
    inlines = [BookInline]
    list_display=['UserID','head_shot']

admin.site.register(Userinfo, UserinfoAdmin)