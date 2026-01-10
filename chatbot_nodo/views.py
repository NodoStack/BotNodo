import json
import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import ChatUser, ChatMessage
from .bot_logic import iniciar_conversacion, procesar_mensaje_usuario
from .states import MENU_PRINCIPAL


@csrf_exempt
def chatbot_webhook(request):

    # =========================
    # ✅ VERIFICACIÓN META (GET)
    # =========================
    if request.method == "GET":
        verify_token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if verify_token == os.getenv("META_VERIFY_TOKEN"):
            return HttpResponse(challenge)
        else:
            return HttpResponse("Invalid verify token", status=403)

    # =========================
    # 🔹 MENSAJES (POST)
    # =========================
    if request.method == "POST":
        try:
            data_json = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        usuario_id = data_json.get("usuario_id")
        mensaje = data_json.get("mensaje", "").strip()

        if not usuario_id:
            return JsonResponse({"error": "usuario_id requerido"}, status=400)

        # Obtener o crear usuario
        user, _ = ChatUser.objects.get_or_create(
            telefono=usuario_id,
            defaults={"estado": MENU_PRINCIPAL}
        )

        # Guardar mensaje entrante
        if mensaje:
            ChatMessage.objects.create(
                user=user,
                texto=mensaje,
                direccion="in"
            )

        # Lógica del bot
        if not mensaje:
            respuesta, estado = iniciar_conversacion(usuario_id)
        else:
            respuesta, estado = procesar_mensaje_usuario(usuario_id, mensaje)

        # Guardar respuesta
        ChatMessage.objects.create(
            user=user,
            texto=respuesta,
            direccion="out"
        )

        return JsonResponse({
            "respuesta": respuesta,
            "estado": estado
        })

    return JsonResponse({"error": "Método no permitido"}, status=405)
