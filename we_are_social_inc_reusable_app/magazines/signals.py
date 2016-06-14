# coding=utf-8
import arrow
from .models import Purchase

from paypal.standard.ipn.signals import valid_ipn_received


def subscription_created(sender, **kwargs):
    """
    Created a subscription in the db
    """
    print('sub created')
    # 'sender' argument sent with the signal. In this case, is an instance of
    #  the instant payment notification.
    ipn_obj = sender  # ipn - instant payment notification
    # custom was defined in the PayPayPaymentForm in magazines/templatetags/magazine_extras.py
    magazine_id = ipn_obj.custom.split('-')[0]
    user_id = ipn_obj.custom.split('-')[1]
    # Create record in the db
    Purchase.objects.create(magazine_id=magazine_id,
                            user_id=user_id,
                            subscription_end=arrow.now().replace(weeks=+4).datetime)


def subscription_was_cancelled(sender, **kwargs):

    ipn_obj = sender
    magazine_id = ipn_obj.custom.split('-')[0]
    user_id = ipn_obj.custom.split('-')[1]
    # Get record from the db
    purchase = Purchase.object.get(user_id=user_id, magazine_id=magazine_id)
    # Update the subscription_end (to end the subscription immediately) and save/update in the db
    purchase.subscription_end = arrow.now()
    purchase.save()


# connect() method used to tell Django that we want the
# relevant code to be run whenever those signals are sent.
valid_ipn_received.connect(subscription_created)  # see magazines/signals
valid_ipn_received.connect(subscription_was_cancelled)  # see magazines/signals