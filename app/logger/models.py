from django.db import models


class LogEntry (models.Model): 
    temprature =  models.IntegerField()
    humidity = models.IntegerField();
    timestamp =  models.DateTimeField(auto_now_add=  True)

    def __str__(self):
        return str(self.timestamp) + f" -t@{self.temprature} -h@{self.humidity}"
    

