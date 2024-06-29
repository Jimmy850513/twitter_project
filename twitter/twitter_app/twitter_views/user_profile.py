from django.views.generic import TemplateView
from django.shortcuts import render
from database_connect.database_connect import Db_connect
from django.http import JsonResponse, HttpResponse
from datetime import datetime
class DataDamend(Db_connect):
    def __init__(self):
        super().__init__()

    def stmt_select_personal_profile(self):
        stmt = """select * FROM user_profile
        WHERE user_id = %(user_id)s"""
        return stmt
    
    def update_user_profile(self):
        stmt = """UPDATE user_profile SET
        job_title=%(job_title)s,
        user_profile1=%(user_profile1)s,
        user_profile2=%(user_profile2)s,
        user_profile3=%(user_profile3)s,
        user_birthday=%(user_birthday)s,
        last_update_time=NOW()
        WHERE user_id = %(user_id)s
        """
        return stmt
    
    def update_job_title(self):
        stmt = """UPDATE user_profile SET job_title=%(job_title)s,last_update_time=NOW()
        WHERE user_id = %(user_id)s"""
        return stmt
    
    def update_user_profile1(self):
        stmt = """UPDATE user_profile SET user_profile1 = %(user_profile1)s,last_update_time=NOW()
        WHERE user_id = %(user_id)s"""
        return stmt
    
    def update_user_profile2(self):
        stmt = """UPDATE user_profile SET user_profile2 = %(user_profile2)s,last_update_time=NOW()
        WHERE user_id = %(user_id)s"""
        return stmt
    
    def update_user_profile3(self):
        stmt = """UPDATE user_profile SET user_profile3 = %(user_profile3)s,last_update_time=NOW()
        WHERE user_id = %(user_id)s"""
        return stmt
    
    def update_user_birthday(self):
        stmt = """UPDATE user_profile SET user_birthday = %(user_birthday)s,last_update_time=NOW()
        WHERE user_id = %(user_id)s"""
        return stmt
    
    def __str__(self):
        return "SQL Query"


"""
main processing
"""
def user_profile_main(user_id):
    dbh = DataDamend()
    data_ld = dict()
    personal_file = dbh.db_fetchone(dbh.stmt_select_personal_profile(),{'user_id':user_id})
    if personal_file:
        data_ld['username'] = personal_file['username'] if personal_file['username'] else ''
        data_ld['user_id'] = personal_file['user_id'] if personal_file['user_id'] else ''
        data_ld['user_profile1'] = personal_file['user_profile1'] if personal_file['user_profile1'] else '尚未編輯'
        data_ld['user_profile2'] = personal_file['user_profile2'] if personal_file['user_profile2'] else '尚未編輯'
        data_ld['user_profile3'] = personal_file['user_profile3'] if personal_file['user_profile3'] else '尚未編輯'
        data_ld['user_birthday'] = personal_file['user_birthday'].strftime('%Y-%m-%d') if personal_file['user_birthday'] else ''
        data_ld['job_title'] = personal_file['job_title'] if personal_file['job_title'] else '尚未編輯'
    print(data_ld)
    return data_ld
    
def user_profile_save(data_form,user_id):
    dbh = DataDamend()
    job_title = data_form['job_title']
    user_profile1 = data_form['user_profile1']
    user_profile2 = data_form['user_profile2']
    user_profile3 = data_form['user_profile3']
    user_birthday = data_form['user_birthday']
    
    data_ld = dict()
    if job_title:
        dbh.db_execute(dbh.update_job_title(),{'job_title':job_title,'user_id':user_id})
    elif user_profile1:
        dbh.db_execute(dbh.update_user_profile1(),{'user_profile1':user_profile1,'user_id':user_id})
    elif user_profile2:
        dbh.db_execute(dbh.update_user_profile2(),{'user_profile2':user_profile2,'user_id':user_id})
    elif user_profile3:
        dbh.db_execute(dbh.update_user_profile3(),{'user_profile3':user_profile3,'user_id':user_id})
    elif user_birthday:
        dbh.db_execute(dbh.update_user_birthday(),{'user_birthday':user_birthday,'user_id':user_id})
    data_ld = dbh.db_fetchone(dbh.stmt_select_personal_profile(),{'user_id':user_id})
    personal_file = dbh.db_fetchone(dbh.stmt_select_personal_profile(),{'user_id':user_id})
    if personal_file:
        data_ld['username'] = personal_file['username']
        data_ld['user_id'] = personal_file['user_id']
        data_ld['user_profile1'] = personal_file['user_profile1']
        data_ld['user_profile2'] = personal_file['user_profile2']
        data_ld['user_profile3'] = personal_file['user_profile3']
        data_ld['user_birthday'] = personal_file['user_birthday']
        data_ld['job_title'] = personal_file['job_title']
    return data_ld
"""
url interface
"""
class User_profile(TemplateView):
    template_name = 'user_profile.html'

    def get(self,request):
        user_id = request.session.get('user_id',None)
        username = request.session.get('username',None)
        outline_d = {'user_id':user_id,'username':username}
        if username and user_id:
            data_ld = user_profile_main(user_id)
        else:
            data_ld = dict()
        template_dict = dict(
            data_ld=data_ld,
            outline_d=outline_d
        )
        return render(request,self.template_name,template_dict)
    
    def post(self,request):
        data_form = request.POST
        user_id = request.session['user_id']
        op = data_form['fmTextOP']
        if op == 'SAVE':
            data_ld = user_profile_save(data_form,user_id)
            ret_json = dict(data=data_ld)
            print(ret_json)
            return JsonResponse(ret_json)
        template_dict = {

        }
        return render(request,self.template_name,template_dict)