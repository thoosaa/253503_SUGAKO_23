from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import re
from django.core.exceptions import ValidationError

class UserAccountManager(BaseUserManager): 
    def create_user(self, username, password=None): 
        if not username:
            raise ValueError("Username field is required!") 

        user = self.model(username=self.model.normalize_username(username))
        user.set_password(password) 
        user.save(using=self._db) 
        return user 

    def create_superuser(self, username, password): 
        user = self.create_user(username, password=password) 
        user.is_customer = False
        user.is_staff = False
        user.is_superuser = True
        user.save(using=self._db) 
        return user 

class User(AbstractBaseUser): 
    class Types(models.TextChoices): 
        CUSTOMER = "CUSTOMER" , "customer"
        STAFF = "STAFF" , "staff", 
        ADMIN = "ADMIN", 'admin'
    
    type = models.CharField(max_length = 8 , choices = Types.choices , default = Types.ADMIN) 
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True) 
    is_customer = models.BooleanField(default=False) 
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False) 

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'

    objects = UserAccountManager() 

    def has_perm(self, perm, obj=None): 
        return self.is_superuser

    def has_module_perms(self, app_label): 
        return True 

    def __str__(self): 
        return str(self.username)
    
class CustomerManager(models.Manager): 
    def create_user(self , username , password = None): 
        if not username or len(username) <= 0 :  
            raise  ValueError("username field is required !") 
        if not password : 
            raise ValueError("Password is must !") 
        username  = username.lower() 
        user = self.model( 
            username = username 
        ) 
        user.set_password(password) 
        user.save(using = self._db) 
        return user 
      
    def get_queryset(self , *args,  **kwargs): 
        queryset = super().get_queryset(*args , **kwargs) 
        queryset = queryset.filter(type = User.Types.CUSTOMER) 
        return queryset     
        
class Customer(User): 
    class Meta :  
        proxy = True
    objects = CustomerManager() 
      
    def save(self , *args , **kwargs): 
        if not self.pk:
            self.type = User.Types.CUSTOMER
        self.is_customer = True
        return super().save(*args , **kwargs) 
    
class CustomerProfile(models.Model):
    name = models.CharField(max_length=300)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
        regex=r"^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$",
        message="Phone number must be in the format '+375 (29) XXX-XX-XX'",
    )
    phonenumber = models.CharField(max_length=21, validators=[phone_regex])
    city = models.CharField(max_length=50)
    address = models.TextField(max_length=400)

    def __str__(self):
        return self.customer.username

class StaffManager(models.Manager): 
    def create_user(self , username , password = None): 
        if not username or len(username) <= 0 :  
            raise  ValueError("username field is required !") 
        if not password : 
            raise ValueError("Password is must !") 
        username = username.lower() 
        user = self.model( 
            username = username 
        ) 
        user.set_password(password) 
        user.save(using = self._db) 
        return user 
        
    def get_queryset(self , *args , **kwargs): 
        queryset = super().get_queryset(*args , **kwargs) 
        queryset = queryset.filter(type = User.Types.STAFF) 
        return queryset 
      
class Staff(User): 
    class Meta : 
        proxy = True
    objects = StaffManager() 
      
    def save(self  , *args , **kwargs): 
        if not self.pk:
            self.type = User.Types.STAFF
        self.is_staff = True
        return super().save(*args , **kwargs)

class StaffProfile(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone_regex = RegexValidator(
        regex=r"^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$",
        message="Phone number must be in the format '+375 (29) XXX-XX-XX'",
    )
    phonenumber = models.CharField(max_length=21, validators=[phone_regex])
    email = models.CharField(max_length=70)
    photo = models.ImageField(upload_to='images/')
    profession = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.staff.username

class PromoCode(models.Model):
    code = models.CharField(
        max_length=35,
        unique=True
    )
    expiration = models.DateField()
    discount = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(80)]
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
    
    def is_valid(self):
        return self.expiration >= timezone.now().date()
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('code'),
                name='promocode_name_case_insensitive_unique',
                violation_error_message = "Promocode already exists (case insensitive match)"
            ),
        ]

class ToyModal(models.Model):
    modal = models.CharField(
        max_length=200
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.modal

class ToyType(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True
    )
    promo_codes = models.ManyToManyField(PromoCode, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def display_promocode(self):
        return ', '.join(promocode.code for promocode in self.promo_codes.all())

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='toy_type_name_case_insensitive_unique',
                violation_error_message = "Toy type already exists (case insensitive match)"
            ),
        ]

class Toy(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(ToyType, on_delete=models.CASCADE) 
    modals = models.ForeignKey(ToyModal, on_delete=models.CASCADE)
    is_manufactured = models.BooleanField(default=True)
    price = models.DecimalField(default=1, decimal_places=2, max_digits=7)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} {self.modals}"


class Sale(models.Model):
    order_date = models.DateField(auto_now_add=True)
    completion_date = models.DateField(blank=True, null=True) 
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)]) 
    toy = models.ForeignKey(Toy, on_delete=models.CASCADE)

    customer = models.ForeignKey(CustomerProfile, on_delete=models.SET_NULL, null=True, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    promo_code = models.CharField(max_length=35, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.toy.name}"

    def apply_discount(self):
        promo_codes = self.toy.type.promo_codes.all()
        if self.promo_code:
            promo_code = promo_codes.filter(code=self.promo_code).first()
            if promo_code and promo_code.is_valid():
                discount = promo_code.discount
                total_price = self.toy.price * self.quantity
                discounted_price = total_price * (100 - discount) / 100
                return round(discounted_price, 2)
            else:
                self.promo_code = None
        return self.toy.price * self.quantity

    def save(self, *args, **kwargs):
        self.price = self.apply_discount()
        super().save(*args, **kwargs)


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        abstract = True

class News(BaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    class Meta:
        verbose_name = "news"
        verbose_name_plural = "news"

    def __str__(self):
        return f"{self.title}"
    

class FAQ(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    question = models.CharField(max_length=400)
    answer = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class About(models.Model):
    text = models.TextField(max_length=1200)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
    
class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Feedback(models.Model):
    text = models.TextField(max_length=500)
    toy = models.ForeignKey(Toy, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    rate = models.IntegerField(default = 0, validators = [MinValueValidator(1),MaxValueValidator(5)])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class PickUpPoints(models.Model):
    adress = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)