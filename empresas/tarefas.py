# meuapp/tarefas.py
import pywhatkit as kit
from datetime import date
from empresas.models import Cliente

def enviar_mensagem_aniversario():
    # Obter a data atual
    data_atual = date.today()
    
    # Filtrar os clientes que fazem aniversário hoje
    clientes_aniversariantes = Cliente.objects.filter(data_aniversario__month=data_atual.month, data_aniversario__day=data_atual.day)
    
    # Mensagem de aniversário
    mensagem_aniversario = "Feliz Aniversário! 🎉🎂 Espero que seu dia seja cheio de alegria e felicidade!"

    # Enviar mensagem de aniversário para cada cliente
    for cliente in clientes_aniversariantes:
        numero_whatsapp = cliente.numero_whatsapp
        # Enviar a mensagem
        kit.sendwhatmsg(f"+{numero_whatsapp}", mensagem_aniversario, data_atual.hour, data_atual.minute)
