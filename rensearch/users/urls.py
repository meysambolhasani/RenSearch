
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('user-profile/<int:pk>/', views.user_profile, name='user-profile'),
    path('user-account/', views.user_account, name='user-account'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="users/reset_password.html"),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="users/reset_password_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/reset.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="users/reset_password_complete.html"),
         name="password_reset_complete"),

    path('edit-account/', views.edit_account, name='edit-account'),
    path('add-skill/', views.add_skill, name='add-skill'),
    path('update-skill/<int:pk>/', views.update_skill, name='update-skill'),
    path('delete-skill/<int:pk>/', views.delete_skill, name='delete-skill'),

    path('inbox/', views.inbox, name="inbox"),
    path('message/<int:pk>/', views.viewMessage, name="message"),
    path('create-message/<int:pk>/', views.createMessage, name="create-message"),
]


# 1 - User submits email for reset              //PasswordResetView.as_view()           //name="reset_password"
# 2 - Email sent message                        //PasswordResetDoneView.as_view()        //name="passsword_reset_done"
# 3 - Email with link and reset instructions    //PasswordResetConfirmView()            //name="password_reset_confirm"
# 4 - Password successfully reset message       //PasswordResetCompleteView.as_view()   //name="password_reset_complete"
