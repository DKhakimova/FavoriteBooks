from django.shortcuts import render, redirect
from .models import Book
from log_reg_app.models import User
from django.contrib import messages

# Create your views here.

def books(request):
    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'books': Book.objects.all()
    }
    return render(request, 'books.html', context)

def create(request):
    if request.method == "POST":
        errors = Book.objects.validate(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')

        else: 
            title = request.POST['title']
            description = request.POST['description']
            user = User.objects.get(id=request.session['user_id'])
            book = Book.objects.create(title=title, description=description, uploaded_by=user)
            user.liked_books.add(book)
            return redirect('/books')

def favorite(request, book_id):
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=book_id)
    user.liked_books.add(book)
    return redirect(f"/books/{book.id}")

def unfavorite(request, book_id):
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=book_id)
    user.liked_books.remove(book)
    return redirect(f"/books/{book.id}")

def update(request, book_id):
    if request.method == "POST":
        book = Book.objects.get(id=book_id)
        book.title = request.POST['title']
        book.description = request.POST['description']

        errors = Book.objects.validate(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/books/{book.id}")
        else:
            book.save()
            return redirect(f"/books/{book.id}")

def delete(request, book_id):
    if request.method == "POST":
        book = Book.objects.get(id=book_id)
        book.delete()
        return redirect('/books')

def show(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    users_who_like = book.users_who_like.all()
    context = {
        'user': user,
        "book": book,
        "users_who_like": users_who_like
    }
    if user == book.uploaded_by:
        return render(request, 'edit.html', context)
    return render(request, 'show.html', context)