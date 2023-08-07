from django.shortcuts import render


def index(request):
    return render(request, 'statuses.html')


def create(request):
    pass


def delete(request):
    pass


def update(request):
    pass

