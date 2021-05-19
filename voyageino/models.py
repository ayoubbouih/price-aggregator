from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator
from django.db.models import Count
from datetime import datetime
# Create your models here.
class Tour(models.Model):
    url = models.TextField()
    title = models.TextField()
    price= models.IntegerField(validators=[MinValueValidator(0)])
    details = models.TextField()
    duree = models.IntegerField(default=1)
    categorie = models.ForeignKey('categorie',on_delete=models.CASCADE)
    operator = models.ForeignKey('Operator',on_delete=models.CASCADE)
    cities = models.ManyToManyField("City",blank=False)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title
    def get_cities(self):
        return self.cities.all()
    def image(self):
        return self.image_set.first()
    def images(self):
        self.image_set.all()
    def printable_cities(self):
        cities = [city.name for city in self.get_cities()]
        return ", ".join(cities)+"."
    def next_depart(self):
        if self.depart_set.count() > 0:
            return self.depart_set.filter(from_date__gte=datetime.today()).first().print_from_date()
        else:
            return None
    def other_images(self):
        return self.image_set.all()[1:]

class City(models.Model):
    name = models.TextField()

    def publish(self):
        self.save()

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name

    def image(self):
        return self.tour_set.all()[self.id  % self.tour_set.count()].image

class categorie(models.Model):
    name = models.TextField()
    photo = models.ImageField(blank=True,null=True,upload_to='voyageino/static/img/categories/')


    def publish(self):
        self.save()


    def __str__(self):
        return self.name

    def image(self):
        l = str(self.photo).split("/")
        r = [l[-3],l[-2],l[-1]]
        return "/".join(r)

class Image(models.Model):
    tour = models.ForeignKey('tour',on_delete=models.CASCADE)
    url = models.TextField()

    def __str__(self):
        return self.url

class Depart(models.Model):
    tour = models.ForeignKey('tour',on_delete=models.CASCADE)
    from_date = models.DateTimeField(blank=True,null=True)
    to_date = models.DateTimeField(blank=True,null=True)
    price = models.IntegerField(validators=[MinValueValidator(0)])

    def print_from_date(self):
        return datetime.strftime(self.from_date,"%b %d, %Y")
    def print_to_date(self):
        return datetime.strftime(self.to_date,"%b %d, %Y")

class Operator(models.Model):
    name = models.TextField()
    image = models.ImageField(blank=True,null=True,upload_to='voyageino/static/img/operator/')
    url = models.URLField()
    description = models.TextField()

    def photo(self):
        l = str(self.image).split("/")
        r = [l[-3],l[-2],l[-1]]
        return "/".join(r)

    def choosed(self):
        counter = self.tour_set.annotate(departs_count=Count("depart"))
        return counter.order_by("-departs_count")[:3]

    def sample(self):
        #ops = self
        pass
        
class Subscriber(models.Model):
    email = models.EmailField()