# Generated by Django 5.0.6 on 2024-06-28 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0013_remove_mapaaulas_data_atualizacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapaaulas',
            name='imagem',
            field=models.ImageField(default='default_mapa_aulas.png', upload_to='mapas_aulas/'),
        ),
        migrations.AlterField(
            model_name='mapaaulas',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='mapas_aulas/'),
        ),
    ]
