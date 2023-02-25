from user.models import Usuario
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

'''class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome') #coloca os campos na tabela
    list_display_links = ('id', 'nome') #vira links
    search_fields = ('nome',) #cria uma pesquisa
    list_per_page = 10 #cria paginação
'''

admin.site.register(Usuario)