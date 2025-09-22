from django.contrib import admin
from django.urls import path,include

from .import views
from .views import alert_on_tab_change,next_page


urlpatterns = [
    path('',views.index),
    path('submit_feedback',views.submit_feedback),

     #Developer Section
    path('developerlogin',views.developerlogin),
    path('dregister', views.dregister),
    path('forget_dev_password', views.forget),
    path('reset_dev_password', views.reset_password),
    path('verify_dev_fpass', views.verify_dev_fpass),
    # path('update_dev_pass', views.update_dev_pass),
    # path('register', views.register),
    path('register', views.send_otp),
    path("verify_otp", views.verify_otp, name="verify_otp"),
    path('login_validate',views.login_validate),
    path('ddashboard',views.ddashboard),
    path('home',views.home),
    path('analyze/', views.analyze_resume, name='analyze_resume'),
    path('profile',views.profile),
    path('update_dprofile',views.update_dprofile),
    path('dprofile_update',views.dprofile_update),
    path('dpass_change',views.dpass_change),
    path('change_dpass',views.change_dpass),
    path('quiz',views.quiz),
    path('submit',views.submit),
    path('score',views.score),
    path('certificate',views.certificate),
    # path('result',views.result),
    path('dlogout',views.dlogout),


    #HR Section
    path('hrlogin',views.hrlogin),
    path('forget_hr_password', views.forgetpass),
    path('reset_hr_password', views.reset_hr_password),
    path('verify_hr_fpass', views.verify_hr_fpass),
    path('hrregister',views.hrregister),
    path('HR',views.otp_to_hr),
    path('verify_hr',views.verify_hr),
    path('hr_validate',views.hr_validate),
    path('hrdashboard',views.hrdashboard),
    path('hr_profile',views.hrprofile),
    path('update_hrprofile',views.update_hrprofile),
    path('updatehrprofile',views.updatehrprofile),
    path('hrpass_change',views.hrpass_change),
    path('change_hrpass',views.change_hrpass),
    path('search',views.search),
    path('view/<int:id>',views.view),
    path('hrlogout',views.hrlogout),


   #Admin Section
    path('admin_login',views.admin_login),
    path('admin_loginvalidate',views.admin_loginvalidate),
    path('Admin1',views.admin),
    path('admin_profile',views.admin_profile),
    path('change_pass',views.change_pass),
    path('pass_change',views.pass_change),
    path('update_profile',views.update_profile),
    path('profile_update',views.profile_update),
    path('admin_logout',views.admin_logout),
    path('admin_clear',views.admin_clear),

    path('dev',views.dev_info),
    path('dev_register',views.dev_register),
    path('send_otp_to_dev',views.send_otp_to_dev),
    path('verify_dev_otp',views.verify_dev_otp),
    path('delete_dev/<int:id>',views.delete_dev),
    path('dev_test',views.dtest_info),

    path('hr',views.hr_info),
    path('hr_register',views.hr_register),
    path('send_otp_to_hr',views.send_otp_to_hr),
    path('verify_hr_otp',views.verify_hr_otp),
    path('delete_hr/<int:id>',views.delete_hr),

    path('test',views.test_que),
    path('add_test',views.add_test_que),
    path('add_question',views.add_question),
    path('delete_que/<int:id>',views.delete_que),

    path('test_cate',views.test_cate),
    path('add_test_cate',views.add_test_cate),
    path('add_cate',views.add_cate),
    path('delete_cate/<int:id>',views.delete_cate),

    path('feedback',views.feedback),

# from django.urls import path

   path('alert-on-tab-change/', alert_on_tab_change, name='alert_on_tab_change'),

   path('next-page/', next_page, name='next_page'),
]



