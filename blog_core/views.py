from django.shortcuts import HttpResponse


def show_home(request):
    return HttpResponse("There will be posts here")


def show_post(request):
    return HttpResponse("There will be post here")
