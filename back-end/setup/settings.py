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
        print(DATABASES)
    elif DB_ENGINE == "mysql":
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": os.getenv("MYSQL_NAME", "pizzaria_db"),
                "USER": os.getenv("MYSQL_USER", ""),
                "PASSWORD": os.getenv("MYSQL_PASSWORD", ""),
                "HOST": os.getenv("MYSQL_HOST", "localhost"),
                "PORT": os.getenv("MYSQL_PORT", "3306"),
            }
        }
    else:
        raise ValueError("DB_ENGINE inválido. Escolha 'postgresql' ou 'mysql'.")



# Configuração específica para testes
# if "test" in sys.argv:
#     DATABASES["default"]["NAME"] = "test_pizzaria_db"  # Nome do banco temporário
#     DATABASES["default"]["USER"] = "root"
#     DATABASES["default"]["PASSWORD"] = ""
#     DATABASES["default"]["HOST"] = "localhost"
#     DATABASES["default"]["PORT"] = "3306"

#opção sugerida pelo gpt pra usar sqlite de temporario
# if "test" in sys.argv:
#     DATABASES["default"] = {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "test_db.sqlite3",
#     }


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

# Configuração de arquivos estáticos
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Configuração do models
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



# Configuração de idioma e fuso horário
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "pizzaria_db",
#         "USER": "postgres",
#         "PASSWORD": "086002",
#         "HOST": "localhost",
#         "PORT": "5432",
#         'OPTIONS': {
#             'client_encoding': 'UTF8',
#         },
#     }
# }

# para conectar no MySQL
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": "pizzaria_db",
# # Substituir com dados da criação do no banco local
#         "USER": "root",
#         "PASSWORD": "",
#         # Substituir se estiver usando um servidor remoto
#         "HOST": "localhost",
#         "PORT": "3306",
#     }
# }

#database_url = os.environ.get("DATABASE_URL")
#DATABASES["default"] = dj_database_url.parse("postgresql://zerissi_banco_user:qddfrvzueuEa065PWzGZTfsoF9PywCfe@dpg-csnseei3esus73ehomqg-a.oregon-postgres.render.com/zerissi_banco")
#DATABASES["default"] = dj_database_url.parse(database_url)

# if database_url and "test" not in sys.argv:
#     DATABASES["default"] = dj_database_url.parse(database_url)


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
