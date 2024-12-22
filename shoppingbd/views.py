from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User # this table already exists in django we import it 
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.core.mail import EmailMessage

def register(request):
    if request.method=='POST':
        fname = request.POST['fname']
        lname=request.POST['lname'] #request.post[id of the input field]
        email = request.POST['email']
        password = request.POST['pass']
        password2 = request.POST['confirmpass']
        agree=request.POST.get('agree')
        if fname == '':
             messages.warning(request, 'Please enter First name!')
             return redirect('register')

        if lname == '':
             messages.warning(request, 'Please enter Last name!')
             return redirect('register')

        if email == '':
             messages.warning(request, 'Please enter Email!')
             return redirect('register')

        if password == '':
             messages.warning(request, 'Please enter Password!')
             return redirect('register')

        if password2 == '':
             messages.warning(request, 'Please enter Confirm Password!')
             return redirect('register')
        if ('agree' not in request.POST):
             messages.warning(request, 'Please agree to our terms and conditions!')
             return redirect('register')

        if password==password2:

            if User.objects.filter(username=email):
                messages.error(request,"Email Already Exists")
                return redirect('register')
            else:
                user=User.objects.create_user(username=email,first_name=fname,last_name=lname,password=password) #these are postgres first_name,last_name
                user.save()
                messages.success(request,"Successfully Registered")
                subject = 'Site Contact Form'
                contact_message = "%s : %s via %s "%(fname, lname, email)
                from_email = settings.EMAIL_HOST_USER
                to_email = [from_email, 'myotheremail@gmail.com']
                send_mail(subject, contact_message, from_email, to_email, fail_silently=False)
    
                return redirect('login')
        
        

        else:
            messages.error(request,"Passwords don't match")
            return redirect('register')
    else:
        return render(request, 'signupdiv.html')