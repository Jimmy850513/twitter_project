from django.views.generic import TemplateView
from django.shortcuts import render
from database_connect.database_connect import Db_connect
from django.http import JsonResponse
class DataDamend(Db_connect):
    def __init__(self):
        super().__init__()
    
    def stmt_select_personal_post(self):
        stmt = """SELECT *
        FROM user_post
        WHERE user_id=%(user_id)s
        and post_id=%(post_id)s"""
        return stmt
    
    def stmt_update_personal_post(self):
        stmt = """UPDATE user_post SET
        post_title = %(post_title)s,
        post_body = %(post_body)s,
        update_time = NOW()
        WHERE post_id = %(post_id)s"""
        return stmt
    
    def stmt_delete_personal_post(self):
        stmt = """DELETE  FROM user_post
        WHERE post_id = %(post_id)s"""
        return stmt
    
    def __str__(self):
        return "SQL Query"


"""
main processing
"""
def user_post_main(user_id,post_id):
    dbh = DataDamend()
    personal_post = dbh.db_fetchall(
        dbh.stmt_select_personal_post(),{'user_id':str(user_id),'post_id':post_id}
        )
    data_ld = list()
    for data in personal_post:
        data_ld.append({**data})
    return data_ld

def update_post_main(data_form):
    dbh = DataDamend()
    post_title = data_form['post_title']
    post_body = data_form['post_body']
    post_id = data_form['post_id']
    post_dict = dict(post_title=post_title,post_body=post_body,post_id=post_id)
    try:
        dbh.db_execute(dbh.stmt_update_personal_post(),post_dict)
        data_ld = dict(msg='更新成功',status='OK')
    except Exception as e :
        print(e)
        data_ld = dict(msg='更新失敗',status='ERROR')
    return data_ld

def delete_post_main(data_form):
    dbh = DataDamend()
    post_id = data_form['post_id']
    try:
        dbh.db_execute(dbh.stmt_delete_personal_post(),{'post_id':post_id})
        data_ld = dict(msg='刪除成功',status='OK')
    except Exception as e:
        data_ld = dict(msg='刪除失敗',status='ERROR')
        print(e)
    return data_ld

"""
url interface
"""
class Personal_update_post(TemplateView):
    template_name = 'personal_update_post.html'

    def get(self,request,**kwargs):
        user_id = request.session.get('user_id','')
        username = request.session.get('username','')
        post_id=kwargs.get('post_id','')
        outline_d = {
            'user_id':user_id,
            'username':username,
            "post_id":post_id
        }
        data_ld = user_post_main(user_id,post_id)
        print(outline_d)
        template_dict = dict(
            outline_d=outline_d,
            data_ld=data_ld
        )
        return render(request,self.template_name,template_dict)
    
    def post(self,request,**kwargs):
        
        template_dict = {

        }
        return render(request,self.template_name,template_dict)
    
class Personal_update_post2(TemplateView):
    def post(self,request):
        data_form  = request.POST
        user_id = request.session.get('user_id','')
        username = request.session.get('username','')
        
        print(data_form)
        op = data_form['fmTextOP']
        if op == 'UPDATE':
            data_ld = update_post_main(data_form)
            ret_json = dict(data=data_ld)
            return JsonResponse(ret_json)
        elif op == 'DELETE':
            data_ld = delete_post_main(data_form)
            ret_json = dict(data=data_ld)
            return JsonResponse(ret_json)