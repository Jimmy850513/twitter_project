from django.views.generic import TemplateView
from django.shortcuts import render
from database_connect.database_connect import Db_connect

class DataDamend(Db_connect):
    def __init__(self):
        super().__init__()
    
    def stmt_select_personal_post(self):
        stmt = """SELECT *
        FROM user_post
        WHERE user_id=%(user_id)s"""
        return stmt
    

    def __str__(self):
        return "SQL Query"


"""
main processing
"""
def user_post_main(user_id):
    dbh = DataDamend()
    personal_post = dbh.db_fetchall(dbh.stmt_select_personal_post(),{'user_id':str(user_id)})
    data_ld = list()
    for data in personal_post:
        if data['post_body']:
            data['post_body'] = data['post_body'].strip()
        data_ld.append(dict(
            post_id=data['post_id'],
            post_title=data['post_title'],
            post_body=data['post_body'],
            user_id=data['user_id'],
            username=data['username']
        ))
        
    return data_ld


    

"""
url interface
"""
class Personal_views_post(TemplateView):
    template_name = 'personal_post_views.html'

    def get(self,request,**kwargs):
        user_id = request.session.get('user_id','')
        username = request.session.get('username','')
        data_ld = user_post_main(user_id)
        print(data_ld)
        outline_d = {
            'user_id':user_id,
            'username':username
        }
        print(outline_d)
        template_dict = dict(
            data_ld=data_ld,
            outline_d=outline_d
        )
        return render(request,self.template_name,template_dict)
    
    def post(self,request):
        
        template_dict = {

        }
        return render(request,self.template_name,template_dict)