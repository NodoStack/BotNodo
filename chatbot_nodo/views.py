import json
import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import ChatUser, ChatMessage
from .bot_logic import iniciar_conversacion, procesar_mensaje_usuario
from .states import MENU_PRINCIPAL
from .whatsapp import enviar_mensaje_whatsapp


VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")


@csrf_exempt
def chatbot_webhook(request):
    # =========================
    # GET → Verificación Meta
    # =========================
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        return HttpResponse("Forbidden", status=403)

    # =========================
    # POST → Mensajes WhatsApp
    # =========================
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        try:
            entry = data["entry"][0]
            change = entry["changes"][0]
            value = change["value"]

            # Mensaje entrante
            message = value["messages"][0]
            usuario_id = message["from"]
            mensaje = message["text"]["body"]

        except (KeyError, IndexError):
            # Eventos que no son mensajes (los ignoramos)
            return JsonResponse({"status": "ignored"}, status=200)

        # Usuario
        user, _ = ChatUser.objects.get_or_create(
            telefono=usuario_id,
            defaults={"estado": MENU_PRINCIPAL}
        )

        # Guardar mensaje entrante
        ChatMessage.objects.create(
            user=user,
            texto=mensaje,
            direccion="in"
        )

        # Lógica del bot
        respuesta, estado = procesar_mensaje_usuario(usuario_id, mensaje)

        # Guardar respuesta
        ChatMessage.objects.create(
            user=user,
            texto=respuesta,
            direccion="out"
        )

        # ⚠️ Por ahora solo devolvemos OK
        # En el paso B enviaremos el mensaje por la API
        enviar_mensaje_whatsapp(usuario_id, respuesta)

        return JsonResponse({"status": "ok"}, status=200)

    return JsonResponse({"error": "Método no permitido"}, status=405)
