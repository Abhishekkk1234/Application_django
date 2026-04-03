from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserFormData
from django.http import HttpResponse
from reportlab.pdfgen import canvas

# Signup
def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )
        return redirect('login')

    return render(request, 'signup.html')


# Login
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


# Logout
def logout_view(request):
    logout(request)
    return redirect('login')


# Home (form + save)
def home(request):
    if request.method == 'POST':
        UserFormData.objects.create(
            user=request.user,
            name=request.POST['name'],
            email=request.POST['email'],
            mobile=request.POST['mobile'],
            address=request.POST['address'],
            country=request.POST['country'],
            pincode=request.POST['pincode'],
            file=request.FILES['file']
        )
        return redirect('home')

    data = UserFormData.objects.filter(user=request.user)
    return render(request, 'home.html', {'data': data})


# PDF Download
def download_pdf(request, id):
    data = UserFormData.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="data.pdf"'

    p = canvas.Canvas(response)

    p.drawString(100, 800, f"Name: {data.name}")
    p.drawString(100, 780, f"Email: {data.email}")
    p.drawString(100, 760, f"Mobile: {data.mobile}")
    p.drawString(100, 740, f"Address: {data.address}")
    p.drawString(100, 720, f"Country: {data.country}")
    p.drawString(100, 700, f"Pincode: {data.pincode}")

    p.save()
    return response
