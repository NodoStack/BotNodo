from chatbot_nodo.bot_logic import (
    iniciar_conversacion,
    procesar_mensaje_usuario,
    TEMP_DATA
)

def simular_conversacion(usuario_id, mensajes):
    print("=" * 35)
    print(f"👤 Usuario: {usuario_id}")
    print("=" * 35)

    # iniciar conversación
    respuesta, estado = iniciar_conversacion(usuario_id)
    print(f"BOT ({estado}): {respuesta}\n")

    for msg in mensajes:
        print(f"USER: {msg}")
        respuesta, estado = procesar_mensaje_usuario(usuario_id, msg)
        print(f"BOT ({estado}): {respuesta}\n")

    print("🧾 Estado final TEMP_DATA:")
    print(TEMP_DATA.get(usuario_id))
    print("=" * 35 + "\n\n")


# ================= PRUEBAS =================

# 1️⃣ Flujo desarrollo
simular_conversacion(
    "user_1",
    ["1", "2", "Necesito un sistema de gestión"]
)

# 2️⃣ Flujo asesoramiento
simular_conversacion(
    "user_2",
    ["2", "2", "Tengo una idea para una app educativa"]
)

# 3️⃣ Flujo contacto humano
simular_conversacion(
    "user_3",
    ["3"]
)

# 4️⃣ Flujo FAQ + volver al menú
simular_conversacion(
    "user_4",
    ["4", "1", "0"]
)
