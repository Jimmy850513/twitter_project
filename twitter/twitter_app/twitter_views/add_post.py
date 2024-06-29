from django.views.generic import TemplateView
from django.shortcuts import render
from database_connect.database_connect import Db_connect
from django.http import JsonResponse
class DataDamend(Db_connect):
    def __init__(self):
        super().__init__()
    
    def insert_into_user_post(self):
        stmt = """INSERT INTO user_post
        (user_id,username,post_title,post_body,post_date)
        VALUES
        (%(user_id)s,%(username)s,%(post_title)s,%(post_body)s,NOW())"""
        return stmt

    def __str__(self):
        return "SQL Query"


"""
main processing
"""

def user_add_post(data_form,user_id,username):
    dbh = DataDamend()
    post_title = data_form['post_title']
    post_body = data_form['post_body']
    data_ld = list()
    data_dict = dict(user_id=user_id,username=username,post_title=post_title,post_body=post_body)
    try:
        dbh.db_execute(dbh.insert_into_user_post(),data_dict)
        data_ld = dict(msg="新增成功",status = 'OK')
    except Exception as e:
        data_ld = dict(msg='新增貼文失敗',status='ERROR')
        print(e)
        
    return data_ld

"""
url interface
"""
class AddPost(TemplateView):
    template_name = 'add_post.html'

    def get(self,request):
        
        user_id = request.session.get('user_id','')
        username = request.session.get('username','')
        outline_d = {
            'user_id':user_id,
            'username':username
        }
        print(outline_d)
        template_dict = dict(
           outline_d=outline_d
        )
        return render(request,self.template_name,template_dict)
    
    def post(self,request):
        user_id = request.session.get('user_id','')
        username = request.session.get('username','')
        data_form = request.POST
        op = data_form['fmTextOP']
        if user_id and username:
            if op == 'SAVE':
                data_ld = user_add_post(data_form,user_id,username)
                ret_json = dict(data=data_ld)
                return JsonResponse(ret_json)
            
        template_dict = {

        }
        return render(request,self.template_name,template_dict)