from django.views.generic import TemplateView
from django.shortcuts import render
from database_connect.database_connect import Db_connect
from django.http import JsonResponse
class DataDamend(Db_connect):
    def __init__(self):
        super().__init__()
    
    def stmt_select_one_post(self):
        stmt = """SELECT * FROM user_post
        WHERE post_id = %(post_id)s"""
        return stmt
    
    def get_comment_on_one_post(self):
        stmt = """SELECT post_id, 
        user_id, username, post_comment, comment_input_time, comment_update_time,comment_id
        FROM public.user_comment
        WHERE post_id = %(post_id)s
        order by comment_update_time ASC;"""
        return stmt

    def insert_into_post_comment(self):
        stmt = """INSERT INTO user_comment
        (post_id,user_id,username,post_comment,comment_input_time)
        VALUES(%(post_id)s,%(user_id)s,%(username)s,%(post_comment)s,NOW())"""
        return stmt
    
    def update_post_comment(self):
        stmt = """UPDATE user_comment
        SET post_comment = %(post_comment)s,
        comment_update_time = NOW()
        WHERE comment_id = %(comment_id)s"""
        return stmt
    
    def delete_post_comment(self):
        stmt = """DELETE FROM user_comment
        WHERE comment_id = %(comment_id)s"""
        return stmt
    
    def insert_post_like_by_user(self):
        stmt = """INSERT INTO post_like(
            post_id,like,like_by_user,like_user_id,like_time
            )VALUES(%(post_id)s,TRUE,%(like_by_user)s,%(like_user_id)s,NOW())"""
        return stmt
    
    def update_post_like_user(self):
        stmt = """UPDATE post_like
        SET like = FALSE
        WHERE post_id =%(post_id)s
        and like_user_id=%(user_id)s"""
        return stmt
    
    def get_post_like_by_user(self):
        stmt = """SELECT * FROM post_like
        WHERE like_user_id = %(user_id)s
        and post_id = %(post_id)s"""
        return stmt
    
    def get_follower_by_user(self):
        stmt = """SELECT user_id, user_name, 
        user_follower_id, user_follower_name, 
        follow_date, cancel_follow
        FROM public.user_follower
        WHERE user_follwer_id = %(user_follower_id)s"""
        return stmt

    def __str__(self):
        return "SQL Query"


"""
main processing
"""
def get_post_main(post_id,user_id):
    dbh = DataDamend()
    post_data = dbh.db_fetchall(dbh.stmt_select_one_post(),{'post_id':post_id})
    post_comment = dbh.db_fetchall(dbh.get_comment_on_one_post(),{'post_id':post_id})
    post_like = dbh.db_fetchall(dbh.get_post_like_by_user(),{'user_id':user_id,'post_id':post_id})
    data_ld = list()
    data_ld2 = list()
    for data in post_data:
        data_ld.append({**data})
        
    for data in post_comment:
        data_ld2.append({**data})
    
    outline_d = dict()
    for data in post_like:
        if data['like']:
            outline_d['like'] = 'true'
        else:
            outline_d['like'] = 'false'          
      
    return data_ld,data_ld2


def insert_into_post_comment(data_form,user_id,username):
    dbh = DataDamend()
    post_comment = data_form['post_comment'].strip()
    post_id = data_form['post_id']
    data_dict = dict(
        post_id=post_id,
        post_comment=post_comment,
        user_id=user_id,
        username=username
    )
    try:
        dbh.db_execute(dbh.insert_into_post_comment(),data_dict)
        data_ld = dict(msg="新增成功",status="OK")
    except Exception as e:
        data_ld = dict(msg="新增失敗",status="ERROR")
    return data_ld
    
def update_post_comment(data_form):
    dbh = DataDamend()
    post_comment = data_form['post_comment']
    comment_id = data_form['comment_id']
    print(comment_id)
    data_dict = dict(
        post_comment=post_comment,
        comment_id=comment_id
    )
    try:
        dbh.db_execute(dbh.update_post_comment(),data_dict)
        data_ld = dict(msg="更新成功",status='OK')
    except Exception as e:
        data_ld = dict(msg='更新失敗',status='ERROR')
    return data_ld
    
def delete_post_comment(data_form):
    dbh = DataDamend()
    comment_id = data_form['comment_id']
    try:
        dbh.db_execute(dbh.delete_post_comment(),{'comment_id':comment_id})
        data_ld = dict(msg="刪除成功",status="OK")
    except Exception as e:
        data_ld = dict(msg="刪除失敗",status="ERROR")
    return data_ld

def like_post(data_form,user_id,user_name):
    dbh = DataDamend()
    post_id = data_form['post_id']
    like = data_form['like_post']
    data_dict = dict()
    dbh.db_execute(dbh.insert_post_like_by_user(),)
    
"""
url interface
"""
class twitter_views_post(TemplateView):
    template_name = 'twitter_views_post.html'

    def get(self,request,**kwargs):
        user_id = request.session.get('user_id',None)
        user_name = request.session.get('username',None)
        post_id = kwargs.get('post_id')
        outline_d = dict(user_id=user_id,user_name=user_name)
        data_ld,data_ld2 = get_post_main(post_id,user_id)
        template_dict = dict(
            outline_d=outline_d,
            data_ld=data_ld,
            data_ld2 = data_ld2
        )
        return render(request,self.template_name,template_dict)
    
    def post(self,request):
        data_form = request.POST
        op = data_form['fmTextOP']
        data_ld = list()
        
        template_dict = {

        }
        return render(request,self.template_name,template_dict)

class Add_Comment(TemplateView):
    template_name = 'twitter_views_post.html'
    def post(self,request):
        data_form = request.POST
        user_id = request.session.get('user_id','')
        username = request.session.get('username','')
        dbh = DataDamend()
        op = data_form['fmTextOP']
        if op == "CREATE":
            data_ld = insert_into_post_comment(data_form,user_id,username)
            ret_json = dict(data=data_ld)
            return JsonResponse(ret_json)
        elif op == 'UPDATE':
            data_ld = update_post_comment(data_form)
            ret_json = dict(data=data_ld)
            return JsonResponse(ret_json)
        elif op == 'DELETE':
            data_ld = delete_post_comment(data_form)
            ret_json = dict(data=data_ld)
            return JsonResponse(ret_json)
        elif op == 'LIKE':
            data_ld = like_post(data_form)
            ret_json = dict(data=data_ld)
            return JsonResponse(ret_json)
        elif op == 'NOTLIKE':
            pass
        template_dict = {

        }
        return render(request,self.template_name,template_dict)