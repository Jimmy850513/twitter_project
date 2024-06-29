
from django.urls import path,include
from .twitter_views import twitter_views01
from .twitter_views import user_register
from .twitter_views import user_login
from .twitter_views import user_profile
from .twitter_views import twitter_views_post
from .twitter_views import add_post
from .twitter_views import personal_views_post
from .twitter_views import personal_update_post
urlpatterns = [
    path('',twitter_views01.twitter_views01.as_view(),name='twitter_views01'),
    path('user_register/',user_register.User_rigister.as_view(),name='user_register'),
    path('user_login/',user_login.User_login.as_view(),name='user_login'),
    path('user_profile/',user_profile.User_profile.as_view(),name='user_profile'),
    path('user_logout/',user_login.User_logout.as_view(),name='user_logout'),
    path('twitter_views_post/<int:post_id>',twitter_views_post.twitter_views_post.as_view(),name='twitter_views_post'),
    path('add_post/',add_post.AddPost.as_view(),name='add_post'),
    path('personal_views_post/',personal_views_post.Personal_views_post.as_view(),name='personal_views_post'),
    path('personal_update_post/<int:post_id>',personal_update_post.Personal_update_post.as_view(),name='personal_update_post'),
    path('personal_update_post2/',personal_update_post.Personal_update_post2.as_view(),name='personal_update_post2'),
    path('add_comment/',twitter_views_post.Add_Comment.as_view(),name='add_comment'),
    
]
