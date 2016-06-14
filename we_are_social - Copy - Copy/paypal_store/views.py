from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


@csrf_exempt
def paypal_return(request):
    """
    Handles the return of a customer after payment.
    Paypal posts all the transaction confirmation info back to return_url when
    the user returns to the site.
    E.g. <QueryDict: {u'protection_eligibility': [u'Ineligible'],
     u'last_name': [u'Hibbert'], u'txn_id': [u'7PC450130C6830542'],
     u'receiver_email': [u'merchant@somesite.com'],
     u'payment_status': [u'Completed'], u'payment_gross': [u'2.30'],
     u'tax': [u'0.00'],u'residence_country': [u'US'],
     u'invoice': [u'1-b1708259-bfbb-49c3-9886-c8d376449610'],
     u'payer_status': [u'verified'], u'txn_type':[u'web_accept'],
     u'handling_amount': [u'0.00'], u'payment_date': [u'07:14:24 Aug 17, 2015 PDT'],
     u'first_name': [u'Mike'],u'item_name': [u'Cheese'], u'charset': [u'utf-8'],
     u'custom': [u''], u'notify_version': [u'3.8'], u'transaction_subject': [u''],
     u'test_ipn': [u'1'], u'item_number': [u''], u'receiver_id': [u'9HXLXHFWVDHMY'],
     u'business': [u'merchant@somesite.com'], u'payer_id':[u'U4KRAKEBX54K4'],
     u'auth': [u'AyTr4qaCrPAlUt2bb3Vq8WoF4cnWkZGxqs4NhXm1wcohCDHd-xXTClihy3V14nnXqVlL0o3-TCjS8goMPWF8yrQ'],
     u'verify_sign': [u'An5ns1Kso7MWUdW4ErQKJJJ4qi4-AGEN-sbiMEvw1zwTlDjlqN.0DXZo'],
     u'payment_fee': [u'0.37'], u'mc_fee': [u'0.37'],u'mc_currency': [u'USD'],
     u'shipping': [u'0.00'], u'payer_email': [u'humpty@dumpty.com'], u'payment_type': [u'instant'],
     u'mc_gross':[u'2.30'], u'quantity': [u'1']}>
    E.g. payment_status shows the transaction status - 'Completed'.
    """
    args = {'post': request.POST, 'get': request.GET}
    return render(request, 'paypal/paypal_return.html', args)


def paypal_cancel(request):
    """
    Handles what happens when they cancel at the PayPal site.
    """
    args = {'post': request.POST, 'get': request.POST}
    return render(request, 'paypal/paypal_cancel.html', args)
