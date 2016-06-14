from __future__ import unicode_literals
import uuid
from django.db import models
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm


class Product(models.Model):

    name = models.CharField(max_length=254, default='')
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    @property  # Defines a function that can be accessed from a template.
    def paypal_form(self):
        """
        Used to create a dict in order to pass the needed information for the
        PayPalPaymentsForm to create our button, and also the required html
        form markup when the page template is rendered.
        """
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,  # Comes from the settings file.
            "amount": self.price,
            "currency": "GBP",
            "item_name": self.name,
            "invoice": "%s-%s" % (self.pk, uuid.uuid4()),  # string to uniquely identify transaction.
            "notify_url": settings.PAYPAL_NOTIFY_URL,  # where PayPal can send any success or error messages on our site.
            "return_url": "%s/paypal-cancel" % settings.SITE_URL,  # where to return a customer after the payment process is complete.
            "cancel_return": "%s/paypal-cancel" % settings.SITE_URL  # where to return the customer if they choose to cancel the payment process.
        }

        return PayPalPaymentsForm(initial=paypal_dict)

    def __unicode__(self):
        return self.name

