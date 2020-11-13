from django.core import mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib import messages

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)

def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid(): ##se o form nao e valido, mata o processo aqui
        return render(request, 'subscriptions/subscription_form.html',
                      {'form': form})

    #se o form for valido, ele vai continuar
    #Envia o emal de confirmacao
    _send_mail('Confirmacao de Inscricao', settings.DEFAULT_FROM_EMAIL, form.cleaned_data['email'], 'subscriptions/subscription_email.txt', form.cleaned_data)


    #Reporta sucesso de processamento
    messages.success(request, 'Inscricao Realizada com Sucesso!')

    return HttpResponseRedirect('/inscricao/')

def new(request):
    return render(request, 'subscriptions/subscription_form.html', {'form': SubscriptionForm()})

def _send_mail(subject, from_, to, template_name, context):
        body = render_to_string(template_name, context)
        mail.send_mail(subject, body, from_, [from_, to])