from user.models import Usuario, UserType
from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'dataNasc', 'cpf', 'telefone', 'email') #coloca os campos na tabela
    list_display_links = ('id', 'nome') #vira links
    search_fields = ('nome',) #cria uma pesquisa
    list_per_page = 10 #cria paginação

class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'desc') #coloca os campos na tabela
    list_display_links = ('id', 'desc') #vira links
    search_fields = ('desc',) #cria uma pesquisa
    list_per_page = 10 #cria paginação


admin.site.register(Usuario, UserAdmin)
admin.site.register(UserType, UserTypeAdmin)