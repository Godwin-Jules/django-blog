from django.contrib import admin
from .models import *

# Register your models here

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email_address',)
    list_filter = ('first_name', 'last_name',)
    sortable_by = ('first_name', 'last_name',)

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'date', 'author', 'slug',)
    list_filter = ('title', 'date',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'post',)

admin.site.register(Tag)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)