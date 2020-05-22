from django.shortcuts import render,redirect
import csv
from csv import writer
import os
import math
from django import template
import pandas as pd
import import_ipynb
from home.Book_recommendation_model_2 import sim_distance, get_recommendations 
from django.http import HttpResponse
from home.models import Cart,Interest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer


register = template.Library()

@register.filter
def round_up(value):
    return int(math.floor(value))





def rated(userId,bookId):
    ratings = pd.read_csv("C:\\Users\\trupti\\Desktop\\BookRack\\home\\ratings.csv",engine="python")
    ratings=ratings[ratings["user_id"]==int(userId)]
    ratings=ratings.values.tolist()
    j=0
    rat=0
    flag=False
    for i in ratings:
        if i[1]==int(bookId):
            rat=ratings[j][2]
            rat = rat*20
            flag=True
            break
        j=j+1
    if flag:
        l=[]
        l.append(flag)
        l.append(rat)
    else:
        l=[]
        l.append(flag)
        l.append(0)   
    return l 

def giveRating(rating,userId,bookId):
    ratings = pd.read_csv("C:\\Users\\trupti\\Desktop\\BookRack\\home\\ratings.csv",engine="python")
    ratings=ratings[ratings["user_id"]==int(userId)]
    ratings=ratings.values.tolist()
    j=0
    flag=False
    for i in ratings:
        if i[1]==int(bookId):
            flag=True
            break
    if  not flag:
        row=[int(userId),int(bookId),rating]
        with open("C:\\Users\\trupti\\Desktop\\BookRack\\home\\ratings.csv", 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow(row)

    



def recommend(bookid):
    book_description = pd.read_csv("C:\\Users\\trupti\\Desktop\\BookRack\\home\\book_data2.csv",engine="python")
    books_tfidf = TfidfVectorizer(stop_words='english')
    book_description['book_desc'] = book_description['book_desc'].fillna('')
    book_description_matrix = books_tfidf.fit_transform(book_description['book_desc'])
    #book_description_matrix.shape
    cosine_similarity = linear_kernel(book_description_matrix, book_description_matrix)
    similarity_scores = list(enumerate(cosine_similarity[bookid]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:6]
    books_index = [i[0] for i in similarity_scores]
    print (book_description['book_title'].iloc[books_index])
    viewdata = book_description.iloc[books_index].values.tolist()
    return viewdata


def product(request):
    return render(request,'product.html')


def index(request,booktitle=None,bookauthor=None):
    if 'loginuser' in request.session:
        sameauth={}
        data={}
        rbooks={}
        rbooks1=[]
        top1=[]
        mydata=pd.read_csv("C:\\Users\\trupti\\Desktop\\BookRack\\home\\book_data2.csv",engine="python")
        top=mydata.head(20)

        ratings = pd.read_csv("C:\\Users\\trupti\\Desktop\\BookRack\\home\\ratings.csv",engine="python")
        d = (ratings.groupby('user_id')['book_id','rating'].apply(lambda x: dict(x.values)).to_dict())

        uname=request.session["loginuser"]
        userId=request.session["userId"]

        # user=User.objects.get_by_natural_key(username=uname)
        
        #print(userid)
                
        #data=Interest.objects.filter(userid=userid)
        
        # for book in data:
        #     rbooks += recommend(book.bookid)
        data = ratings[ratings["user_id"]==userId]
        print(data)

        popular = mydata.sort_values(by=['book_rating'],ascending=False)
        popular = popular.head(10)
        
        if data.empty:
            print("empty")
            top=top.values.tolist()
            top1.append(top)
            sameauth["auth"]=top1
        else:
            print("not empty")
            rec_books = get_recommendations(d, userId)
            print(rec_books)
            for i in range(10):
                book_id = rec_books[i][1]
                rbooks=mydata[mydata["book_id"]== book_id]
                rbooks=rbooks.values.tolist()
                rbooks1.append(rbooks)

            #print(rbooks1)    
            sameauth["auth"]=rbooks1
        sameauth["auth2"]=popular.values.tolist()

        if 'viewbook' in request.POST:
            viewbookbtn=request.POST.get('viewbook') 
            id=int(viewbookbtn)
            viewdata=mydata[mydata["book_id"]==id]
            avgrating = viewdata["book_rating"]
            avgrating = int(avgrating)*20
            viewdata=viewdata.values.tolist()
            test=rated(1,id)
            
            
            #content based filtering
            book_description = pd.read_csv("C:\\Users\\trupti\\Desktop\\BookRack\\home\\book_data2.csv", encoding = 'latin-1')
            books_tfidf = TfidfVectorizer(stop_words='english')
            book_description['book_desc'] = book_description['book_desc'].fillna('')
            book_description_matrix = books_tfidf.fit_transform(book_description['book_desc'])
            cosine_similarity = linear_kernel(book_description_matrix, book_description_matrix)
            similarity_scores = list(enumerate(cosine_similarity[id-1]))
            similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            similarity_scores = similarity_scores[1:6]
            books_index = [i[0] for i in similarity_scores]
            #print (book_description.iloc[books_index])
            viewdata1 = book_description.iloc[books_index].values.tolist()
            return render(request,'product.html',{'viewbook':viewdata , 'viewbook1':viewdata1, 'avgrating': avgrating, 'test': test})


        #for giving ratings
        if 'link' in request.POST:
            rating=request.POST.get('rating')
            bookId=request.POST.get('bookId')
            test=rated(userId,bookId)
            if  not test[0]:
                test[0]=True
                test[1]=rating
                giveRating(rating,userId,bookId)
            id=int(bookId)
            viewdata=mydata[mydata["book_id"]==id]
            avgrating = viewdata["book_rating"]
            avgrating = int(avgrating)*20
            viewdata=viewdata.values.tolist()
            test=rated(1,id)
            
            
            #content based filtering
            book_description = pd.read_csv("C:\\Users\\trupti\\Desktop\\BookRack\\home\\book_data2.csv", encoding = 'latin-1')
            books_tfidf = TfidfVectorizer(stop_words='english')
            book_description['book_desc'] = book_description['book_desc'].fillna('')
            book_description_matrix = books_tfidf.fit_transform(book_description['book_desc'])
            cosine_similarity = linear_kernel(book_description_matrix, book_description_matrix)
            similarity_scores = list(enumerate(cosine_similarity[id-1]))
            similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            similarity_scores = similarity_scores[1:6]
            books_index = [i[0] for i in similarity_scores]
            #print (book_description.iloc[books_index])
            viewdata1 = book_description.iloc[books_index].values.tolist()
            return render(request,'product.html',{'viewbook':viewdata , 'viewbook1':viewdata1, 'avgrating': avgrating, 'test': test})
            


        #for search
        if 'sbutton' in request.POST:
            #print(request.POST.get('stype'))
            viewdata1 = []
            if (request.POST.get('stype') == '0'):
                title = request.POST.get('searchbox')
                viewdata = mydata[mydata['book_title'] == title ]
                viewdata = viewdata.values.tolist()
                viewdata1.append(viewdata)
                sameauth['auth'] = viewdata1
            if (request.POST.get('stype') == '1'):
                author = request.POST.get('searchbox')
                viewdata = mydata[mydata['book_author'] == author ]

                sameauth['auth'] = viewdata.values.tolist()
            return render(request, 'index.html', sameauth)
        
        return render(request,'index.html',sameauth)
    else:
        return redirect('account/login')
   

def wishlist(request):
    if 'loginuser' in request.session:
        viewdata={}
        viewdata1=[]
        uname=request.session["loginuser"]
        userId=request.session["userId"]
        ratings = pd.read_csv("C:\\Users\\trupti\\Desktop\\BookRack\\home\\ratings.csv",engine="python")
        books = pd.read_csv("C:\\Users\\trupti\\Desktop\\BookRack\\home\\book_data2.csv", encoding = 'latin-1')
        ratings = ratings[ratings["user_id"]==userId]
        for bookID in ratings["book_id"]:
            viewdata=books[books["book_id"]== bookID]
            viewdata=viewdata.values.tolist()
            viewdata1.append(viewdata)    
        

         
        return render(request,'wishlist.html',{'cartdisplay':viewdata1} )
    else:
        return redirect('account/login')     
    
    

