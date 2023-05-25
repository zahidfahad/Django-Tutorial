# Generated by Django 4.2.1 on 2023-05-25 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DialogsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('changeable_timestamp', models.DateTimeField(null=True)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1', to=settings.AUTH_USER_MODEL, verbose_name='User1')),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2', to=settings.AUTH_USER_MODEL, verbose_name='User2')),
            ],
            options={
                'verbose_name': 'Dialog',
                'verbose_name_plural': 'Dialogs',
                'default_permissions': (),
                'unique_together': {('user1', 'user2')},
            },
        ),
        migrations.CreateModel(
            name='MessageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thread_name', models.TextField(db_index=True)),
                ('text', models.TextField(null=True, verbose_name='Message Text')),
                ('sent', models.DateTimeField(auto_now_add=True, verbose_name='Message Sent Time')),
                ('read', models.BooleanField(default=False, verbose_name='Read/Unread Status')),
                ('dialog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dialog_messages', to='chat.dialogsmodel', verbose_name='Dialog Instance')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_receiver', to=settings.AUTH_USER_MODEL, verbose_name='Receiver')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_sender', to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ('sent',),
                'default_permissions': (),
            },
        ),
    ]
