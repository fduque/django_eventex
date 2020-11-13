
# Eventex

Sistema de Eventos encomendado pela Morena

[![Build Status](https://travis-ci.com/fduque/django_eventex.svg?branch=master)](https://travis-ci.com/fduque/django_eventex)

## Como desenvolver?

1. Clone o repositorio
2. Crie um virtualenv com python 3.5
3. Ative o virtualenv
4. Instale as dependencias
5. Configure a instancia com o .env
6. Execute os testes

```console
git clone git@github.com:henriquebastos/eventex.git wttd
cd wttd
python -m venv .wttd
source .wttd/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```


### Como fazer o deploy?
1. Crie uma instancia no Heroku
2. Envie as configuracoes para o Heroku
3. Defina um SECRET_KEY segura para a instancia
4. Defina DEBUG=False
5. Configure o servico de email
6. Envie para o Heroku

```console
heroku create minhainstancia
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku config:set DEBUG=False
#configura o email
git push heroku master --force
```