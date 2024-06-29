from django.views.generic import TemplateView
from django.shortcuts import render
from database_connect.database_connect import Db_connect

class DataDamend(Db_connect):
    def __init__(self):
        super().__init__()
    
    def stmt_select_all_post(self):
        stmt = """SELECT *
        FROM user_post"""
        rows = self.db_fetchall(stmt)
        return rows
    

    def __str__(self):
        return "SQL Query"


"""
main processing
"""
def user_post_main():
    dbh = DataDamend()
    user_post = dbh.stmt_select_all_post()
    data_ld = list()
    for data in user_post:
        data_ld.append(dict(**data))
    return data_ld

def add_post_main():
    dbh = DataDamend()
    

"""
url interface
"""
class twitter_views01(TemplateView):
    template_name = 'twitter_views.html'

    def get(self,request):
        data_ld = user_post_main()
        user_id = request.session.get('user_id','')
        username = request.session.get('username','')
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