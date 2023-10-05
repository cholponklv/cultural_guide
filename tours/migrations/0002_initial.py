# Generated by Django 4.2.3 on 2023-10-05 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tours', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='toursmembers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tours',
            name='category',
            field=models.ManyToManyField(to='tours.categorytours'),
        ),
        migrations.AddField(
            model_name='tours',
            name='organizer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='organized_tours', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reviewstours',
            name='tours',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tours.tours'),
        ),
        migrations.AddField(
            model_name='reviewstours',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='likestours',
            name='tours',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tours.tours'),
        ),
        migrations.AddField(
            model_name='likestours',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='likesreviews',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='toursmembers',
            unique_together={('user', 'tours')},
        ),
    ]
