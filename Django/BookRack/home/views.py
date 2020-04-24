from django.shortcuts import render,redirect
import csv
import os
from django import template
import pandas as pd
import import_ipynb
from django.http import HttpResponse
from home.models import Cart,Interest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer



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

@login_required
def index(request,booktitle=None,bookauthor=None):
    
    path = os.path.dirname(__file__)
    file = os.path.join(path, 'book_data.csv')
    sameauth={}
    data={}
    rbooks=[]
    mydata=pd.read_csv("C:\\Users\\trupti\\Desktop\\BookRack\\home\\book_data2.csv",engine="python")
    top=mydata.head(20)


    uname=request.session["loginuser"]
    user=User.objects.get_by_natural_key(username=uname)
    userid=user.id
    print(userid)
            
    data=Interest.objects.filter(userid=userid)
    for book in data:
        rbooks += recommend(book.bookid)


    popular = mydata.sort_values(by=['book_rating'],ascending=False)
    popular = popular.head(10)
    if not data:
        sameauth["auth"]=top.values.tolist()
    else:
        sameauth["auth"]=rbooks
    sameauth["auth2"]=popular.values.tolist()


    
    if request.method == 'GET':
       
        if request.GET.get('booklikeid'):
            
            uname=request.session["loginuser"]
            user=User.objects.get_by_natural_key(username=uname)
            userid=user.id
            like=request.GET.get('booklikeid')
            print("like bookid=",like)
            bid=int(like)
            likedata=mydata[mydata["book_id"]==bid]
            listdata=likedata.values.tolist()
            print(listdata)
            title=listdata[0][10]
            author=listdata[0][1]
            genre=listdata[0][11]
            desc=listdata[0][2]
            image=listdata[0][12]
            print(title)
            add=Interest(userid=userid,bookid=bid,booktitle=title,bookgenres=genre,bookauthor=author,bookdesc=desc,bookimage=image)
            add.save()
            #messages.success(request,"added to like")
        if request.GET.get('bookid'):

            viewbook=request.GET.get('bookid')
            print("viewbookis====",viewbook)
            id=int(viewbook)
            viewdata=mydata[mydata["book_id"]==id]
            viewdata=viewdata.values.tolist()
            
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
            return render(request,'product.html',{'viewbook':viewdata , 'viewbook1':viewdata1})
    
    if 'viewbook' in request.POST:
        viewbookbtn=request.POST.get('viewbook') 
        id=int(viewbookbtn)
        viewdata=mydata[mydata["book_id"]==id]
        viewdata=viewdata.values.tolist()
        
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
        return render(request,'product.html',{'viewbook':viewdata , 'viewbook1':viewdata1})

    if 'sbutton' in request.POST:
        print(request.POST.get('stype'))
        if (request.POST.get('stype') == '0'):
            title = request.POST.get('searchbox')
            viewdata = mydata[mydata['book_title'] == title ]
            sameauth['auth'] = viewdata.values.tolist()
        if (request.POST.get('stype') == '1'):
            author = request.POST.get('searchbox')
            viewdata = mydata[mydata['book_author'] == author ]
            sameauth['auth'] = viewdata.values.tolist()
        return render(request, 'index.html', sameauth)
    return render(request,'index.html',sameauth)
   

@login_required
def wishlist(request):
    
    if request.method == 'GET':
            print("sddaddd")
            bookid=request.GET.get("bookid")
            
            uname=request.session["loginuser"]
            user=User.objects.get_by_natural_key(username=uname)
            userid=user.id
            print("---->",bookid)
            removebook=Interest.objects.filter(bookid=bookid)
            if removebook.delete():
                print("book is removed")
                data=Interest.objects.filter(userid=userid)
                print(data)
                
                return render(request,'wishlist.html',{'cartdsiplay':data} ) 
            
    else:
            cartdsiplay=Interest.objects.all()
            return render(request,'wishlist.html',{'cartdsiplay':cartdsiplay} )
    return render(request,'index.html') 


