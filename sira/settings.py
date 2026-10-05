from pathlib import Path
import os
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-only')
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
ALLOWED_HOSTS = [x.strip() for x in os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if x.strip()]
INSTALLED_APPS = ['django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','core']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'sira.urls'
TEMPLATES = [{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'core'/'templates'],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'sira.wsgi.application'
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'session.sqlite3'}}
LANGUAGE_CODE='es-ve'; TIME_ZONE='America/Caracas'; USE_I18N=True; USE_TZ=True
STATIC_URL='static/'; STATIC_ROOT=BASE_DIR/'staticfiles'
SESSION_COOKIE_HTTPONLY=True; SESSION_COOKIE_SAMESITE='Lax'; CSRF_COOKIE_HTTPONLY=True
SIRA_API_URL=os.getenv('SIRA_API_URL','http://127.0.0.1:8080/api/v1').rstrip('/')
