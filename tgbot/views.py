from django.http import HttpResponse, HttpRequest

def home(request: HttpRequest):
    return HttpResponse('<b>Hello</b> world')
