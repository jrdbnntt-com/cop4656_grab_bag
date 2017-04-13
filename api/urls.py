from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'test/simple_post_test$', views.test.SimplePostTestView.as_view()),
    url(r'test/get/simple_get_test$', views.test.get.SimpleGetTestView.as_view()),

    url(r'user/login$', views.user.LogInView.as_view()),
    url(r'user/logout$', views.user.LogOutView.as_view()),
    url(r'user/register$', views.user.RegisterView.as_view()),

    url(r'player/update_location$', views.player.UpdateLocationView.as_view()),

    url(r'game/create$', views.game.CreateView.as_view()),
    url(r'game/join$', views.game.JoinView.as_view()),
    url(r'game/start$', views.game.StartView.as_view()),

    url(r'game/get/summary', views.game.get.SummaryView.as_view())
]
