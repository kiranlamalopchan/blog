from django.db import models

class SubscribedEmail(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


    @staticmethod
    def get_all_email():
        return SubscribedEmail.objects.all()

    @staticmethod
    def save_email(email):
        email_object = SubscribedEmail(email= email)        
        return email_object.save()


