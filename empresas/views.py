from django.shortcuts import render,redirect
from .models import *
from .forms import *
from .utils import enviar_mensagem_whatsapp
from datetime import date
import pywhatkit as kit
from .tasks import *
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
from .models import Empresa, MensagemAniversario
from .forms import MensagemAniversarioForm



def prof(request, empresa_slug):
    empresa = Empresa.objects.get(slug=empresa_slug)
    profissionais = Profissional.objects.filter(empresa=empresa)
    return render(request, 'comun/profissionais.html', {'empresa': empresa, 'profissionais': profissionais})


def cadastrar_mensagem_aniversario(request, empresa_slug):
    empresa = Empresa.objects.get(slug=empresa_slug)

    try:
        mensagem_aniversario = MensagemAniversario.objects.get(empresa=empresa)
    except MensagemAniversario.DoesNotExist:
        mensagem_aniversario = None

    if request.method == 'POST':
        form = MensagemAniversarioForm(request.POST, instance=mensagem_aniversario)
        if form.is_valid():
            mensagem_aniversario = form.save(commit=False)
            mensagem_aniversario.empresa = empresa
            mensagem_aniversario.save()
            
            # Chamar a função para enviar mensagens de aniversário
            enviar_mensagem_aniversario(mensagem_aniversario)
            
            return redirect('empresa_detail', empresa_slug=empresa.slug)
    else:
        form = MensagemAniversarioForm(instance=mensagem_aniversario)

    return render(request, 'cadastrar_mensagem_aniversario.html', {'form': form, 'empresa': empresa})

def enviar_mensagem_aniversario(mensagem_aniversario):
    # Configurações do Chrome WebDriver (certifique-se de que o chromedriver.exe está no seu PATH)
    service = Service('path/to/chromedriver')  # Substitua 'path/to/chromedriver' pelo caminho do seu chromedriver.exe
    service.start()
    
    # Configurações do Chrome para conectar-se a uma instância existente
    chrome_options = webdriver.ChromeOptions()
    chrome_options.debugger_address = "localhost:9222"
    
    # Inicializa o WebDriver do Chrome com as configurações
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Obter a data e hora atuais
    data_e_hora_atual = datetime.now()
    
    # Filtrar os clientes que fazem aniversário hoje
    clientes_aniversariantes = Cliente.objects.filter(data_aniversario__month=data_e_hora_atual.month, data_aniversario__day=data_e_hora_atual.day)
    
    # Mensagem de aniversário
    mensagem = mensagem_aniversario.mensagem
    
    # Enviar mensagem de aniversário para cada cliente
    for cliente in clientes_aniversariantes:
        numero_whatsapp = cliente.numero_whatsapp
        
        # Cria a URL para enviar a mensagem diretamente para o número de telefone
        url_mensagem = f"https://web.whatsapp.com/send?phone={numero_whatsapp}&text={mensagem}"
        
        # Abre a URL da mensagem no navegador existente
        driver.get(url_mensagem)
        
        # Enviar a mensagem pressionando a tecla Enter
        try:
            driver.find_element_by_css_selector("footer div.copyable-text").send_keys(Keys.ENTER)
        except Exception as e:
            print(f"Erro ao enviar mensagem para o número {numero_whatsapp}: {e}")
        
        # Espera um curto período para garantir que a mensagem seja enviada
        time.sleep(2)
        
    # Fecha o navegador após o envio de todas as mensagens
    driver.quit()






#funciona
'''def cadastrar_mensagem_aniversario(request, empresa_slug):
    empresa = Empresa.objects.get(slug=empresa_slug)

    try:
        mensagem_aniversario = MensagemAniversario.objects.get(empresa=empresa)
    except MensagemAniversario.DoesNotExist:
        mensagem_aniversario = None

    if request.method == 'POST':
        form = MensagemAniversarioForm(request.POST, instance=mensagem_aniversario)
        if form.is_valid():
            mensagem_aniversario = form.save(commit=False)
            mensagem_aniversario.empresa = empresa
            mensagem_aniversario.save()
            
            # Chamar a função para enviar mensagens de aniversário
            enviar_mensagem_aniversario(mensagem_aniversario)
            
            return redirect('empresa_detail', empresa_slug=empresa.slug)
    else:
        form = MensagemAniversarioForm(instance=mensagem_aniversario)

    return render(request, 'cadastrar_mensagem_aniversario.html', {'form': form, 'empresa': empresa})

def enviar_mensagem_aniversario(mensagem_aniversario):
    # Obter a data e hora atuais
    data_e_hora_atual = datetime.now()
    
    # Obter a hora e minuto do horário atual
    hora_atual = data_e_hora_atual.hour
    minuto_atual = data_e_hora_atual.minute
    
    # Filtrar os clientes que fazem aniversário hoje
    clientes_aniversariantes = Cliente.objects.filter(data_aniversario__month=data_e_hora_atual.month, data_aniversario__day=data_e_hora_atual.day)
    
    # Mensagem de aniversário
    mensagem = mensagem_aniversario.mensagem
    
    # Enviar mensagem de aniversário para cada cliente
    for cliente in clientes_aniversariantes:
        numero_whatsapp = cliente.numero_whatsapp
        # Enviar a mensagem imediatamente
        kit.sendwhatmsg_instantly(f"+{numero_whatsapp}", mensagem)'''

