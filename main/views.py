# django imports
from django.shortcuts import render, redirect
from django.views.generic import View

# django user authentication imports
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)

# project imports
from main.forms import UserCreationForm


class RegisterView(View):

    def get(self, request):

        # if a user is already logged in, redirect to home
        if request.user.is_authenticated():
            return redirect('main:home')

        # save a blank user creation form in the context and reload page
        context = {'form': UserCreationForm}
        return render(request, 'project/register.html', context)

    def post(self, request):

        # if a user is already logged in, redirect to home
        if request.user.is_authenticated():
            return redirect('main:home')

        # create a filled user creation form from POST data
        filled_user_creation_form = UserCreationForm(request.POST)

        # if the filled form is valid:
        if filled_user_creation_form.is_valid():

            # create a new user object with the form information
            user = filled_user_creation_form.save()

            # authenticate the new user against the database (a formality)
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])

            # log the new user into the site and redirect to home
            auth_login(request, user)
            return redirect('main:home')

        # if the filled form was invalid
        else:

            # save error message and invalid form to be passed back for editing
            context = {}
            context['error_on_create'] = True
            context['form'] = filled_user_creation_form
            return render(request, 'project/register.html', context)


class LoginView(View):

    def get(self, request):

        # get the next parameter to remember where to go after login
        context = {}
        context['next'] = request.GET.get('next', '/')
        return render(request, 'project/login.html', context)

    def post(self, request):

        # if a user is already logged in, redirect to home
        if request.user.is_authenticated():
            return redirect('main:home')

        # attempt to authenticate the user
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])

        # if the user is found in the database
        if user is not None:

            # and the user's account is active
            if user.is_active:

                # then go ahead and log the user in and redirect to next
                auth_login(request, user)
                return redirect(request.POST.get('next', None))

            # if the user's account is not active
            else:

                # reload the login page and display error message
                context = {}
                context['error'] = 'Account deactivated.'
                return render(request, 'project/login.html', context)

        # if the user isn't found in the database
        else:

            # reload the login page and display error message
            context = {}
            context['error'] = 'Username or password not found'
            return render(request, 'project/login.html', context)


class LogoutView(View):

    def get(self, request):
        auth_logout(request)
        return redirect('main:home')


def home(request):
    return render(request, 'main/home.html')
