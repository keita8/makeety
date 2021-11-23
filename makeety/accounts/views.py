from django.shortcuts import render, redirect, reverse
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators  import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from carts.views import _cart_id
from carts.models import Cart, CartItem
import requests


# Inscription
def register(request):

    if request.user.is_authenticated:
        return redirect('homepage')
    else:

        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                first_name   = form.cleaned_data['first_name']
                last_name    = form.cleaned_data['last_name']
                phone_number = form.cleaned_data['phone_number']
                email        = form.cleaned_data['email']
                city         = form.cleaned_data['city']
                password     = form.cleaned_data['password']
                username     = email.split('@')[0]
                user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, city=city,username=username, password=password)
                user.phone_number = phone_number
                user.save()

                # LIEN D'ACTIVATION DU COMPTE
                current_site = get_current_site(request)
                mail_subject = "Lien d'activation de votre compte"
                message      = render_to_string('accounts/account_verification_email.html', {
                    'user'   : user,
                    'domain' : current_site,
                    'uid'    : urlsafe_base64_encode(force_bytes(user.pk)),
                    'token'  : default_token_generator.make_token(user),
                    } )
                to_email=email
                send_email=EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                messages.success(request, "Compte crée avec succès")
                # return redirect('accounts:login')
                return redirect('/accounts/login/?command=verification&email='+email)

        else:
            form = RegistrationForm()

        context = {
        'form' : form,
        }
        return render(request, 'accounts/register.html', context)


# Connexion
def login(request):

    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']

            user = auth.authenticate(password=password, email=email)

            if user is not None:

                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)

                        # Getting the product variations by cart id
                        product_variation = []
                        for item in cart_item:
                            variation = item.variations.all()
                            product_variation.append(list(variation))

                        # Get the cart items from the user to access his product variations
                        cart_item = CartItem.objects.filter(user=user)
                        ex_var_list = []
                        id = []
                        for item in cart_item:
                            existing_variation = item.variations.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)

                        # product_variation = [1, 2, 3, 4, 6]
                        # ex_var_list = [4, 6, 3, 5]

                        for pr in product_variation:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()
                except:
                    pass

                auth.login(request, user)
                messages.info(request, f'Nous sommes ravis de vous revoir {user.first_name} ')
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    # next=/cart/checkout/
                    params = dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                        nextPage = params['next']
                        return redirect(nextPage)
                except:
                    return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Email ou mot de passe incorrect')
                return redirect('accounts:login')

        template_name = 'accounts/login.html'
        context = {}

    return render(request, template_name, context)


# Déconnexion
@login_required(login_url='accounts:login')
def logout(request):

    auth.logout(request)
    messages.success(request, 'Nous serons ravis de vous revoir')
    return redirect('accounts:login')

# Lien d'activation du compte
def activate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Votre compte a bien été activé')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Ce lien d\'activation a deja expiré.')
        return redirect('accounts:register')


# Tableau de bord
@login_required(login_url='accounts:login')
def dashboard(request):

    template_name = 'accounts/dashboard.html'
    context = {}

    return render(request, template_name, context)


# Réinitialisation du mdp
def forget_password(request):

    if request.method == 'POST':

        email = request.POST['email']

        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            # LIEN DE REINITIALISATION DU MOT DE PASSE
            current_site = get_current_site(request)
            mail_subject = "Réinitialisation de votre mot de passe"
            message      = render_to_string('accounts/reset_password_email.html', {
                'user'   : user,
                'domain' : current_site,
                'uid'    : urlsafe_base64_encode(force_bytes(user.pk)),
                'token'  : default_token_generator.make_token(user),
                } )
            to_email=email
            send_email=EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, "Les instructions de réinitialisation de votre mot de passe vous ont été envoyées.")
            return redirect('accounts:login')

        else:
            messages.error(request, 'Cette adresse email n\'est associée à aucun compte.')
            return redirect('accounts:forget_password')

    template_name = 'accounts/forget_password.html'
    context = {}

    return render(request, template_name, context)


# Redirection vers la page de réinitialisation si le token est valide
def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None


    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Réinitialiser votre mot de passe')
        return redirect('accounts:reset_password')
    else:
        messages.error(request, 'Ce lien de réinitialisation a deja expiré')
        return redirect('accounts:login')


# Page de réinitialisation du mot de passe
def reset_password(request):

    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Votre mot de passe a été réinitialisé avec succès')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Les mots de passe ne correspondent pas')
            return redirect('accounts:reset_password')
    else:
        template_name = 'accounts/new_password.html'
        context = {}

        return render(request, template_name, context)