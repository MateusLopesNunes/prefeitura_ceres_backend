from django.contrib import admin
from .models import RequestType, StatusCode, Status, Request

class RequestTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'desc') #coloca os campos na tabela
    list_display_links = ('id', 'desc') #vira links
    search_fields = ('desc',) #cria uma pesquisa
    list_per_page = 10 #cria paginação

class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_user', 'request_type', 'importance', 'comment', 'lat', 'lon', 'created', 'completed') #coloca os campos na tabela
    list_display_links = ('id',) #vira links
    search_fields = ('desc',) #cria uma pesquisa
    list_per_page = 10 #cria paginação

class StatusCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'desc', 'title') #coloca os campos na tabela
    list_display_links = ('id', 'desc') #vira links
    search_fields = ('desc',) #cria uma pesquisa
    list_per_page = 10 #cria paginação

class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_request', 'status_code', 'dateTime') #coloca os campos na tabela
    list_display_links = ('id',) #vira links
    search_fields = ('id_request', 'status_code',) #cria uma pesquisa
    list_per_page = 10 #cria paginação

admin.site.register(RequestType, RequestTypeAdmin)
admin.site.register(StatusCode, StatusCodeAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Request, RequestAdmin)