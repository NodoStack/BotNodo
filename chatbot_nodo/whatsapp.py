import requests
import os

META_TOKEN = os.getenv("META_ACCESS_TOKEN")
PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")

def enviar_mensaje_whatsapp(telefono, texto):
    url = f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages"

    headers = {
        "Authorization": f"Bearer {META_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": telefono,
        "type": "text",
        "text": {
            "body": texto
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
