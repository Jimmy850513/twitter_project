from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from database_connect.database_connect import Db_connect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.contrib.auth import authenticate, login,logout

class DataDamend(Db_connect):
    def __init__(self):
        super().__init__()

    def stmt_select_auth_user(self):
        stmt = """SELECT * FROM auth_user
        WHERE username = %(username)s"""
        return stmt
    
    def stmt_select_user_account(self):
        stmt = """SELECT * FROM user_account
        WHERE username = %(username)s"""
        return stmt
    
    def __str__(self):
        return "SQL Query"


"""
main processing
"""
def user_login(data_form,req):
    dbh = DataDamend()
    username = data_form['username']
    password = data_form['password']
    data_dict = dict(username=username,password=password)
    user = authenticate(req,username=username,password=password)
    data_ld = dict()
    if user is not None:
        login(req,user)
        user_account = dbh.db_fetchall(dbh.stmt_select_user_account(),data_dict)
        if user_account:
            user_account = user_account[0] 
        req.session['user_id'] = user_account['id']
        req.session['username'] = user_account['username']
        data_ld = dict(msg='登入成功',status = 'OK',
                       user_id=user_account['id'],
                       username=user_account['username'])
    else:
        data_ld = dict(msg='登入失敗,請檢查帳號密碼',status='ERROR',username='',user_id='')
    return data_ld
"""
url interface
"""
class User_login(TemplateView):
    template_name = 'user_login.html'

    def get(self,request):
        data_ld = {"content":"user_login"}
        template_dict = dict(
            data_ld=data_ld
        )
        return render(request,self.template_name,template_dict)
    
    def post(self,request):
        data_form = request.POST

        op = data_form['fmTextOP']
        if op == 'SEARCH':
            data_ld = user_login(data_form,request)
            if data_ld['status'] == 'OK':
                request.session['user_id'] = data_ld['user_id']
                request.session['username'] = data_ld['username']
            ret_json = dict(data=data_ld)
            return JsonResponse(ret_json)
        template_dict = {

        }
        return render(request,self.template_name,template_dict)
    
class User_logout(TemplateView):
    def get(self,request):
        logout(request)
        return redirect('twitter_views01')
    def post(self,request):
        logout(request)
        return redirect('twitter_views01')