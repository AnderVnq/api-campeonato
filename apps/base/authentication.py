from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.utils import timezone
from django.conf import settings
from datetime import timedelta

 
class ExpireTokeAuthentication(TokenAuthentication):
    expired=False
    
    def expires_in(self,token):
        time_elapsed=timezone.now() - token.created
        left_time=timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed

        return left_time

    def is_token_expired(self,token):
        return self.expires_in(token)<timedelta(seconds=0)

    def token_expired_handler(self,token):
        is_expire=self.is_token_expired(token)
        if is_expire :
            self.expired=False
            user=token.user
            token.delete()
            token=self.get_model().objects.create(user=user)
            print("token expirado")
        return token
    

    def authenticate_credentials(self, key):
        message,token,user=None,None,None
        print(f"key {key}")
        try:
            token=self.get_model().objects.select_related('user').get(key=key)
            user=token.user
            token=self.token_expired_handler(token)
            #print(f"user desde authentocate credentials {user}, {token}")
        except self.get_model().DoesNotExist:
            #message='token invalido'
            pass
            #self.expired=True
        # if token is not None:
        #     if not token.user.is_active:
        #         message = 'Usuario no activo o eliminado'

        #     is_expired= self.token_expired_handler(token)
        #     if is_expired:
        #         message = 'Token expirado'
                
        return user#(user,token,message,self.expired)
    







class Authentication(object):
    user=None
    #user_token_expired=False
    def get_user(self,request):
        token=get_authorization_header(request).split()
        if token:
            try:
                token=token[1].decode()   
                print(token)
            except:   
                return None
            expired_token=ExpireTokeAuthentication()
            #user,token,message,self.user_token_expired=expired_token.authenticate_credentials(token)
            #user,token=expired_token.authenticate_credentials(token)
            user=expired_token.authenticate_credentials(token)
            #print(f"user desde get user {user,token,message}")
            if user != None:
                self.user=user
                return user
            #return message
        return None

    def dispatch(self,request,*args, **kwargs):
        user=self.get_user(request)
        if user is not None:
            # if type(user)== str:
            #     response= Response({'error':user,'expired':self.user_token_expired},status=status.HTTP_400_BAD_REQUEST)
            #     response.accepted_renderer=JSONRenderer()
            #     response.accepted_media_type='application/json'
            #     response.renderer_context={}
            #     print(f"user desde dispatch {user}")
            #     return response
            
            # if not self.user_token_expired:
            return super().dispatch(request,*args, **kwargs)
        
        response= Response({'error':'No se han enviado las credenciales'},status=status.HTTP_400_BAD_REQUEST)
        response.accepted_renderer=JSONRenderer()
        response.accepted_media_type='application/json'
        response.renderer_context={}
        return response