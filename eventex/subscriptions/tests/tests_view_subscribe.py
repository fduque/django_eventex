from django.core import mail
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscribeGet(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """"Get/inscricao/ must return status code 200 """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """"Must use subscriptions/subscription_form.html"""
        response = self.client.get('/inscricao/')
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """"HTML Must contain input tags"""
        #Version 2
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


        #Version 1
        #self.assertContains(self.resp, '<form')
        #self.assertContains(self.resp, '<input', 6)
        #self.assertContains(self.resp, 'type="text"', 3)
        #self.assertContains(self.resp, 'type="email"')
        #self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """HTML must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))

class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos', cpf='12345678901', email='henrique@bastos.net', phone='11-11111-1111')
        self.resp = self.client.post('/inscricao/', data)


    def test_post(self):
        """Valid POST should redirect to /incricao/ """
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_erros(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Henrique Bastos',
                    cpf='12345678901',
                    email='henrique@bastos.net',
                    phone='11-11111-1111')
        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscricao Realizada com Sucesso!')