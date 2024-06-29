from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import logout
# Create your views here.


class CheckSession(TemplateView):
    template_name = 'index.html'
    
    def get(self,request):
        user_id = request.session.get('user_id',None)
        username = request.session.get('username',None)
        outline_d = {'user_id':user_id,'username':username}
        template_dict = dict(
            outline_d=outline_d
        )
        return render(request,self.template_name,template_dict)
    
    def post(self,request):
        template_dict = dict()
        logout(request)
        return render(request,self.template_name,template_dict)