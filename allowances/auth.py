from django.contrib.auth.backends import BaseBackend
from myapp.models import Users


class MyBackend(BaseBackend):
    __isActive : False

    def authenticate(self, request, emp_id=None, emp_pass = None):
        logged_in = Users.objects.filter(emp_id=emp_id, emp_pass=emp_pass)
        if logged_in:
            __isActive = True
            return True
        else:
            return False

    def get_user(self, user_id):
        super().get_user(user_id)

    def get_active(self):
        return self.__isActive

