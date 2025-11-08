from django.http import HttpResponse

def home_page(request, user_name):
    return HttpResponse(f"Hello, {user_name}")