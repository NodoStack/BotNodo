from django.contrib import admin
from .models import ChatUser, ChatMessage, Lead

@admin.register(ChatUser)
class ChatUserAdmin(admin.ModelAdmin):
    list_display = ("telefono", "estado", "creado")
    search_fields = ("telefono",)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "direccion", "fecha")
    list_filter = ("direccion",)
    search_fields = ("texto",)

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("user", "tipo_proyecto", "email")
