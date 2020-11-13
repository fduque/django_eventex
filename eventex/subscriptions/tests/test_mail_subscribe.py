from django.test import TestCase
from django.core import mail


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos', cpf='12345678901', email='henrique@bastos.net', phone='11-11111-1111')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmacao de Inscricao'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'duqtechnology@gmail.com'

        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['duqtechnology@gmail.com', 'henrique@bastos.net']

        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = ['Henrique Bastos',
                    '12345678901',
                    'henrique@bastos.net',
                    '11-11111-1111']
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
        #Version 1.0
        #self.assertIn('Henrique Bastos', self.email.body)
        #self.assertIn('12345678901', self.email.body)
        #self.assertIn('henrique@bastos.net', self.email.body)
        #self.assertIn('11-11111-1111', self.email.body)