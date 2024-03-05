from django.db import models
from django.utils.text import slugify
from PIL import Image

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
    imagem = models.ImageField(upload_to='imagens/',blank=True, null=True)

    # Adicione outros campos conforme necessário

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.imagem:
            img = Image.open(self.imagem.path)

            # Defina as larguras e alturas desejadas
            largura_padrao = 208
            altura_padrao = 300

            # Redimensione a imagem
            img.thumbnail((largura_padrao, altura_padrao))
            img.save(self.imagem.path)

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
    disponivel = models.BooleanField(default=True)

    def marcar_como_ocupado(self):
        self.disponivel = False
        self.save()

    def marcar_como_disponivel(self):
        self.disponivel = True
        self.save()


    def __str__(self):
        return f"{self.empresa.nome} - {self.dia_semana} ({self.hora_abertura.strftime('%H:%M')} às {self.hora_fechamento.strftime('%H:%M')}) {self.disponivel}"
    
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