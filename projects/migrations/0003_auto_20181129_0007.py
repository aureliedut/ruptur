# Generated by Django 2.1.3 on 2018-11-29 00:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0002_auto_20181123_1512'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectContributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('AX', 'Accepté'), ('RQ', 'Demandé'), ('RF', 'Refusé')], default='RQ', max_length=2)),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='users.Contributor'),
        ),
        migrations.AddField(
            model_name='projectcontributor',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='projectcontributor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='contributors',
            field=models.ManyToManyField(related_name='projects', through='projects.ProjectContributor', to=settings.AUTH_USER_MODEL),
        ),
    ]