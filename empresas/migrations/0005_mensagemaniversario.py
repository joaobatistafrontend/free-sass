# Generated by Django 4.2.10 on 2024-02-28 02:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0004_horarioatendimento'),
    ]

    operations = [
        migrations.CreateModel(
            name='MensagemAniversario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensagem', models.TextField()),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresas.empresa')),
            ],
        ),
    ]
