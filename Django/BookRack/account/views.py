from django.shortcuts import render,redirect
from django.contrib import messages
import pandas as pd
import csv
import itertools
from csv import writer
from django.contrib.auth.models import User,auth
from django.http import HttpResponseRedirect, HttpResponse


# Create your views here.
def userEntry(Fname,Lname,password,Email):
    userData=pd.read_csv("C:\\Users\\trupti\\Desktop\\BookRack\\account\\users.csv",engine="python")
    userId=int(userData['userId'].max())+1
    row=[userId,Fname,Lname,0,Email,password,0]
    with open('C:\\Users\\trupti\\Desktop\\BookRack\\account\\users.csv', 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(row)


def login(request):

    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        userData=pd.read_csv("C:\\Users\\trupti\\Desktop\\BookRack\\account\\users.csv",engine="python")
        userData=userData.values.tolist()
        for i in userData:
            if(i[4] == email and i[5] == password):
                request.session["loginuser"]= i[1]
                request.session["userId"]=i[0]
                return redirect('/')

        messages.info(request,'invalid credentials')
        return redirect('login')



        # user = auth.authenticate(username=username,password=password)

        # if user is not None:
        #     auth.login(request,user)
        #     print(username)
        #     request.session["loginuser"]=username
        #     print(request.session["loginuser"])
        #    # request.session['is_logged']= True
        #     return redirect("/")

        # else:
        #     messages.info(request,'invalid credentials')
        #     return redirect('login')
    else:    
        return render(request,'login.html')
def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2'] 
        email = request.POST['email']
   
        if password1==password2:
            userEntry(first_name,last_name,password1,email)
            return redirect('login')    
        else:
            messages.info(request,'Password and Confirm password are not matching')
            return redirect('register')
    else:
        return render(request,'register.html')


        # if password1==password2:
        #     if  User.objects.filter(username=username).exists():
        #         messages.info(request,'Username taken')
        #         return redirect('register')
        #     elif User.objects.filter(email=email).exists():
        #         messages.info(request,'email taken')
        #         return redirect('register')    
        #     else:
        #         user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
        #         user.save()
        #         request.session["uname"]=username
        #         print('user created')
        #         return redirect('login')

        # else:
        #     print('password not matching.....')
        #     return redirect('register')
    
def logout(request):
    if 'loginuser' in request.session:
        del request.session['loginuser']
        del request.session['userId']
        #auth.logout(request)
        return HttpResponseRedirect('login')
    else:
        return redirect('login')        



   