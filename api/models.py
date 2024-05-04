from django.db import models
from django.contrib.auth.models import User
from django.db.models import F

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Level(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name


class Subject(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name



class School(models.Model):
  user = models.OneToOneField(CustomUser, null=True, blank=True, on_delete=models.CASCADE, unique=True, related_name='school')
  profile_image = models.ImageField(upload_to='schools/', blank=True, null=True)
  name = models.CharField(max_length=100, blank=True, null=True)
  levels = models.ManyToManyField(Level, blank=True, null=True)
  subjects = models.ManyToManyField(Subject, blank=True, null=True)

  def __str__(self):
    return str(self.name)


class Teacher(models.Model):
  phone = models.CharField(max_length=20, blank=True, null=True)
  levels = models.ManyToManyField(Level, blank=True, null=True)
  subjects = models.ManyToManyField(Subject, blank=True, null=True)
  profile_image = models.ImageField(upload_to='teachers/', blank=True, null=True)

  def __str__(self):
    return self.user.username


class Student(models.Model):
  phone = models.CharField(max_length=20)
  levels = models.ManyToManyField(Level)
  profile_image = models.ImageField(upload_to='students/', blank=True)

  def __str__(self):
    return self.user.username






class WebSite(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
  details = models.JSONField(null=True, blank=True)

  # def __str__(self):
    # return str(self.user.username)







class Product(models.Model):
  image = models.ImageField(upload_to='books/',null=True, blank=True)
  levels = models.ManyToManyField(Level)
  name = models.CharField(max_length=100)
  description = models.TextField()
  price = models.FloatField()
  quantity = models.IntegerField()
  min_quantity = models.IntegerField(null=True, blank=True)

  def __str__(self):
    return self.name
  


class Cart(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)



class Order(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # school or teacher or student
  student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=100)
  description = models.TextField(null=True, blank=True)
  phone = models.CharField(max_length=20)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  total_price = models.FloatField(null=True, blank=True, default=0)
  is_paied = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.product.name
  
  def save(self, *args, **kwargs):
    # calculate total price
    self.total_price = self.product.price * self.quantity

    # quantity update
    new_quantity = self.quantity
    try:
      old_quantity = Order.objects.get(id=self.id).quantity
    except:
      old_quantity = 0

    diff = new_quantity - old_quantity

    self.product.quantity -= diff
    self.product.save()
    super().save(*args, **kwargs)

  def delete(self, *args, **kwargs):
    self.product.quantity += self.quantity
    self.product.save()
    super().delete(*args, **kwargs)








