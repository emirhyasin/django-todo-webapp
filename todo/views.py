from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import TodoForm, SignUpForm
from .models import Todo
import requests
from datetime import datetime

def home(request):
    form = TodoForm(request.POST or None)
    if request.user.is_authenticated:
        form = TodoForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
                todo = form.save(commit=False)
                todo.user = request.user
                todo.save()
                messages.add_message(request, messages.SUCCESS, "Todo added successfully.")
                return redirect("home")
            
        todos = Todo.objects.filter(user=request.user, completed=False)
    else:
        todos = []
    return render(request, "home.html", {"form": form, "todos": todos})

def weather(request):
    try:
        if request.method == "POST":
            API_KEY = 'YOUR_API_KEY'
            city = request.POST["city"]
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
            response = requests.get(url).json()
            time = datetime.now().strftime("%A, %B %d %Y, %H:%M:%S %p")
            city_weather = {
                'city': city,
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
                'temperature': 'Temperature: ' + str(response['main']['temp']) + ' °C',
                'country': response['sys']['country'],
                'wind': 'Wind: ' + str(response['wind']['speed']) + ' km/h',
                'humidity': 'Humidity: ' + str(response['main']['humidity']) + ' %',
                'time': time
            }
        else:
            city_weather = None
        context = {'city_weather': city_weather}
        return render(request, "weather.html", context)
    except:
        return render(request, "weather.html", {"error": "City not found."})

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            remember_me = request.POST.get("remember")
            if remember_me:
                request.session.set_expiry(60*60*24*30)
            else:
                request.session.set_expiry(0)
            messages.add_message(request, messages.SUCCESS, "You have successfully logged in.")
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, "Email or password is incorrect.")
            return redirect('login')
    else:
        return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "You have successfully logged out.")
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password=password)
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "You have successfully registered.")
            return redirect('home')
    return render(request, "register.html", {"form": form})

@login_required
def todo_delete(request, pk):
        todo = get_object_or_404(Todo, id=pk, user=request.user)
        todo.delete()
        messages.add_message(request, messages.SUCCESS, "Todo deleted successfully.")
        return redirect("home")

def todo_complete(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.completed = True
    todo.save()
    messages.add_message(request, messages.SUCCESS, "Todo status updated successfully.")
    return redirect("home")

def completed_todos(request):
    todos = Todo.objects.filter(user=request.user, completed=True)
    return render(request, "completed_todos.html", {"todos": todos})

def todo_list(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TodoForm()
    
    todo_cards = Todo.objects.all()
    
    return render(request, "todo_list.html", {"form": form, "todo_cards": todo_cards})

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            
            try:
                user = User.objects.get(username=username)
                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "Your password has been updated successfully.")
                    return redirect('home')
                else:
                    messages.error(request, "Current password is incorrect.")
            except User.DoesNotExist:
                messages.error(request, "User not found.")
    else:
        form = ChangePasswordForm()
    
    return render(request, 'change_password.html', {'form': form})