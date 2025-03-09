from datetime import timedelta
from pathlib import Path
import dj_database_url
import os
import sys
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta
SECRET_KEY = os.getenv("SECRET_KEY", "chave-padrao-para-dev")

# Define o ambiente
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Hosts permitidos
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(" ")

# Configuração de CORS
CORS_ALLOWED_ORIGINS = ALLOWED_HOSTS if not DEBUG else ["http://localhost:8081", "http://127.0.0.1:8081"]
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Permite todas as origens apenas em dev


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "corsheaders",
    "gerenciador_de_motoboys.apps.GerenciadorDeMotoboysConfig",
    "gerenciador_de_funcionarios.apps.GerenciadorDeFuncionariosConfig",
    "gerenciador_de_clientes.apps.GerenciadorDeClientesConfig",
    "gerenciador_de_produtos.apps.GerenciadorDeProdutosConfig",
    "gerenciador_de_pedidos.apps.GerenciadorDePedidosConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "setup.middlewares.CustomCorsMiddleware"
]

ROOT_URLCONF = "setup.urls"
WSGI_APPLICATION = "setup.wsgi.application"


# Configuração do banco de dados
DB_ENGINE = os.getenv("DB_ENGINE", "postgresql").lower()
DATABASE_URL = os.getenv("DATABASE_URL")


if DATABASE_URL:

    # Usa a URL de banco de dados para produção
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # Configuração local (PostgreSQL ou MySQL)
    if DB_ENGINE == "postgresql":
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": os.getenv("POSTGRES_NAME"),
                "USER": os.getenv("POSTGRES_USER"),
                "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
                "HOST": os.getenv("POSTGRES_HOST"),
                "PORT": os.getenv("POSTGRES_PORT"),
                "OPTIONS": {
                    "client_encoding": "UTF8",
                },
            }
        }

# Configuração específica para testes sqlite
if "test" in sys.argv:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",  # Cria um arquivo SQLite para testes
    }

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "setup.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/


LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Configuração para arquivos estáticos
STATIC_URL = '/static/'  # URL para acessar arquivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Diretório onde os arquivos estáticos serão coletados
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Diretórios adicionais para arquivos estáticos
]