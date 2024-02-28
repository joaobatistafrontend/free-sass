from django.db import models
from django.utils.text import slugify

class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Profissional(models.Model):
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100)
    # Adicione outros campos conforme necessário

    def __str__(self):
        return self.nome

class Servico(models.Model):
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    duracao = models.IntegerField()  # Em minutos, por exemplo
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    # Adicione outros campos conforme necessário

    def __str__(self):
        return self.nome

class HorarioAtendimento(models.Model):
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=10)  # Por exemplo: Segunda-feira, Terça-feira, etc.
    hora_abertura = models.TimeField()
    hora_fechamento = models.TimeField()

    def __str__(self):
        return f"{self.empresa.nome} - {self.dia_semana} ({self.hora_abertura}-{self.hora_fechamento})"
    
class MensagemAniversario(models.Model):
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    mensagem = models.TextField()

    def __str__(self):
        return f"Mensagem de Aniversário - {self.empresa.nome}"
    
class Cliente(models.Model):
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    numero_whatsapp = models.CharField(max_length=20)  # Número de telefone no formato internacional
    data_aniversario = models.DateField()

    def __str__(self):
        return self.nome