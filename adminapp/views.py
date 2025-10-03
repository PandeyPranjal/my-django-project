from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from home.models import * 
from .models import *
from decimal import Decimal
from userapp.models import *
from django.views.decorators.cache import cache_control
#changes made in viewcat 'cat':cats

# Create your views here.
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def admindash(request):
    if 'adminid' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('adminlogin')
    adminid= request.session.get('adminid')
    context={
        'adminid':adminid,
        'user_count':UserInfo.objects.all().count(),
        'book_count':Book.objects.all().count(),
        'cat_count':Category.objects.all().count(),
        'order_count':Order.objects.all().count(), #here is raising error
        'enq_count':Enquiry.objects.all().count(),
    }
    return render(request, 'admindash.html',context)
def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request, "You are logged out.")
        return redirect('adminlogin')
    else:
        return redirect('adminlogin')
    
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
    
def viewenqs(request):
    if 'adminid' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('adminlogin')
    adminid= request.session.get('adminid')
    enqs=Enquiry.objects.all()
    context={
        'adminid':adminid,
        'enqs':enqs
    }
    return render(request, 'viewenqs.html',context)


def delenq(request,id):
    if 'adminid' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('adminlogin')
    enq=Enquiry.objects.get(id=id)
    enq.delete()
    messages.success(request, "Message deleted Successfully")#####
    return redirect ('viewenqs')

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def addcat(request):#fun name addcat
    if 'adminid' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('adminlogin')
    adminid= request.session.get('adminid')
    context={
        'adminid':adminid,
    }
    if request.method=="POST":
        name=request.POST.get('name')
        description=request.POST.get('description')
        cats=Category(name=name, description=description)
        cats.save()
        messages.success(request, "Category added  successfully")
        return redirect('addcat')
        
    
    return render(request, 'addcat.html',context)#


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def viewcat(request): #viwcat
    if 'adminid' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('adminlogin')
    adminid= request.session.get('adminid')
    cats=Category.objects.all()
    context={
        'adminid':adminid,
        'cat':cats,        #this is added after everryting
    }
    return render(request, 'viewcat.html',context)


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def addbook(request): #addbook
    if 'adminid' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('adminlogin')
    adminid= request.session.get('adminid')
    cats=Category.objects.all()
    context={
        'adminid':adminid,
        'cats':cats,
    }
    if request.method=="POST":
        title=request.POST.get('title')
        author=request.POST.get('author')
        category=request.POST.get('category')
        cats= Category.objects.get(id=category)   #check it and it must be added
        description=request.POST.get('description')
        original_price=request.POST.get('original_price')
        price=request.POST.get('price')
        published_date=request.POST.get('published_date')
        language=request.POST.get('language')
        cover_image=request.FILES.get('cover_image')
        stock=request.POST.get('stock')
        b=Book(
            title=title,
            author=author,
            category=cats,
            description=description,
            original_price=original_price,
            price=price,
            published_date=published_date,
            language=language,
            cover_image=cover_image,
            stock=stock
            
        )
        b.save()
        messages.success(request,"Book added successfully")
    return render(request, 'addbook.html',context)


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def viewbook(request): #viewbook
    if 'adminid' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('adminlogin')
    adminid= request.session.get('adminid')####
    book=Book.objects.all()
    context={
        'adminid':adminid,
        'book':book,
    }
    return render(request, 'viewbook.html',context)

def delbook(request,id):
    if 'adminid' not in request.session:
        messages.error(request,'Inavlid Session')
        return redirect('adminlogin')
    book = Book.objects.get(id = id)
    book.delete()
    messages.success(request,"Book Deleted")
    return redirect('viewbook')

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def editbook(request,id):
    if 'adminid' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('adminlogin')
    adminid= request.session.get('adminid')
    book=Book.objects.get(id=id)
    cats=Category.objects.all()
    context={
        'adminid':adminid,
        'book':book,
        'cats':cats, ####check here too
    }
    if request.method=="POST":
        title=request.POST.get('title')
        author=request.POST.get('author')
        category=request.POST.get('category')
        cat= Category.objects.get(id=category)   #check it and it must be added here should be cat
        description=request.POST.get('description')
        original_price=request.POST.get('original_price')
        price=request.POST.get('price')
        published_date=request.POST.get('published_date')
        language=request.POST.get('language')
        cover_image=request.FILES.get('cover_image')
        stock=request.POST.get('stock')
        book.title=title
        book.author=author
        book.category=cat
        book.description=description
        book.original_price=original_price
        book.price=price
        if published_date:
            book.published_date=published_date
        book.language=language
        if cover_image:
            book.cover_image=cover_image
        book.stock=stock
        book.save()
        messages.success(request, f"{title} is updated successfully")
        return redirect('viewbook')
   
    return render(request, 'editbook.html',context)
def delcat(request,id):
    if 'adminid' not in request.session:
        messages.error(request,'Session Timed Out')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    cat=Category.objects.get(id=id)
    cat.delete()
    messages.success(request,"Successfully Deleted")
    return redirect('viewcat')


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def changepassword(request):
    # Session check
    if 'adminid' not in request.session:
        messages.error(request, "You are not logged in.")
        return redirect('adminlogin')
    
    adminid = request.session.get('adminid')
    
    # Safely fetch LoginInfo object
    info = get_object_or_404(LoginInfo, username=adminid)
    
    context = {
        'adminid': adminid,
        'info': info,
    }
    
    if request.method == "POST":
        old_pass = request.POST.get('oldpassword')
        new_pass = request.POST.get('newpassword')
        confirm_pass = request.POST.get('confirmpassword')
        
        # Old password check
        if old_pass != info.password:
            messages.error(request, "Incorrect Old Password")
            return redirect('changepassword')
        
        # New password should not be same as old
        if old_pass == new_pass:
            messages.error(request, "Old and new password should not be same")
            return redirect('changepassword')
        
        # Confirm password check
        if new_pass != confirm_pass:
            messages.error(request, "Confirm password and new password are not same")
            return redirect('changepassword')
        
        # Save new password
        info.password = new_pass
        info.save()
        messages.success(request, "Password changed successfully")
        return redirect('changepassword')
    
    return render(request, 'changepassword.html', context)


# def changepassword(request):
#     if 'adminid' not in request.session:
#         messages.error(request,"You are not logged in.")
#         return redirect('adminlogin')
#     adminidd=request.session.get('adminid')
#     info=LoginInfo.objects.get(username=adminidd)
    
#     context={
#         'adminid':adminidd,
#         'info':info,
        
#     }
    
#     if request.method=="POST":
        
#         if info:
#             passs=request.POST.get('oldpassword')
#             if(passs!=info.password):
#                 messages.error(request,"Incorrect Old Password")
#                 return redirect('changepassword')
#             npasss=request.POST.get('newpassword')
#             if(passs==npasss):
#                 messages.error(request,"Old and new password should not be same")
#                 return redirect('changepassword')
#             cn=request.POST.get('confirmpassword')
#             if npasss!=cn:
#                 messages.error(request,"confirm password and new password are not same")
#                 return redirect('changepassword')
#             info.password=npasss
#             info.save()
#             messages.success(request,"Password changed Successfully")
#             return redirect('changepassword')
#         else:
#             messages.error(request,"Not such entry found")
#             return redirect('changepassword')
#     return render(request,'changepassword.html',context)