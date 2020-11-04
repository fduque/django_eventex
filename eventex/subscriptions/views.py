from django.core import mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib import messages

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)

        if form.is_valid():
            form.full_clean() ##Faz o parseamento dos campos dentro da requisicao

            body = render_to_string('subscriptions/subscription_email.txt',
                                    form.cleaned_data)
            mail.send_mail('Confirmacao de Inscricao',
                           body,
                           'duqtechnology@gmail.com',
                           ['duqtechnology@gmail.com', form.cleaned_data['email']])

            messages.success(request, 'Inscricao Realizada com Sucesso!')

            return HttpResponseRedirect('/inscricao/')
        else:
            return render(request, 'subscriptions/subscription_form.html',
                          {'form': form})

    else:
        context = {'form': SubscriptionForm()}
        return render(request, 'subscriptions/subscription_form.html', context)