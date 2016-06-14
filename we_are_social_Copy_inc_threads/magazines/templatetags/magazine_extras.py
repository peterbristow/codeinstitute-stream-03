import uuid

from django import template
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm

register = template.Library()


def paypal_form_for(magazine, user):
    """
    Handles creating a form when passed the user and
    magazine objects.
    """
    if user.is_subscribed(magazine):  # see accounts/models.py
        html = "Subscribed!"
    else:
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "currency_code": "GBP",
            "cmd": "_xclick-subscriptions",
            "a3": magazine.price,
            "p3": 1,
            "t3": "M",
            "src": 1,
            "sra": 1,
            "item_name": magazine.name,
            "invoice": uuid.uuid4,
            "notify_url": settings.PAYPAL_NOTIFY_URL,
            "return_url": "%s/paypal_return/" % settings.SITE_URL,
            "cancel_return": "%s/paypal_cancel/" % settings.SITE_URL,
            "custom": "%s-%s" % (magazine.pk, user.id)  # magazines/signals methods use this.
        }

        # render the form
        if settings.DEBUG:
            html = PayPalPaymentsForm(initial=paypal_dict,button_type='subscribe').sandbox()
        else:
            html = PayPalPaymentsForm(initial=paypal_dict,button_type='subscribe').render()

    return html

# Register this simple_tag (template tag) with the Django template system.
# Using a simple_tag is important in this stage, as a normal filter can
# only accept one argument, and in our case we want to pass in both the
# user and the magazine as arguments.
# called in the template like so:
# E.g.
# {% load magazine_extras %}
# <td>{% paypal_form_for magazine user %}</td>
register.simple_tag(paypal_form_for)
