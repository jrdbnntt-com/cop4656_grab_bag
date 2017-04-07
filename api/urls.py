from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'test/simple_post_test$', views.test.SimplePostTestView.as_view()),
    url(r'test/get/simple_get_test$', views.test.get.SimpleGetTestView.as_view()),

]
