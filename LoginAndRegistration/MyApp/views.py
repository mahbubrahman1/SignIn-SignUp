from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# home function 
def home(request):
    user_info = {}

    if request.user.is_authenticated:
        user_id = request.user.id
        user_information = User.objects.get(pk=user_id)

        user_info = {'user_information': user_information}

    return render(request, 'MyApp/home.html', context=user_info)


# user sign up 
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # username validation
        if User.objects.filter(username=username):
            messages.warning(request, "That Username is taken! Try another.")
            return redirect('signup')

        # email validation 
        if User.objects.filter(email=email):
            messages.warning(request, "The email has already been taken. Try another.")
            return redirect('signup')
        
        # username validation two
        if not username.isalnum():
            messages.warning(request, "Username must be Alpha-Numeric!")
            return redirect('signup')

        # check first password and second password
        if password1 == password2:
            user = User.objects.create_user(username, email, password1)
            user.first_name = first_name
            user.last_name = last_name

            user.save()

            messages.success(request, "Your account has been successfully created. Now you can sign in.")
            return redirect('signup')
        
        else:
            messages.warning(request, "Password doesn't match. Try again.")

        return redirect('signup')

    else:
        return render(request, 'MyApp/signup.html')


# user sign in
def signin(request):
    if request.method == 'POST':
        signinusername = request.POST.get('signinusername')
        signinpassword = request.POST.get('signinpassword')

        # check username and password 
        user = authenticate(username=signinusername, password=signinpassword)

        # check user in database
        if user is not None:
            login(request, user)
            return redirect('home')
            
        else:
            messages.warning(request, "Invalid username or password")
            return redirect('signin')
            
    else:
        return render(request, 'MyApp/signin.html')


# sign out 
def signout(request):
    logout(request)
    return redirect('home')