from django.contrib import admin
from django.utils.html import format_html
from .models import Author, Category, Comment, MobilePrice, Post, ContactInfo

admin.site.site_header = 'KIRAN BLOG Administration'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width="80" height="80" />'.format(obj.profile_picture.url))

    image_tag.short_description = 'profile_pic'
    list_display = ['user', 'image_tag']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width="200" height="80" />'.format(obj.thumbnail.url))

    image_tag.short_description = 'thumbnail'
    list_display = ['title', 'author', 'timestamp', 'featured', 'image_tag']


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_no', 'company', 'messages']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'content', 'post')


@admin.register(MobilePrice)
class MobilePriceAdmin(admin.ModelAdmin):
    list_display = ('id',)
