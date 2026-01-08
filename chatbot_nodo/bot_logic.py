from .states import *
from .models import ChatUser, Lead


def iniciar_conversacion(usuario_id):
    user, _ = ChatUser.objects.get_or_create(
        telefono=usuario_id,
        defaults={"estado": MENU_PRINCIPAL}
    )

    user.estado = MENU_PRINCIPAL
    user.save()

    mensaje = (
        "👋 ¡Hola! Soy el asistente de NodoStack.\n\n"
        "¿En qué podemos ayudarte hoy?\n"
        "Respondé con el número 👇\n\n"
        "1️⃣ Quiero desarrollar una app o sistema\n"
        "2️⃣ Tengo una idea y quiero asesoramiento\n"
        "3️⃣ Quiero hablar con alguien\n"
        "4️⃣ Tengo una consulta general"
    )

    return mensaje, MENU_PRINCIPAL


def procesar_mensaje_usuario(usuario_id, mensaje):
    mensaje = mensaje.strip()

    user, _ = ChatUser.objects.get_or_create(
        telefono=usuario_id,
        defaults={"estado": MENU_PRINCIPAL}
    )

    lead, _ = Lead.objects.get_or_create(user=user)
    estado = user.estado

    # 🔒 Conversación finalizada
    if estado == FIN:
        return "🙏 La conversación ya finalizó. Si necesitás algo más, escribí nuevamente.", FIN

    # 🔙 Volver al menú (global)
    if mensaje == "0":
        return iniciar_conversacion(usuario_id)

    # ------------------ MENU PRINCIPAL ------------------
    if estado == MENU_PRINCIPAL:

        if mensaje == "1":
            lead.status = "interesado"
            lead.save()
            user.estado = DESARROLLO_TIPO
            user.save()
            return (
                "🚀 ¡Genial! ¿Qué tipo de solución estás buscando?\n\n"
                "1️⃣ 📱 Aplicación móvil\n"
                "2️⃣ 🖥️ Sistema web\n"
                "3️⃣ 🧠 Integración con IA\n"
                "4️⃣ 🛒 E-commerce\n"
                "5️⃣ 🏢 Software empresarial\n"
                "0️⃣ 🔙 Volver",
                DESARROLLO_TIPO
            )

        if mensaje == "2":
            lead.status = "interesado"
            lead.save()
            user.estado = ASESORAMIENTO
            user.save()
            return (
                "💡 Nos encanta trabajar con ideas desde cero.\n"
                "¿Cómo preferís avanzar?\n\n"
                "1️⃣ 📅 Agendar reunión gratuita\n"
                "2️⃣ 📝 Dejar mi idea por escrito\n"
                "0️⃣ 🔙 Volver",
                ASESORAMIENTO
            )

        if mensaje == "3":
            user.estado = CONTACTO_HUMANO
            user.save()
            return (
                "📞 Un asesor se pondrá en contacto a la brevedad ✅\n\n",
                CONTACTO_HUMANO
            )

        if mensaje == "4":
            user.estado = FAQ_MENU
            user.save()
            return (
                "❓ ¿Qué querés saber?\n\n"
                "1️⃣ 💰 Costos\n"
                "2️⃣ ⏱️ Tiempos\n"
                "3️⃣ 🔐 Protección de ideas\n"
                "4️⃣ 🧑‍💻 Equipo\n"
                "0️⃣ 🔙 Volver",
                FAQ_MENU
            )

        return iniciar_conversacion(usuario_id)


    # ------------------ DESARROLLO_TIPO ------------------
    if estado == DESARROLLO_TIPO:
        opciones = {
            "1": "Aplicación móvil",
            "2": "Sistema web",
            "3": "Integración con IA",
            "4": "E-commerce",
            "5": "Software empresarial"
        }

        if mensaje not in opciones:
            return "❌ Elegí una opción válida (1 a 5).", DESARROLLO_TIPO

        lead.tipo_proyecto = opciones[mensaje]
        lead.save()

        user.estado = DESARROLLO_DESCRIPCION
        user.save()

        return (
            "Perfecto. Contanos en palabras qué necesitás desarrollar:",
            DESARROLLO_DESCRIPCION
        )

    # ------------------ DESARROLLO_DESCRIPCION ------------------
    if estado == DESARROLLO_DESCRIPCION:
        lead.descripcion_proyecto = mensaje
        lead.status = "calificado"
        lead.save()

        user.estado = DESARROLLO_CONFIRMACION
        user.save()

        return (
            "Gracias por la descripción. Un asesor se pondrá en contacto a la brevedad ✅",
            DESARROLLO_CONFIRMACION
        )

    # ------------------ DESARROLLO_CONFIRMACION ------------------
    if estado == DESARROLLO_CONFIRMACION:
        user.estado = FIN
        user.save()
        return "🙏 Gracias por tu interés en NodoStack.", FIN

    # ------------------ ASESORAMIENTO ------------------
    if estado == ASESORAMIENTO:

        if mensaje == "1":
            lead.status = "agenda"
            lead.save()
            user.estado = ASESORAMIENTO_CONFIRMACION
            user.save()
            return (
                "📅 Genial. Te dejamos el link para agendar tu reunión:\n"
                "https://calendly.com/nodostack/consulta",
                ASESORAMIENTO_CONFIRMACION
            )

        if mensaje == "2":            
            user.estado = ASESORAMIENTO_IDEA
            user.save()
            return "📝 Contanos tu idea:", ASESORAMIENTO_IDEA

        return "❌ Opción inválida. Elegí 1, 2 o 0.", ASESORAMIENTO

    # ------------------ ASESORAMIENTO_IDEA ------------------
    if estado == ASESORAMIENTO_IDEA:
        lead.idea = mensaje
        lead.status = "calificado"
        lead.save()
        
        user.estado = ASESORAMIENTO_CONFIRMACION
        user.save()

        return (
            "Gracias por compartir tu idea 🙌 Un asesor se pondrá en contacto.",
            ASESORAMIENTO_CONFIRMACION
        )

    # ------------------ ASESORAMIENTO_CONFIRMACION ------------------
    if estado == ASESORAMIENTO_CONFIRMACION:
        user.estado = FIN
        user.save()
        return "🙏 Gracias por tu interés en NodoStack.", FIN

    # ------------------ CONTACTO_HUMANO ------------------
    if estado == CONTACTO_HUMANO:
        user.estado = FIN
        user.save()
        return "✅ Un asesor se pondrá en contacto a la brevedad.", FIN

    # ------------------ FAQ ------------------
    if estado == FAQ_MENU:
        if lead.status == "nuevo":
           lead.status = "descartado"
           lead.save()
        respuestas = {
            "1": "💰 El costo depende del alcance del proyecto.",
            "2": "⏱️ Los tiempos varían según complejidad.",
            "3": "🔐 Firmamos acuerdos de confidencialidad.",
            "4": "🧑‍💻 Nuestro equipo está formado por devs senior."
        }

        if mensaje in respuestas:
            return respuestas[mensaje] + "\n\n0️⃣ 🔙 Volver al menú", FAQ_MENU

        return "❌ Opción inválida. Elegí 1 a 4 o 0.", FAQ_MENU

    # ------------------ FALLBACK ------------------
    return iniciar_conversacion(usuario_id)
    
    
    
    
    
    
    
    
    
    
    
    