from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.http import HttpResponseRedirect, HttpResponse


# Create your views here.
def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            print(username)
            request.session["loginuser"]=username
            print(request.session["loginuser"])
           # request.session['is_logged']= True
            return redirect("/")

        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:    
        return render(request,'login.html')
def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username'] 
        password1 = request.POST['password1']
        password2 = request.POST['password2'] 
        email = request.POST['email']
       # Interest = request.POST['Interest']
        # if request.POST.get('interest'):
        #     data=request.POST['interest']
        #     print(data)
        # else:
        #     print("not selected")


        if password1==password2:
            if  User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return redirect('register')    
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                request.session["uname"]=username
                print('user created')
                return redirect('login')

        else:
            print('password not matching.....')
            return redirect('register')
    else:
        return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
     #if request.session.has.key('is_logged'):       




   