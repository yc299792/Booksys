from django.contrib import admin
from Book.models import *
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(BookInfo,BookAdmin)
admin.site.register(PictureInfo)
admin.site.register(PeopleInfo)

