from django.shortcuts import render
from .models import SubscribedEmail

# Create your views here.
class NewsletterView(View):
    def post():
        email = request.POST.get('email')
        if email:
            if SubscribedEmail.objects.filter(email=email).exists():
                msg = f"This '{email}' email has already Subscribed. No need to Subscribe again."
                context = {'msg': msg}
            else:
                SubscribedEmail.save_email(email)
                msg = "Thank's for your Subscription. Every updates will be now Notify."
                context = {'msg': msg}
        return render(request, 'newsletter.html', context)
