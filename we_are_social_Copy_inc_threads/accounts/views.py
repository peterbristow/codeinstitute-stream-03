# coding=utf-8
import datetime
import json

import arrow
import stripe
from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from accounts.forms import UserRegistrationForm, UserLoginForm
from models import User

stripe.api_key = settings.STRIPE_SECRET


def register(request):
    """
    Gets a new users email and password and creates an account.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # create a charge customer object for one off payments.
                # customer = stripe.Charge.create(
                #     amount=999,
                #     currency="USD",
                #     description=form.cleaned_data['email'],
                #     card=form.cleaned_data['stripe_id'],
                # )

                # create a customer object within Stripe using the email and
                # Stripe token/id for a re-occurring subscription.
                customer = stripe.Customer.create(
                    email=form.cleaned_data['email'],
                    card=form.cleaned_data['stripe_id'],  # this is currently the card token/id
                    plan='REG_MONTHLY2',  # name of plan. See 'Plans' in Stripe website.
                )
            except stripe.error.CardError, e:
                messages.error(request, "Your card was declined!")
            else:
                # charge() method above returns a customer object that contains a 'paid' boolean field.
                # If customer.paid:
                # form.save()

                if customer:
                    user = form.save()

                    # Used in updating/cancelling the subscription
                    user.stripe_id = customer.id  # This will be a string of the form ‘cus_XXXXXXXXXXXXXX’)

                    # Arrow is a fast way of dealing with dates and times in Python.
                    # Create a date that is exactly 4 weeks from now and convert it
                    # into a datetime object which is compatible with our DateTimeField
                    # in the User model.
                    user.subscription_end = arrow.now().replace(weeks=+4).datetime

                    user.save()

                    # request.POST.get() - gets specific data
                    user = auth.authenticate(email=request.POST.get('email'),
                                             password=request.POST.get('password1'))

                    if user:
                        auth.login(request, user)  # login customer/user in.
                        messages.success(request, "You have successfully registered.")
                        # reverse refers to the 'name' given to a route in urls.py
                        return redirect(reverse('profile'))

                    else:
                        messages.error(request, "unable to log you in at this time!")

                else:
                    messages.error(request, "We were unable to take payment from the card provided.")

    else:
        today = datetime.date.today()
        form = UserRegistrationForm(initial={'expiry_month': today.month, 'expiry_year': today.year})

    args = {'form': form, 'publishable': settings.STRIPE_PUBLISHABLE}
    # cross-site request forgery protection
    args.update(csrf(request))

    return render(request, 'register.html', args)


@login_required(login_url='/login/')
def cancel_subscription(request):
    """
    Cancel subscriptions
    """
    try:
        # get an instance of the stripe customer from stripe.
        # Pass the stripe_id get the stripe customer via the stripe API
        customer = stripe.Customer.retrieve(request.user.stripe_id)

        # To end immediately, set the subscription_end field on our user to ‘arrow.now()’
        # customer.subscription_end = arrow.now()

        # customer then calls the cancel_subscription() method and
        # automatically cancels the customers subscription at the period end.
        customer.cancel_subscription(at_period_end=True)
    except Exception, e:
        messages.error(request, e)
    return redirect('profile')


@csrf_exempt  # Stops Django from blocking this call from Stripe.
def subscriptions_webhook(request):
    event_json = json.loads(request.body)  # Turn request.body into a dict.
    # Verify the event by fetching it from Stripe
    try:
        # firstly verify this is a real event generated by Stripe.com
        # commented out for testing - uncomment when live
        # event = stripe.Event.retrieve(event_json['object']['id'])
        cust = event_json['object']['customer']  # find customer
        paid = event_json['object']['paid']
        user = User.objects.get(stripe_id=cust)  # get customer from db
        if user and paid:  # if user exists and has paid
            user.subscription_end = arrow.now().replace(weeks=+4).datetime  # add 4 weeks from now
            user.save()

    except stripe.InvalidRequestError, e:
        return HttpResponse(status=404)
    return HttpResponse(status=200)


@login_required(login_url='/login/')  # page cannot be viewed unless user is logged in.
def profile(request):
    return render(request, 'profile.html')


def login(request):
    if request.method == 'POST':
        # if submitting form create instance of form class and populate
        form = UserLoginForm(request.POST)
        if form.is_valid():  # if login form is valid
            # authenticate user:
            # 'auth' will find our class 'EmailAuth' in backends.py via the
            # backend list in settings.py and then call the authenticate method.
            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password'))
            if user is not None:
                auth.login(request, user)  # login user. login() is a django method. Sets up a user session.
                messages.success(request, "You have successfully logged in.")
                return redirect(reverse('profile'))
            else:
                form.add_error(None, "Your email or password is not recognised.")

    else:
        # if login link has been clicked show the empty login form
        form = UserLoginForm()

    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'login.html', args)


def logout(request):
    """
    Destroy the login session
    """
    auth.logout(request)  # destroys the user session.
    messages.success(request, 'You have successfully logged out.')
    return redirect(reverse('index'))
