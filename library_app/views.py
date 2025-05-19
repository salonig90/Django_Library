from django.shortcuts import render,redirect
from .models import Book
from .forms import AdminSignupForm
from django.contrib import messages

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm 

# Create your views here.
def home(request):
    return render(request,'home.html')

def student_view(request):
    books_data = Book.objects.all()
    context= {'book': books_data}
    return render(request, 'student_view.html', context )
    

# Retrieve all books
def all_books(request):
    books_data = Book.objects.all()
    context= {'book': books_data}
    return render(request, 'all_books.html', context )


# Create a book entry
def create_book(request):
    if request.method == 'POST':   # submits the data to the server
        title = request.POST['title']
        author = request.POST['author']
        published_date = request.POST['published_date']
        isbn_number = request.POST['isbn_number']
        
        # Create the book record
        book = Book(title= title,author = author,published_date=published_date,isbn_number=isbn_number)

        book.save()
        return redirect('all_books')
    return render(request, 'create_book.html')



# Update a book entry
def update_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.published_date = request.POST['published_date']
        book.isbn_number = request.POST['isbn_number']
        book.save()

        return redirect('/all_books')
    else:
        context = { 'book' : book }
        return render(request, 'update_book.html', context)

# Delete a book entry
def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('/all_books')

# Admin signup view

def adminsignup(request):
    if request.method == 'POST':
        fm=AdminSignupForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,"Account created succesfully")
            return redirect('adminsignin')
        
        else:
            messages.error(request,"Invalid data")
    else:
        fm= AdminSignupForm() #empty object 
    return render(request,'adminsignup.html',{'rg':fm })

def adminsignin(request):
    if request.method == "POST":
        fm = AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                return render(request,'aftersignin.html',{'user': user })
    else:
        fm = AuthenticationForm()
    return render(request,"adminsignin.html",{'user_data':fm})

def aftersignin(request):
    return render(request,'aftersignin.html')

def logout_view(request):
    logout(request)
    return redirect("home")
