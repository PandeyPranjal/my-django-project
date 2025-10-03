from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from adminapp.models import *


# Create your views here.
def index(request):
    context={
        'books': Book.objects.all(),#here we can add ne arrivals
        'new_arrivals':Book.objects.all()[:10],
        'userid':request.session.get('userid')
    }
    return render(request, 'index.html', context)
def about(request):
    context={
        'userid':request.session.get('userid')
    }
    return render(request, 'about.html',context)
def contact(request):
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        contactno=request.POST.get('contactno')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        enq=Enquiry(name=name, email=email, contactno=contactno, subject=subject, message=message)
        enq.save()
        
        messages.success(request, "Your enquiry has been submitted successfully.")
        return redirect('contact')
    context={
            'userid':request.session.get('userid'),#passed context
        }
    return render(request, 'contact.html',context)
def register(request):
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        contactno=request.POST.get('contactno')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword') #check 
        if password != cpassword:
            messages.error(request, "Password and confirm password doesn't match")
            return redirect ('register')
        ch=LoginInfo.objects.filter(username=email)
        if ch:
            messages.error(request, "Email already exists")
            return redirect('register')  ####
        log=LoginInfo(usertype="user", username=email, password=password)
        user=UserInfo(name=name, email=email, contactno=contactno,login=log)
        log.save()
        user.save()
        messages.success(request, "Your account has been created successfully.")
        return redirect('register')
    return render(request, 'register.html')
def login(request):
    if request.method == "POST":
        username= request.POST.get('username')
        password= request.POST.get('password')
        try:
            user= LoginInfo.objects.get(username=username,password=password,usertype="user")
            if user is not None:
                request.session['userid'] = username
                messages.success(request, "Welcome User!")
                return redirect('index')
        except LoginInfo.DoesNotExist:
            messages.error(request, "Invalid Credentials")
            return redirect('login')#here paste cntext
        context={
            'userid':request.session.get('userid'),
        }
    
    return render(request, 'login.html') #check here as I had to pass context 
def adminlogin(request):
    return render(request, 'adminlogin.html')
def adminlog(request):
    if request.method == "POST":
        username= request.POST.get('username')
        password= request.POST.get('password')
        try:
            admin= LoginInfo.objects.get(username=username,password=password,usertype="admin")
            if admin is not None:
                request.session['adminid'] = username
                messages.success(request, "Welcome Admin!")
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request, "Invalid Credentials")
            return redirect('adminlogin')
    else:
        return redirect('adminlogin')
    
    
def book_details(request, id):
    context={
        'book': Book.objects.get(id=id)
    }
    return render(request,'book_details.html', context)