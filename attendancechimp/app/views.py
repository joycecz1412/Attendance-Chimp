from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


def team_bio_view(request):
    current_user = request.user.username if request.user.is_authenticated else "Guest"
    bios = [
        {"name": "Joyce", "description": "Fourth Year Econ & DS Major"},
        {"name": "Minseo", "description": "Third Year Econ & DS Major"},
    ]
    current_time = timezone.localtime(timezone.now())
    context = {
        "current_user": current_user, 
        "bios": bios,
        "current_time": current_time.now().strftime("%Y-%m-%d %H:%M:%S")  # Format current time
    }
    
    return render(request, "app/index.html", context)

def new_user_form(request):
    if request.method == 'GET':
        return render(request, 'app/new_user_form.html')
    else:
        return HttpResponseBadRequest("This page only accepts GET requests.")


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        is_student = request.POST.get('is_student') == '1'

        if User.objects.filter(email=email).exists():
            return HttpResponseBadRequest("A user with this email already exists.")

        user = User.objects.create_user(username=user_name, email=email, password=password)
        user.save()
        return JsonResponse({"message": "User created successfully!"})
    else:
        return HttpResponseBadRequest("This page only accepts POST requests.")


