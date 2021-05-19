from django.contrib import admin
from .models import Tour,City,categorie,Image,Depart,Operator,Subscriber

# Register your models here.
from django.contrib import messages
from django.utils.translation import ngettext

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("title", "categorie","price","duree","cities_count","departs_count","operator")

    def cities_count(self, obj):
        return obj.cities.count()
    
    def departs_count(self, obj):
        return obj.depart_set.count()
    
    def operator(self,obj):
        return obj.operator.name
    
    search_fields = ('title__startswith','title__endswith')

def combine_cities(self, request, queryset):
    name= queryset.first().name
    id = City.objects.latest('id').id+1
    new_city = City(id, name)
    new_city.save()
    updated = len(queryset)
    for city in queryset:
        for tour in city.tour_set.all():
            tour.cities.add(new_city)
            tour.cities.remove(city)
        city.delete()
    self.message_user(request,f"{updated} cities were combined to {name}", messages.SUCCESS)


@admin.register(City)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ("name","Tours_count")
    actions = [combine_cities]

    def Tours_count(self, obj):
        return int(obj.tour_set.count())


    

@admin.register(categorie)
class categorieAdmin(admin.ModelAdmin):
    list_display =("id", "name", "tour_count")

    def tour_count(self, obj):
        return obj.tour_set.count()


admin.site.register(Image)
@admin.register(Depart)
class DepartAdmin(admin.ModelAdmin):
    list_display =("tour_name", "from_date", "to_date","price")

    def tour_name(self,obj):
        return obj.tour.title


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url",'tours_count')

    def tours_count(self, obj):
        return obj.tour_set.count()

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("id", "email")