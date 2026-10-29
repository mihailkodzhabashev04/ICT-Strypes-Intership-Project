from django.contrib import admin
from .models import Comment, Post, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','post_title', 'pundlished_date']
    list_display_links = ['id','post_title']
    list_filter = ['pundlished_date']
    search_fields = ['post_title']

# Register your models here.
admin.site.register(Comment)
admin.site.register(Tag)