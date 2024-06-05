from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Customer, CustomerProfile, Staff, StaffProfile, User, Toy, ToyType, ToyModal
from .forms import CustomerRegistrationForm
from .views import *

class Authentication(TestCase):
    def test_customer_register(self):
        response = self.client.post(reverse('customer_register'), {'username': 'testcustomer', 'password': 'testpassword', 'is_18': True, 'phonenumber': '1234567890', 'city': 'Test City', 'address': 'Test Address', 'name': 'Test Name'})
        self.assertEqual(response.status_code, 200)  

    def test_customer_login(self):
        customer = Customer.objects.create(username='testcustomer', password='testpassword')
        response = self.client.post(reverse('customer_login'), {'username': 'testcustomer', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)

    def setUp(self):
        staff = Staff.objects.create(username='teststaff', password='testpassword')
        self.staff = StaffProfile.objects.create(staff = staff)

    def test_staff_login(self):
        response = self.client.post(reverse('staff_login'), {'username': 'teststaff', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  

    def test_invalid_staff_login(self):
        response = self.client.post(reverse('staff_login'), {'username': 'nonexistentstaff', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)  

    def test_nonexistent_staff_login(self):
        response = self.client.post(reverse('staff_login'), {'username': 'nonexistentstaff', 'password': 'password'})
        self.assertEqual(response.status_code, 200)

class Edit(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(username='testcustomer', password='testpassword')
        self.customer_profile = CustomerProfile.objects.create(customer=self.customer, phonenumber='1234567890', city='Test City', address='Test Address', name='Test Name')

    def test_customer_edit_post(self):
        self.client.force_login(self.customer)
        response = self.client.post(reverse('customer_edit'), {'username': 'testcustomer', 'password':'testpassword', 'phonenumber': '9876543210', 'city': 'New City', 'address': 'New Address', 'name': 'New Name'})
        self.assertEqual(response.status_code, 302)

        updated_customer_profile = CustomerProfile.objects.get(customer=self.customer)
        self.assertEqual(updated_customer_profile.phonenumber, '9876543210')

    def test_customer_edit_get(self):
        self.client.force_login(self.customer)
        response = self.client.get(reverse('customer_edit'))
        self.assertEqual(response.status_code, 200) 

    def test_customer_edit_template(self):
        self.client.force_login(self.customer)
        response = self.client.get(reverse('customer_edit'))
        self.assertTemplateUsed(response, 'edit/customer_edit.html') 

class Read(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(username='testcustomer', password='testpassword')
        self.customer_profile = CustomerProfile.objects.create(customer=self.customer, phonenumber='1234567890', city='Test City', address='Test Address', name='Test Name')

    def test_customer_read(self):
        self.client.force_login(self.customer)
        response = self.client.get(reverse('customer_read'))
        self.assertEqual(response.status_code, 200)

    def test_customer_read_template(self):
        self.client.force_login(self.customer)
        response = self.client.get(reverse('customer_read'))
        self.assertTemplateUsed(response, 'read/customer_read.html')

class LogoutDelete(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_log_out_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('log_out'))
        self.assertEqual(response.status_code, 302) 

    def test_log_out_unauthenticated_user(self):
        response = self.client.get(reverse('log_out'))
        self.assertEqual(response.status_code, 302) 

    def test_delete_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('delete', args=[self.user.id]))
        self.assertEqual(response.status_code, 302) 

    def test_delete_unauthenticated_user(self):
        response = self.client.get(reverse('delete', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)  

class SaveFeedbackViewTests(TestCase):
    def setUp(self):
        toyModal = ToyModal.objects.create(modal = 'Test Modal')
        toyType = ToyType.objects.create(name = 'Test Type')
        self.toy = Toy.objects.create(name='Test Toy', price=10, type = toyType, modals = toyModal)
        self.customer = Customer.objects.create(username='testcustomer', password='testpassword')
        self.customer_profile = CustomerProfile.objects.create(customer=self.customer, phonenumber='1234567890', city='Test City', address='Test Address', name='Test Name')

    def test_save_feedback_customer_authenticated(self):
        self.client.force_login(self.customer)
        response = self.client.post(reverse('feedback form'), {'feedback_text': 'Test feedback'})
        self.assertEqual(response.status_code, 200)

    def test_save_feedback_customer_unauthenticated(self):
        response = self.client.post(reverse('feedback form'), {'feedback_text': 'Test feedback'})
        self.assertEqual(response.status_code, 403)

class BuyViewTests(TestCase):
    def setUp(self):
        toyModal = ToyModal.objects.create(modal = 'Test Modal')
        toyType = ToyType.objects.create(name = 'Test Type')
        self.toy = Toy.objects.create(name='Test Toy', price=10, type = toyType, modals = toyModal)
        self.customer = Customer.objects.create(username='testcustomer', password='testpassword')
        self.customer_profile = CustomerProfile.objects.create(customer=self.customer, phonenumber='1234567890', city='Test City', address='Test Address', name='Test Name')

    def test_buy_customer_authenticated(self):
        self.client.force_login(self.customer)
        response = self.client.post(reverse('buy', args=[self.toy.id]), {'quantity': 1, 'completion_date': '2022-12-31', 'promo_code': 'TEST'})
        self.assertEqual(response.status_code, 400) 

    def test_buy_customer_unauthenticated(self):
        response = self.client.post(reverse('buy', args=[self.toy.id]), {'quantity': 1, 'completion_date': '2022-12-31', 'promo_code': 'TEST'})
        self.assertEqual(response.status_code, 403) 

