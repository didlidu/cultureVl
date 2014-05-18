from django.utils import simplejson
from .Dajaxice import Dajaxice, dajaxice_autodiscover
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def sayhello(request):
    return simplejson.dumps({'message':'Hello World'})