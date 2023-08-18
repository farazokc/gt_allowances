from django.contrib.auth.backends import BaseBackend
from myapp.models import Users


class MyBackend(BaseBackend):
    _INSTANCE = None
    __isActive = None
    _Current_logged_in = 0
    errors = {
        'Trans_Req'    : "'Travel From' cannot be same as 'Travel To' and 'Travel To' cannot be same as 'Return To'",
        'login_failed' : 'Employee ID or Password not correct',
         'Location'    :  "Location already saved"
    }
    success = {
        'Trans_Req' : 'Official visit saved succesfully',
        'Location' :  'Location saved succesfully',
        'Petrol'   :   'Petrol price added'
    }
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
            self._Current_logged_in = emp_id
            # print(("ID" , self._Current_logged_in))

            return True
        else:

            return False

    def logout(self):
        self.__isActive = False
        self._Current_logged_in = None
        # request
        return True

    def get_user(self, user_id):
        super().get_user(user_id)

    def get_active(self):
        return self.__isActive
    
    def get_current_logged_in(self):
        return self._Current_logged_in

    def get_error_msg(self):
        return self.errors
    def get_success(self):
        return self.success