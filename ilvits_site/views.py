from django.shortcuts import render


def homepage(request):
    return render(request, 'home.html')


def portfolio(request):
    return render(request, 'portfolio.html')


def contact(request):
    return render(request, 'contact.html')



