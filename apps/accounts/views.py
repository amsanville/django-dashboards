# Django stuff
from django.shortcuts import render, redirect, HttpResponse
# How view functions can respond:
#   -Render for using templates with context
#   -HttpResponse for raw HTML responses
#   -Redirects for kicks to other URLs, (give it the 'name' of the url from routing)

from django.contrib.auth import login, authenticate, logout
# Basic authentication stuff in Django
#   -login to login the user
#   -logout to logout the user
#   -authenticate to verify a set of credentials, used internally in login

from django.contrib import messages
# Message system in Django, allows rendering and assign of messages, see base.html template for html that implements the message system.

from django.contrib.auth.forms import AuthenticationForm
# Form for authenticating users properly. Note, if you ever want a user to login, use this form in Django

from django.contrib.auth.decorators import login_required
# Allows the decorator, login_required, to be used, which forces a user to login

from django.contrib.auth.models import User
# Import Django's user model

# My stuff
from apps.accounts.forms import NewUserForm, EditInfoForm
from apps.core.helper import gen_panel_data
from apps.core.models import Panel, Dashboard

# Create your views here.
def account_page(request):
    '''
    Provide links for the user to either login or sign up.
    '''
    context = {
        'title' : 'Welcome!',
    }
    return render(request, 'accounts/account_page.html', context)

def all_users(request):
    '''
    View all of the other users.
    '''
    context = {
        'title' : 'All Users',
        'all_users' : User.objects.filter(is_superuser=False),
    }
    return render(request, 'accounts/all_users.html', context)

def view_profile(request, user_id):
    '''
    View for the profile page. If the user is logged in and it is their profile, let them make edits. Otherwise they can just view the profile.
    '''
    # Check if the current user is the same as the page they are viewing
    user = User.objects.get(id=user_id)

    if request.user == user:
        is_viewing_self = True
    else:
        is_viewing_self = False

    # Get the dashboards
    all_dashboards = Dashboard.objects.filter(owner=user)

    # Get the panels from the database
    panel_list = Panel.objects.filter(owner=user)
    all_panels = gen_panel_data(panel_list, request.user)
    context = {
        'title': '@' + user.username,
        'is_viewing_self': is_viewing_self,
        'all_dashboards' : all_dashboards,
        'all_panels' : all_panels,
    }
    return render(request, 'accounts/view_profile.html', context)

def sign_up(request):
    '''
    Sign up for a new profile.
    '''
    # Sign up form:
    # Recall the steps for dealing with forms:
    # 1.) Check for POST request
    # 2.) If no POST request, make an empty form
    # 3.) If there is a POST request, validate the form and add the data to the database

    # Perform standard POST request form processing
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Extra stuff
            # Send a user a message that their account was created
            # Use: message.tag(request, message_text)
            # The tags get used in base.html with bootstrap
            messages.success(request, 'Account created successfully. Welcome!')
            # Log the user in with Django's authentication system
            login(request, user)

            return redirect('home')
    else:
        form = NewUserForm()

    # Set context
    context = {
        'title' : 'Sign Up',
        'form' : form,
    }

    return render(request, 'accounts/signup.html', context)

def login_view(request):
    '''
    Log in the user
    '''
    # Login Form:
    # Uses built-in Django form to properly do the authentication (AuthenticationForm)
    # Same pattern as sign-up:
    # 1.) Check for POST request
    # 2.) If no POST request, make an empty form
    # 3.) If there is a post request, validate the form, and in this case login

    # Perform standard POST request form processing
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # User has specified valid credentials, have user log-in, and then
            # redirect back home
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()

    # Set context
    context = {
        'title': 'Login',
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    '''
    Log out the user.
    '''
    # Logout
    # No form needed, just a button
    # When the user presses the button
    # 1.) It logs them out
    # 2.) Updates a message to let them know they logged out
    # 3.) Brings them back to the homepage
    logout(request)
    messages.success(request, 'Logged out.')
    return redirect('home')

@login_required
def edit_profile(request, user_id):
    '''
    Edit the information in the profile using the EditInfoForm
    '''
    # Same as other form methods, in this case, since the form is a model form that uses the user as a model, we can instantiate the form with the user's info as the default and then overwrite it with what's in the post request like so:
    if request.method == 'POST':
        form = EditInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('view_profile', user_id=user_id)
    else:
        form = EditInfoForm(instance=request.user)
    context = {
        'title' : 'Edit Info for @' + request.user.username,
        'form' : form,
    }
    return render(request, 'accounts/edit_profile.html', context)