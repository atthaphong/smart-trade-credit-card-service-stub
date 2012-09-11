from django.core.exceptions import ObjectDoesNotExist
from creditcard.models import Account
from django.http import HttpResponse


SUCCESS = 'success'
FAILED = 'failed'

def verify(request):

    result = FAILED
    card_num = request.POST['card_num']
    card_ccv = request.POST['card_ccv']
    amount = float(request.POST['amount'])

    try:
       account =  Account.objects.get(number=card_num,ccv=card_ccv)
       if account.is_verified(amount):
           result = SUCCESS
       else:
           result = FAILED

    except ObjectDoesNotExist:
        result = FAILED

    return HttpResponse(result)

def pay(request):

    result = FAILED
    card_num = request.POST['card_num']
    card_ccv = request.POST['card_ccv']
    amount = float(request.POST['amount'])

    try:
        account =  Account.objects.get(number=card_num,ccv=card_ccv)
        if account.is_paid(amount):
            print('here')
            result = SUCCESS
        else:
            result = FAILED

    except ObjectDoesNotExist:
        print('not found')
        result = FAILED

    return HttpResponse(result)