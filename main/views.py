from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, authenticate, forms
from .forms import LoginForm, UserCreateForm, UserChangeForm, PasswdChangeForm
from django.core.mail import send_mail
from django.contrib.auth.models import User


def index(request):
    data = {}
    if not request.user.is_authenticated:
        data['loginform'] = LoginForm(request.POST or None)
    return render(request, 'main/index.html', data)


def login_view(request):
    """
    View called for  the /login/ url.

    Instanciate a LoginForm and pass it to the login.html template.

    :param request: The request object
    :return: HttpResponseRedirect a redirect to target page | redirect to main page | render of login.html
    """

    form = LoginForm(request.POST or None)

    data = {'login_form': form}

    if request.POST:

        if 'cancel' in request.POST:
            return redirect('main:index')
        elif form.is_valid():
            user = form.login(request)

            if not user.last_login:
                form = UserCreateForm(instance=user)
                return render(request, 'main/new_user.html', {'form': form, 'userid': user.pk, 'mode': 'ny'})
            elif user:
                login(request, user)

            if 'next' in request.POST and len(request.POST['next']) > 0:
                return redirect(request.POST['next'])
            else:
                return redirect('main:index')

        data['next'] = request.POST['next']

    if request.GET:
        if 'next' not in data and 'next' in request.GET:
            data['next'] = request.GET['next']
        if 'from' in request.GET:
            data['from'] = request.GET['from']

    return render(request, 'main/login.html', data)


def forgot_password(request):
    """ View for reseting password. Generates a new random password and sends to given email """
    errors = []

    if request.POST:
        email = request.POST.get('email')
        user_match = User.objects.filter(email=email)

        if user_match.count() is 0:
            errors.append('The provided email does not exist')
        else:
            user = user_match[0]
            pw = User.objects.make_random_password()
            user.set_password(pw)
            user.save()

            message = 'Here is your new password for www.edueval.no:\n\n' \
                      + pw \
                      + '\n\nYour username is: ' + user.username
            subject = 'Edueval - new passord'
            from_email = 'dev.trollkode@gmail.com'
            send_mail(subject, message, from_email, [email])

            errors.append('An email has been sent to your inbox. <a href="/">Back to the front page</a>')

    return render(request, 'main/forgot_password.html', {'errors': errors})


def handle_new_user(request):
    """
    View for handling a user that logs in for the first time
    :param request:
    :return:
    """
    if request.POST:

        if request.POST.get('cancel'):
            return redirect('main:index')

        userid = request.POST.get('user_id')
        userform = UserCreateForm(request.POST, userid=userid)
        message = ['Velkommen som ny bruker i byggordboka.',
                   'Vennligst velg et nytt passord. Du kan også velge et nytt brukernavn']

        if userform.is_valid() and userid:
            userform.update(userid)

            username = userform.cleaned_data.get('username')
            password = userform.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                next_url = request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('main:index')

        return render(request, 'main/new_user.html',
                      {'form': userform, 'userid': userid, 'message': message})

    return redirect('main:index')


@login_required
def edit_user_info(request):
    """ View for editing user account information """
    fb_msg = None

    if request.POST:
        user = request.user
        mode = request.POST.get('mode')

        # If the button for user info was clicked
        if mode == 'ch_usr':
            ch_user_form = UserChangeForm(request.POST)
            ch_pw_form = PasswdChangeForm(user=request.user)
            if ch_user_form.is_valid():
                user.username = ch_user_form.cleaned_data.get('username')
                user.email = ch_user_form.cleaned_data.get('email')

                user.save()
                fb_msg = "Din kontoinformasjon har blitt oppdatert"

        # If the button for password was clicked
        if mode == 'ch_pw':
            ch_pw_form = PasswdChangeForm(data=request.POST, user=request.user)
            ch_user_form = UserChangeForm(instance=request.user, initial={'old_username': request.user.username})
            if ch_pw_form.is_valid():
                new_pw = ch_pw_form.cleaned_data.get('new_password1')
                user.set_password(new_pw)
                user.save()
                fb_msg = "Ditt passord har blitt endret"

    else:
        ch_pw_form = PasswdChangeForm(user=request.user)
        ch_user_form = UserChangeForm(instance=request.user, initial={'old_username': request.user.username})

    return render(request, 'main/edit_user.html', {'usrform': ch_user_form, 'pwform': ch_pw_form, 'fdbck': fb_msg})
