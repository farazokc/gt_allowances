from django.contrib.auth.backends import BaseBackend
from myapp.models import Users


class MyBackend(BaseBackend):
    _INSTANCE = None
    __isActive = None
    __Current_logged_in :  None

    def __init__(self):
        if MyBackend._INSTANCE is None:
            MyBackend._INSTANCE = self
    @staticmethod
    def getInstance():
        if MyBackend._INSTANCE is None:
            MyBackend()
        return MyBackend._INSTANCE




    def authenticate(self, request, emp_id=None, emp_pass = None):
        logged_in = Users.objects.filter(emp_id=emp_id, emp_pass=emp_pass)

        if logged_in:
            self.__isActive = True
            self.__Current_logged_in = emp_id
            return True
        else:
            return False

    def get_user(self, user_id):
        super().get_user(user_id)

    def get_active(self):
        return self.__isActive
    
    def get_current_logged_in(self):
        return self.__Current_logged_in
