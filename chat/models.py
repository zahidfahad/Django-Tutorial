from django.db import models
from user.models import (
    User,BaseModel
)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Q

# Create your models here.





class DialogsModel(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User1"),
                              related_name="user1", db_index=True)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User2"),
                              related_name="user2", db_index=True)

    changeable_timestamp = models.DateTimeField(null=True)

    def __str__(self):
        return "Dialog between " + f"{self.user1_id}, {self.user2_id}"


    @staticmethod
    def dialog_exists(u1: AbstractBaseUser, u2: AbstractBaseUser):
        return DialogsModel.objects.filter(Q(user1=u1, user2=u2) | Q(user1=u2, user2=u1)).exists()   

    @staticmethod
    def create_if_not_exists(u1: AbstractBaseUser, u2: AbstractBaseUser):
        if not DialogsModel.dialog_exists(u1, u2):
            res = DialogsModel.objects.create(user1=u1, user2=u2)
        else:
            res = \
            DialogsModel.objects.filter(Q(user1=u1, user2=u2) | Q(user1=u2,user2=u1)).last()
        return res

    @staticmethod
    def get_dialogs_for_user(user: AbstractBaseUser):
        dialogs = DialogsModel.objects.filter(Q(user1=user) | Q(user2=user)).order_by('-changeable_timestamp')
        return dialogs

    @staticmethod
    def get_dialog_between(u1: AbstractBaseUser, u2: AbstractBaseUser):
        if DialogsModel.dialog_exists(u1,u2):
            dialog = DialogsModel.objects.filter(Q(user1=u1,user2=u2) | Q(user1=u2,user2=u1)).last()
            return dialog
        return None

    @property
    def get_last_text(self):
        return MessageModel.objects.filter(dialog=self).latest('sent')

    @property
    def get_conversation(self):
        # returns whole convo
        return self.dialog_messages.all()

    @property
    def msg_exist(self):
        msg = self.dialog_messages.all()
        if msg:
            return True
        return False

    @staticmethod
    def sort_dialogs_by_time(dialog,sent):
        try:
            dialog = DialogsModel.objects.get(id = dialog.id)
            dialog.changeable_timestamp = sent
            dialog.save()
        except Exception as e:
            print(e)

    class Meta:
        unique_together = ('user1', 'user2',)
        verbose_name = "Dialog"
        verbose_name_plural = "Dialogs"
        default_permissions = ()

    def save(self, *args, **kwargs):
        # can not create a dialog with self
        if not self.user1 == self.user2:
            super(DialogsModel, self).save(*args, **kwargs)




class MessageModel(models.Model):
    # dialog between
    dialog = models.ForeignKey(DialogsModel,on_delete=models.CASCADE,
    related_name="dialog_messages",verbose_name=_("Dialog Instance"))
    # thread name is sender & receivers combination of id
    # it works as the room name for both user to stay in a same room
    # via django channels websocket
    thread_name = models.TextField(db_index=True)
    # sender
    sender = models.ForeignKey(User,on_delete=models.CASCADE,
    related_name="msg_sender",verbose_name=_("Sender"),db_index=True)
    # receiver
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,
    related_name="msg_receiver",verbose_name=_("Receiver"),db_index=True)
    # actual msg text
    text = models.TextField(null=True,verbose_name=_("Message Text"))
    # msg sent time
    sent = models.DateTimeField(auto_now_add=True,verbose_name=_("Message Sent Time"))
    # read/unread
    read = models.BooleanField(verbose_name=_("Read/Unread Status"), default=False)

    @staticmethod
    def get_unread_count_for_dialog_between(sender :AbstractBaseUser, receiver :AbstractBaseUser):
        return \
        MessageModel.objects.filter(sender = sender, receiver = receiver, read=False).count()

    def __str__(self):
        return str(self.pk)

    @staticmethod
    def get_convo_between(u1: AbstractBaseUser, u2 :AbstractBaseUser):
        return \
        MessageModel.objects.filter(
            Q(sender=u1,receiver=u2) | Q(sender=u2,receiver=u1)
        )

    # customizing model save method on upon every save call
    def save(self, *args, **kwargs):
        # create dialog model if not exists
        self.dialog = DialogsModel.create_if_not_exists(self.sender, self.receiver)
        super(MessageModel, self).save(*args, **kwargs)

        # after saving self => ordering dialog model
        DialogsModel.sort_dialogs_by_time(self.dialog,self.sent)



    class Meta:
        ordering = ('sent',)
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        default_permissions = ()