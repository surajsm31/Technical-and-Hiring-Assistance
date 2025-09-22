from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    # def ready(self):
    #     em = "ssmtest31@gmail.com"
    #     pw = "SurajTest@315"
    #     ad = Admin(Email=em,Pass=pw)
    #     ad.save()

        # print("Django project has started!")

