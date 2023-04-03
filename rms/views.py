from os import stat
from django.shortcuts import render
from django.views import View

# Create your views here.


class ResultView(View):
    @staticmethod
    def get(request):
        context = {}
        return render(request, 'result.html', context)
