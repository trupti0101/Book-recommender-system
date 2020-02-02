from django.shortcuts import render, redirect
from .models import Book
from .forms import BookCreate
from django.http import HttpResponse
import csv
import os
from django import template

from django.http import StreamingHttpResponse



#DataFlair
def index(request):
	shelf = Book.objects.all()
	path = os.path.dirname(__file__)
	file = os.path.join(path, 'book_data.csv')

	with open(file) as csv_file:
		shelf = csv.reader(csv_file, delimiter=',')
		line_count = 0
		books = []
    #     See your console/terminal
		for row in shelf:
			if line_count == 0:
				#print('\n\nColumn names are {}, {}, {}, {}'.format(row[0], row[1], row[3], row[2]))
				books.append(row)
				line_count += 1
			else:
				#print('\t{} {} lives in {}, and his phone number is {}.'.format(row[0], row[1], row[3], row[2]))
				line_count += 1
				books.append(row)
				if line_count == 2:
					break
			print('Processed {} lines.\n\n'.format(line_count))
			print(books)


	#shelf = Book.objects.all()
		return render(request, 'book/library.html', {'author': books[1][0], 'image':books[1][11], 'shelf':books})
	#return render(request, 'book/library.html', {'shelf':shelf})

register = template.Library()

@register.filter
def index(List, i):
    return List[int(i)]

@register.filter
def row_length(List):
    return range(len(List))


def upload(request):
	upload = BookCreate()
	if request.method == 'POST':
		upload = BookCreate(request.POST, request.FILES)
		if upload.is_valid():
			upload.save()
			return redirect('index')
		else:
			return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
	else:
		return render(request, 'book/upload_form.html', {'upload_form':upload})

def update_book(request, book_id):
	book_id = int(book_id)
	try:
		book_sel = Book.objects.get(id = book_id)
	except Book.DoesNotExist:
		return redirect('index')
	book_form = BookCreate(request.POST or None, instance = book_sel)
	if book_form.is_valid():
		book_form.save()
		return redirect('index')
	return render(request, 'book/upload_form.html', {'upload_form':book_form})

def delete_book(request, book_id):
	book_id = int(book_id)
	try:
		book_sel = Book.objects.get(id = book_id)
	except Book.DoesNotExist:
		return redirect('index')
	book_sel.delete()
	return redirect('index')



















# def details(request, book_id):
# 	book_id = int(book_id)
# 	try:
# 		book_sel = Book.objects.get(id = book_id)
# 	except Book.DoesNotExist:
# 		return redirect('index')
# 	url = book_sel.picture.url
# 	return render(request, 'book/details.html', {'book':book_sel, 'url':url})
