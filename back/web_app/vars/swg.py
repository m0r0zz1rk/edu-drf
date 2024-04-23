from .tinymce import *

SWAGGER_SETTINGS = {
   'USE_SESSION_AUTH': False,
   'SECURITY_DEFINITIONS': {
      'Token': {
            'type': 'apiKey',
            'name': 'Авторизация по токену (шаблон: Token (JWT-токен)',
            'in': 'header'
      }
   }
}
