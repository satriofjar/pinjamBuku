from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . models import Book, Rent, Message
from .utils import is_staf
from .forms import BookForm, UserForm, MessageForm

# Create your views here.
@login_required(login_url='login')
def index(request):
    books = Book.objects.filter(is_available=True)
    rents = Rent.objects.filter(user=request.user, is_active=True)
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'books': books, 
        'rents': rents,
        'form': form,
    }
    return render(request, 'base/index.html', context)


@login_required(login_url='login')
def rent_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    if book.is_available:
        if request.user.is_authenticated:
            rent = Rent.objects.create(
                user=request.user, 
                book=book)
            rent.save()
            book.is_available = False
            book.save()
            return redirect('home')
    

@user_passes_test(is_staf, login_url='login')
def dashboard(request):
    books = Book.objects.all()
    # rents = books.rent_set.filter(is_available=False)
    rents = Rent.objects.filter(is_active=True)
    users = User.objects.all()
    messages = Message.objects.all()

    context = {
        'books': books, 
        'rents': rents,
        'users': users,
        'messages': messages,
    }

    return render(request, 'base/dashboard.html', context)


@user_passes_test(is_staf, login_url='login')
def make_staff(request, pk):
    user = get_object_or_404(User, id=pk)
    user.is_staff = True
    user.save()
    return redirect('dashboard')


@user_passes_test(is_staf, login_url='login')
def demote_staff(request, pk):
    user = get_object_or_404(User, id=pk)
    user.is_staff = False
    user.save()
    return redirect('dashboard')

@user_passes_test(is_staf, login_url='login')
def return_book(request, pk):
    rent = get_object_or_404(Rent, id=pk)
    rent.is_active = False
    rent.save()

    book = get_object_or_404(Book, id=rent.book.id)
    book.is_available = True
    book.save()

    return redirect('dashboard')


@user_passes_test(is_staf, login_url='login')
def add_book(request):
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            messages.error(request, form.errors)
        
    context = {
        'form': form,
    }

    return render(request, 'base/book-form.html', context)


@user_passes_test(is_staf, login_url='login')
def edit_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    form = BookForm(instance=book)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        print('test')
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        
    context = {
        'form': form,
    }

    return render(request, 'base/book-form.html', context)


@user_passes_test(is_staf, login_url='login')
def delete_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    book.delete()
    return redirect('dashboard')



def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Email or password incorrect')
            return redirect('login')
        
    context = {
        'page': 'login',
    }
    return render(request, 'base/register.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')


def register(request):
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()

            login(request, user)
            return redirect('home')
         
        else:
            messages.error(request, form.errors)

    context = {
        'form': form,
    }
    return render(request, 'base/register.html', context)