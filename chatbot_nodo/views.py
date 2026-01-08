import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import ChatUser, ChatMessage
from .bot_logic import iniciar_conversacion, procesar_mensaje_usuario
from .states import MENU_PRINCIPAL


@csrf_exempt
def chatbot_webhook(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data_json = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    usuario_id = data_json.get("usuario_id")
    mensaje = data_json.get("mensaje", "").strip()

    if not usuario_id:
        return JsonResponse({"error": "usuario_id requerido"}, status=400)

    # 🔹 Obtener o crear usuario
    user, _ = ChatUser.objects.get_or_create(
        telefono=usuario_id,
        defaults={"estado": MENU_PRINCIPAL}
    )

    # 🔹 Guardar mensaje entrante
    if mensaje:
        ChatMessage.objects.create(
            user=user,
            texto=mensaje,
            direccion="in"
        )

    # 🔹 Lógica del bot (UNA sola fuente de verdad)
    if not mensaje:
        respuesta, estado = iniciar_conversacion(usuario_id)
    else:
        respuesta, estado = procesar_mensaje_usuario(usuario_id, mensaje)

    # 🔹 Guardar respuesta del bot
    ChatMessage.objects.create(
        user=user,
        texto=respuesta,
        direccion="out"
    )

    # ⚠️ NO guardar estado acá
    # El bot_logic ya lo hace

    return JsonResponse({
        "respuesta": respuesta,
        "estado": estado
    })
