from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel
from django.contrib.auth.models import User
# Create your models here.


class  Historical_Emails(BaseModel):

    send_to=models.ForeignKey(User,on_delete=models.CASCADE , related_name="email_send_user")
    asunto=models.CharField(max_length=250)
    historical=HistoricalRecords()

    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by=value


    def __str__(self) -> str:
        return ""