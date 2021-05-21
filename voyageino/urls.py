from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("",views.home_page, name='home_page'),
    path('update', views.update, name='update'),
    path("tour/<int:id>", views.tour_page),
    path("categorie/<int:id>/<int:page>", views.get_categorie),
    path("categorie/<int:id>", views.get_categorie),
    path("search", views.search),
    path("operator/<int:id>", views.get_operator),
    path("operator/<int:id>/<int:page>", views.get_operator),
    path("operators", views.operators_page),
    path("favourites/",views.get_favourites),
    path("add_favourites/<int:id>", views.add_favourites),
    path("remove_favourites/<int:id>", views.remove_favourites),
    path("subscribe", views.subscribe),
    path("newsletter_send", views.newsletter_send),
    path("login", views.login_page, name="login_page"),
    path("login_process", views.login_process),
    path("logout", views.logout_process),
    path("register", views.register),
    path("register_process", views.register_process),
    path("profile", views.profile),
    path("password_change", views.password_change),
    path("password_change_process", views.password_change_process),


    path("scraping",views.scraping),
    path("intrepidtravel",views.intrepidtravel),
    path("tourradar", views.touraddar),
    path("traveltalk", views.travlertalks),
    path("globus", views.globus),
    path("cosmos",views.cosmos),
    
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
