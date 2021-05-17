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
    path("search/<int:page>", views.search),
    path("search", views.search),
    path("operator/<int:id>", views.get_operator),
    path("operator/<int:id>/<int:page>", views.get_operator),
    path("operator", views.operator_page),
    path("get_favourites", views.get_favourites),
    path("add_favourites/<int:id>", views.add_favourites),
    path("subscribe", views.subscribe),
    path("newsletter_send", views.newsletter_send),
    
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
