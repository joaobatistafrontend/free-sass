from twilio.rest import Client
from django.conf import settings

def enviar_mensagem_whatsapp(numero_destino, mensagem):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=mensagem,
        from_='whatsapp:' + settings.TWILIO_WHATSAPP_NUMBER,
        to='whatsapp:' + numero_destino
    )
    return message.sid
