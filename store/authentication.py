from django.contrib.auth.backends import BaseBackend
from store.models import User
from django.db.models import Q


class EmailOrPhoneBackend(BaseBackend):
    
    def authenticate(self, request, username=None, password=None):
        
        try:
            user_object = User.objects.get(Q(email=username) | Q(phone=username))
            
            if user_object.check_password(password):
                return user_object
            else:
                return None
        except:
            return None
        
    def get_user(self, user_id):
        return User.objects.get(id=user_id)