from django.conf.urls import url

from DoAnApi.api import PostList, PostDetail, UserHasPostApi, LikePost, ListComment, UserAPI, Login, Logout, Signup, \
    ActiveUser, SaveComment,UserCreatePost, UserPostDetail, PostdetailWithAuth, SearchPost, ChangePassword, \
    ForgetPassword, ResetPassword, InputpPin

urlpatterns = [
    url(r'^posts/$', PostList.as_view()),
    url(r'^posts/(?P<slug>[\w-]+)/$', PostDetail.as_view()),
    url(r'^post_with_auth/(?P<slug>[\w-]+)/$', PostdetailWithAuth.as_view()),
    url(r'^user_create_post/$', UserCreatePost.as_view()),
    url(r'^user/$', UserHasPostApi.as_view()),
    url(r'^user/(?P<slug>[\w-]+)/$', UserPostDetail.as_view()),
    url(r'^like_post/$', LikePost.as_view()),
    url(r'^comment/$', ListComment.as_view()),
    url(r'^save_comment/$', SaveComment.as_view()),
    url(r'^get_user/$', UserAPI.as_view()),
    url(r'^login/$', Login.as_view()),
    url(r'^logout/$', Logout.as_view()),
    url(r'^signup/$', Signup.as_view()),
    url(r'^active/$', ActiveUser.as_view()),
    url(r'^search/$', SearchPost.as_view()),
    url(r'^change_password/$', ChangePassword.as_view()),
    url(r'^forget_password/$', ForgetPassword.as_view()),
    url(r'^input_pin/$', InputpPin.as_view()),
    url(r'^reset_password/$', ResetPassword.as_view()),
]