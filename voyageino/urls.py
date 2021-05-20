from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("",views.home_page),
    path('update', views.update, name='update'),
    path("tour/<int:id>", views.tour_page),
    path("categorie/<int:id>/<int:page>", views.get_categorie),
    path("categorie/<int:id>", views.get_categorie),
    path("search", views.search),
    path("operator/<int:id>", views.get_operator),
    path("operator/<int:id>/<int:page>", views.get_operator),
    path("operator", views.operator_page),
    path("add_favourites/<int:id>", views.add_favourites),
    path("remove_favourites/<int:id>", views.remove_favourites),
    path("subscribe", views.subscribe),
    path("newsletter_send", views.newsletter_send),
    path("login", views.login),
    path("login_process", views.login_process),
    path("logout", views.logout_process),

    path("scraping",views.scraping),
    path("intrepidtravel",views.intrepidtravel),
    path("tourradar", views.touraddar),
    path("traveltalk", views.travlertalks),
    path("globus", views.globus),
    path("cosmos",views.cosmos),
    
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
