from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Course, People, Lecture, QR_Codes, getUploadsForCourse
from django.shortcuts import get_object_or_404 
import secrets
import string
from pyzbar.pyzbar import decode
from PIL import Image
import io

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
        new_person = People(user=user, is_instructor=not is_student)
        user.save()
        new_person.save()
        return JsonResponse({"message": "User created successfully!"})
    else:
        return HttpResponseBadRequest("This page only accepts POST requests.")

@csrf_exempt
def new_course(request):
    return render(request, 'app/new_course.html'  )

@csrf_exempt
def new_lecture(request):
    courses = Course.objects.all()
    return render(request, 'app/new_lecture.html', {'courses': courses})

@csrf_exempt
def new_qr_upload(request):
    return render(request, 'app/new_qr_upload.html')

@csrf_exempt
@login_required
@require_POST
def create_course(request):
    if not request.user.is_authenticated or not request.user.people.is_instructor:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    course_id = request.POST.get('course-name')
    days_of_week = [request.POST.get(day_key) for day_key in ['day-mon', 'day-tue', 'day-wed', 'day-thu', 'day-fri'] if request.POST.get(day_key)]
    start_time = request.POST.get('start-time')
    end_time = request.POST.get('end-time')

    new_course = Course(course_id=course_id, start_time=start_time, end_time=end_time, days=days_of_week, instructor=request.user.people)
    new_course.save()
    
    return JsonResponse({"status": "success", "course_id": new_course.course_id})

@csrf_exempt
@login_required
@require_POST
def create_lecture(request):
    if not request.user.is_authenticated or not request.user.people.is_instructor:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    
    course_id = request.POST.get('choice')

    if not course_id:
        return JsonResponse({"error": "No course selected"}, status=400)

    try:
        course = Course.objects.get(course_id=course_id)

        lecture_time = timezone.now()
        qrdata = request.POST.get('qr_code_string')
        if not qrdata:
            characters = string.ascii_letters + string.digits + string.punctuation
            random_string = ''.join(secrets.choice(characters) for _ in range(16))
            qrdata = random_string
        new_lecture = Lecture(course=course, lecture_time=lecture_time, qrdata=qrdata)
        new_lecture.save()
        return JsonResponse({"status": "success", "message": "Lecture created successfully"})
    except Course.DoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=404)
    
@csrf_exempt
@login_required
@require_POST
def create_qr_code_upload(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    if request.user.people.is_instructor:
        return HttpResponse(status=401)
    upload = request.FILES.get('imageUpload')
    try:
        image = Image.open(upload)
        qr_code = decode(image)
        if qr_code: 
            qr_data = qr_code[0].data.decode("utf-8")
            lecture = Lecture.objects.filter(qrdata=qr_data).first()
            if not lecture:
                return JsonResponse({'status': 'error', 'message': 'No matching lecture found for the QR code.'}, status=404)
            qr_upload = QR_Codes(uploader=request.user, qr_code=qr_data, 
                                 time_uploaded=timezone.now(), lecture=lecture)
            qr_upload.save()
            return JsonResponse({'message': 'QR code uploaded successfully'}, status=200)
        else:
            return JsonResponse({"status": "error", "message": "No QR code found."}, status=400)
    except Exception as e:
            return JsonResponse({"status": "error", "message": f"Error decoding QR code: {str(e)}"})   

def dumpUploads(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    if request.method != 'GET':
        return HttpResponseForbidden("Only GET requests are allowed.")
    if not request.user.people.is_instructor: 
        return HttpResponse(status=401)

    uploads = QR_Codes.objects.all().values('uploader', 'time_uploaded')
    upload_data = [{"username": entry['uploader'], "time_uploaded": entry['time_uploaded']} for entry in uploads]
    return JsonResponse(upload_data, safe=False)

def getUploads(request):
    course_id = request.GET.get('course')
    if not course_id:
        return JsonResponse({"error": "The 'course' parameter is required and cannot be empty."}, 
                            status=400)
    uploads = getUploadsForCourse(course_id)
    upload_data = [{"uploader": qr.uploader, "time_uploaded": qr.time_uploaded}
                   for qr in uploads]
    return JsonResponse({"uploads": upload_data})