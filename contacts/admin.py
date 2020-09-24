from django.contrib import admin
from .models import Contact
# Register your models here.


# @admin.register(Contact)
# class ContactAdmin(admin.ModelAdmin):
#     # list_display = fields = ('name', 'mobile', 'email',
#     #                          'address', 'profession', 'status')
#     list_filter = fields = ('name', 'mobile', 'email',
#                             'address', 'profession', 'status')

admin.site.register(Contact)
