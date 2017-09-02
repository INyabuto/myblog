from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish',
                    'status')
    list_filter = ('status', 'created', 'publish', 'author') # create a sidebar with filter options
    search_fields = ('title', 'body') # Create a search option
    prepopulated_fields = {'slug': ('title',)} # prepolate the slug field with the title
    raw_id_fields = ('author',) # create a look up widget on the author field
    date_hierarchy = 'publish' # sort by publish
    ordering = ['status', 'publish'] # order by status and publish

# Register your models here.
admin.site.register(Post, PostAdmin)
