from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # we import this so we can edit the password field in our acc obj
from .models import Account


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')  #this turns this particular list to a link
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    #this will make the password readonly
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)


