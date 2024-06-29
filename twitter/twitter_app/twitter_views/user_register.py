from django.views.generic import TemplateView
from django.shortcuts import render
from database_connect.database_connect import Db_connect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse

class DataDamend(Db_connect):
    def __init__(self):
        super().__init__()
        
    def stmt_select_user_account(self):
        stmt = """SELECT username FROM user_account
        WHERE username = %(username)s"""
        return stmt
    
    def stmt_find_user_id(self):
        stmt = """SELECT id FROM user_account
        WHERE usernam = %(username)s"""
        return stmt
    
    def stmt_find_user_email(self):
        stmt = """SELECT user_email FROM user_account
        WHERe username = %(username)s"""
        return stmt
    
    def insert_into_user_account(self):
        stmt = """INSERT INTO user_account
        (username,user_password,user_email,register_date)
        VALUES(%(username)s,%(password)s,%(email)s,NOW())"""
        print(stmt)
        return stmt
    
    def select_last_id(self):
        stmt = """SELECT id FROM user_account
        order by id DESC limit 1"""
        return stmt
    
    def insert_into_user_profile(self):
        stmt = """INSERT INto user_profile(user_id,username)
        VALUES(%(user_id)s,%(username)s)"""
        return stmt
    def insert_into_auth_user(self):
        stmt = """INSERT INTO auth_user
        (password,username,email,is_superuser,first_name,last_name,is_staff,is_active,date_joined)
        VALUES(%(password)s,%(username)s,%(email)s,FALSE,'','',FALSE,TRUE,NOW())"""
        return stmt
    
    def __str__(self):
        return "SQL Query"


"""
main processing
"""

def user_register_main(data_form):
    dbh = DataDamend()
    username = data_form['username']
    user_password = data_form['password']
    user_password2 = data_form['confirm-password']
    user_email = data_form['email']
    data_dict = dict(
        username=username,
        password=make_password(user_password),
        email=user_email
    )
    # check email
    user_email_check = dbh.db_execute(dbh.stmt_find_user_email(),data_dict)
    if user_email_check:
        data_ld = dict(msg='目前有人使用該email',status='ERROR')
        return data_ld
    username_check = dbh.db_execute(dbh.stmt_select_user_account(),data_dict)
    if username_check:
        data_ld = dict(msg='目前使用者名稱已有人使用',status='ERROR')
        return data_ld
    if user_password!=user_password2:
        data_ld = dict(msg='確認密碼不符合',status='ERROR')
        return data_ld
    else:
        dbh.db_execute(dbh.insert_into_user_account(),data_dict)
        dbh.db_execute(dbh.insert_into_auth_user(),data_dict)
        user_id = dbh.db_fetchone(dbh.select_last_id())
        if user_id:
            user_id = int(user_id[0])
            dbh.db_execute(dbh.insert_into_user_profile(),{'user_id':user_id,'username':username})
        data_ld = dict(msg='註冊成功,以建立個人資訊！',status='OK')
        return data_ld
"""
url interface
"""
class User_rigister(TemplateView):
    template_name = 'user_register.html'

    def get(self,request):
        
        template_dict = dict(
            
        )
        return render(request,self.template_name,template_dict)
    
    def post(self,request):
        data_form = request.POST
        print(data_form)
        data_ld = user_register_main(data_form)
        ret_json = dict(data=data_ld)
        return JsonResponse(ret_json)
    