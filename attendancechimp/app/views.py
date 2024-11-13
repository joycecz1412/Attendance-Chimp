from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Course, People, Lecture, QR_Codes


def team_bio_view(request):
    current_user = request.user.username if request.user.is_authenticated else "Not Logged In"
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

@csrf_exempt
def new_course(request):
    return render(request, 'app/new_course.html'  )

@csrf_exempt
def new_lecture(request):
    return render(request, 'app/new_course.html'  )

@csrf_exempt
def new_qr_upload(request):
    return render(request, 'app/new_qr_upload.html')

@csrf_exempt
@login_required
@require_POST
def create_course(request):
    if not request.user.is_authenticated or not request.user.People.is_instructor:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    instructor_id = request.POST.get('instructor_id')
    course_ID = request.POST.get('course_ID')
    days_of_week = [request.Post.get(day_key) for day_key in ['day-mon', 'day-tue', 'day-wed', 'day-thu', 'day-fri'] if request.POST.get(day_key)]
    start_time = request.POST.get('start-time')
    end_time = request.POST.get('end-time')

    try:
        instructor = People.objects.get(id=instructor_id, is_instructor=True)
    except People.DoesNotExist:
        return JsonResponse({"error": "Unauthorized or invalid instructor"}, status=403)

    new_course = Course(name=name, start_time=start, end_time=end_time, days=days_of_week, instructor=request.user)
    new_course.save()
    
    return JsonResponse({"status": "success", "course_id": new_course.course_ID})

@csrf_exempt
@login_required
@require_POST
def create_lecture(request):
    if not request.user.is_authenticated or not request.user.People.is_instructor:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    course_id = request.POST.get('choice') 
    course = Course.objects.get(name=course_id)
    lecture_time = datetime.now()

    try:
        course = Course.objects.get(course_ID=course_id)
    except Course.DoesNotExist:
        return JsonResponse({"error": "Course does not exist"}, status=404)

    new_lecture = Lecture(course=course_instance, lecture_date=datetime.now())
    new_lecture.save()
    return JsonResponse({"status": "success, lecture created"})
    
@csrf_exempt
@login_required
@require_POST
def create_qr_code_upload(request):
    if request.user.People.is_instructor:
        return HttpResponse(status=401)
    image = request.FILES.get('imageUpload')
    qr_upload = Upload(user=request.user, qr_code=image)
    qr_upload.save()
    return JsonResponse({'message': 'QR code uploaded successfully'}, status=200)
    

def dumpUploads(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=403)
    if request.method != 'GET':
        return HttpResponseForbidden("Only GET requests are allowed.")
    if not request.user.People.is_instructor: 
        return HttpResponse(status=403)

    uploads = Upload.objects.all().values('user__username', 'upload_time')
    upload_data = [{"username": entry['user__username'], "upload_time": entry['upload_time']} for entry in uploads]
    return JsonResponse(upload_data, safe=False)
