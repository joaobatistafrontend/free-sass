
from django.contrib import admin
from django.urls import path,include
from .views import *
from .comunviews import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('<slug:empresa_slug>/', empresa_detail, name='empresa_detail'),
    path('<slug:empresa_slug>/cadastrar-profissional/', cadastrar_profissional, name='cadastrar_profissional'),
    path('<slug:empresa_slug>/cadastrar-servico/', cadastrar_servico, name='cadastrar_servico'),
    path('<slug:empresa_slug>/cadastrar-horario-atendimento/', cadastrar_horario_atendimento, name='cadastrar_horario_atendimento'),
    path('<slug:empresa_slug>/cadastrar-mensagem-aniversario/', cadastrar_mensagem_aniversario, name='cadastrar_mensagem_aniversario'),
    path('<slug:empresa_slug>/cadastrar-cliente/', cadastrar_cliente, name='cadastrar_cliente'),

    path('<slug:empresa_slug>/cadastrar-agendamento/', agendamento, name='agendamento'),
    path('<slug:empresa_slug>/pro/', prof, name='Profissional'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)