def cadastrar_cliente(request, empresa_slug):
    empresa = Empresa.objects.get(slug=empresa_slug)

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.empresa = empresa
            cliente.save()
            return redirect('empresa_detail', empresa_slug=empresa.slug)
    else:
        form = ClienteForm()

    return render(request, 'cadastrar_cliente.html', {'form': form, 'empresa': empresa})
'''def cadastrar_mensagem_aniversario(request, empresa_slug):
    empresa = Empresa.objects.get(slug=empresa_slug)

    try:
        mensagem_aniversario = MensagemAniversario.objects.get(empresa=empresa)
    except MensagemAniversario.DoesNotExist:
        mensagem_aniversario = None

    if request.method == 'POST':
        form = MensagemAniversarioForm(request.POST, instance=mensagem_aniversario)
        if form.is_valid():
            mensagem_aniversario = form.save(commit=False)
            mensagem_aniversario.empresa = empresa
            mensagem_aniversario.save()
            
            # Enviar mensagem de aniversário para todos os clientes
            clientes = Cliente.objects.filter(empresa=empresa, data_aniversario=date.today())
            for cliente in clientes:
                enviar_mensagem_whatsapp(cliente.numero_whatsapp, mensagem_aniversario.mensagem)
            
            return redirect('empresa_detail', empresa_slug=empresa.slug)
    else:
        form = MensagemAniversarioForm(instance=mensagem_aniversario)

    return render(request, 'cadastrar_mensagem_aniversario.html', {'form': form, 'empresa': empresa})
'''
'''def cadastrar_mensagem_aniversario(request, empresa_slug):
    empresa = Empresa.objects.get(slug=empresa_slug)

    try:
        mensagem_aniversario = MensagemAniversario.objects.get(empresa=empresa)
    except MensagemAniversario.DoesNotExist:
        mensagem_aniversario = None

    if request.method == 'POST':
        form = MensagemAniversarioForm(request.POST, instance=mensagem_aniversario)
        if form.is_valid():
            mensagem_aniversario = form.save(commit=False)
            mensagem_aniversario.empresa = empresa
            mensagem_aniversario.save()
            return redirect('empresa_detail', empresa_slug=empresa.slug)
    else:
        form = MensagemAniversarioForm(instance=mensagem_aniversario)

    return render(request, 'cadastrar_mensagem_aniversario.html', {'form': form, 'empresa': empresa})'''

def cadastrar_horario_atendimento(request, empresa_slug):
    empresa = Empresa.objects.get(slug=empresa_slug)

    if request.method == 'POST':
        form = HorarioAtendimentoForm(request.POST)
        if form.is_valid():
            horario_atendimento = form.save(commit=False)
            horario_atendimento.empresa = empresa
            horario_atendimento.save()
            return redirect('empresa_detail', empresa_slug=empresa.slug)
    else:
        form = HorarioAtendimentoForm()

    return render(request, 'cadastrar_horario_atendimento.html', {'form': form, 'empresa': empresa})


def cadastrar_servico(request, empresa_slug):
    empresa = Empresa.objects.get(slug=empresa_slug)

    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            servico = form.save(commit=False)
            servico.empresa = empresa
            servico.save()
            return redirect('empresa_detail', empresa_slug=empresa.slug)
    else:
        form = ServicoForm()

    return render(request, 'cadastrar_servico.html', {'form': form, 'empresa': empresa})
def cadastrar_profissional(request, empresa_slug):
    empresa = Empresa.objects.get(slug=empresa_slug)

    if request.method == 'POST':
        form = ProfissionalForm(request.POST)
        if form.is_valid():
            profissional = form.save(commit=False)
            profissional.empresa = empresa
            profissional.save()
            return redirect('empresa_detail', empresa_slug=empresa.slug)
    else:
        form = ProfissionalForm()

    return render(request, 'cadastrar_profissional.html', {'form': form, 'empresa': empresa})

def empresa_detail(request, empresa_slug):
    empresa = Empresa.objects.get(slug=empresa_slug)
    return render(request, 'index.html', {'empresa': empresa})
