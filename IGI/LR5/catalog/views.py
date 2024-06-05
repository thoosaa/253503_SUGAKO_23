from collections import Counter
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from toyfactory.settings import LOGGING
from .forms import CustomerRegistrationForm, SaleForm, FeedbackForm
from .models import  User, CustomerProfile, Customer, Staff, StaffProfile, News, FAQ, Toy, Sale, ToyType, PromoCode, About, Job, Feedback, PickUpPoints
from django.contrib.auth import login, logout 
from .decorators import superuser_required, staff_required, customer_required, login_required
from datetime import datetime
from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncMonth
import requests
from statistics import mean, median, mode
from .utils import *
import logging 
import tzlocal
import calendar

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('catalog')

def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            is_18 = form.cleaned_data.get('is_18', False)
            if is_18:
                user = form.save()
                customer_profile = CustomerProfile(customer=user, phonenumber=form.cleaned_data['phonenumber'], city=form.cleaned_data['city'], address=form.cleaned_data['address'], name=form.cleaned_data['name'])
                customer_profile.save()
                logger.info('New customer registered: %s', user.username)
                return render(request, 'registration/customer_log.html')
            else:
                form.add_error('is_18', 'Вам должно быть минимум 18 лет.') 
    else:
        form = CustomerRegistrationForm()
    return render(request, 'registration/customer_reg.html', {'form': form})


def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            customer = Customer.objects.get(username=username, password = password)
            if customer is not None:
                login(request, customer)
                logger.info('Customer logged in: %s', customer.username)
                #customer_profile = CustomerProfile.objects.get(customer = customer)
                return redirect('home')
            else:
                logger.warning('Invalid login attempt for username: %s', username)
                return render(request, 'registration/customer_log.html', {'error': "Invalid login credentials."})
        except Customer.DoesNotExist:
            logger.warning('Customer account does not exist: %s', username) 
            return render(request, 'registration/customer_log.html', {'error': "Customer account does not exist."})
    else:
        return render(request, 'registration/customer_log.html')


def staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            staff = Staff.objects.get(username=username, password = password)
            if staff is not None:
                #request.user = staff
                login(request, staff)
                logger.info('Staff member {} logged in successfully.'.format(username))
                return redirect('home')
            else:
                logger.warning('Invalid login credentials for staff member {}.'.format(username))
                return render(request, 'registration/staff_log.html', {'error': "Invalid login credentials."})
        except Staff.DoesNotExist:
            logger.warning('Staff account with username {} does not exist.'.format(username))
            return render(request, 'registration/staff_log.html', {'error': "Staff account does not exist."})
    else:
        return render(request, 'registration/staff_log.html')

@customer_required
def customer_edit(request):
    if request.method == 'POST':
        customer_profile = CustomerProfile.objects.get(customer=request.user)
        customer = customer_profile.customer 

        customer.username = request.POST.get('username')
        customer.password = request.POST.get('password')
        customer.save()  

        customer_profile.phonenumber = request.POST.get('phonenumber')
        customer_profile.city = request.POST.get('city')
        customer_profile.address = request.POST.get('address')
        customer_profile.name = request.POST.get('name')
        customer_profile.save() 
        logger.info('Customer profile edited by staff member {}'.format(request.user.username))

        return redirect('home')

    else:
        customer_profile = CustomerProfile.objects.get(customer = request.user)
        return render(request, 'edit/customer_edit.html', {'customer': customer_profile})

@customer_required
def customer_read(request):   
    customer_profile = CustomerProfile.objects.get(customer = request.user)
    logger.info("Customer profile page accessed")
    user_timezone = tzlocal.get_localzone()
    current_date = datetime.now(user_timezone).date()
    current_date_formatted = current_date.strftime("%d/%m/%Y")

    calendar_text = calendar.month(
        datetime.now(user_timezone).year,
        datetime.now(user_timezone).month,
    )

    return render(request, 'read/customer_read.html', {'customer': customer_profile, "user_timezone":user_timezone, "current_date_formatted": current_date_formatted, "calendar_text": calendar_text})

@staff_required
def staff_edit(request):
    if request.method == 'POST':
        staff_profile = StaffProfile.objects.get(staff=request.user)
        staff = staff_profile.staff 

        staff.username = request.POST.get('username')
        staff.password = request.POST.get('password')
        staff.save()  

        staff_profile.name = request.POST.get('name')
        staff_profile.phonenumber = request.POST.get('phonenumber')
        staff_profile.email = request.POST.get('email')
        photo_file = request.FILES.get('photo')
        if photo_file:
            staff_profile.photo = photo_file
        staff_profile.profession = request.POST.get('profession')
        staff_profile.save() 
        logger.info('Staff profile edited by staff member {}'.format(request.user.username))
        return redirect('home')

    else:
        staff_profile = StaffProfile.objects.get(staff = request.user)
        return render(request, 'edit/staff_edit.html', {'staff': staff_profile})

@staff_required
def staff_read(request):
    staff_profile = StaffProfile.objects.get(staff = request.user)
    logger.info("Staff profile page accessed")
    return render(request, 'read/staff_read.html', {'staff': staff_profile})

def home(request):
    latest_news = News.objects.latest('created_at')
    logger.info("Home page accessed")
    return render(request, 'all/home.html', {'latest_news': latest_news})

def about(request):
    about = About.objects.get(id = 1)
    logger.info("About page accessed")
    return render(request, 'all/about.html', {'about': about})

@login_required
def log_out(request):
    logger.info('User {} logged out.'.format(request.user.username))
    logout(request)
    return redirect('home')

@login_required
def delete(request, id):
    try:
        user = User.objects.get(id=id)
        logger.info('User {} deleted.'.format(user.username))
        user.delete()
        return redirect('home')
    except User.DoesNotExist:
        return render(request, '<h2>Does not exist</h2>')

def news_view(request):
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    joke_data = response.json()

    setup = joke_data.get('setup', '')
    punchline = joke_data.get('punchline', '')

    news_list = News.objects.all()
    logger.info("News page accessed")
    return render(request, 'all/news.html', {'news_list': news_list, 'setup': setup, 'punchline': punchline})

def faq_view(request):
    faq_list = FAQ.objects.all()
    logger.info("FAQ list page accessed")
    return render(request, 'all/faq.html', {'faq_list': faq_list})

def contact_view(request):
    contact_list = StaffProfile.objects.all()
    logger.info("Contact list page accessed")
    return render(request, 'all/contact.html', {'contact_list': contact_list})

def confidentiality(request):
    logger.info("Politics of confidentiality page accessed")
    return render(request, 'all/politics_confidential.html')

def cat(request):
    toy_list = Toy.objects.all()
    logger.info('Catalog page accessed')
    return render(request, 'all/catalogue.html', {'toy_list': toy_list})

def search_toys(request):
    query = request.GET.get('search_query')
    toy_list = Toy.objects.filter(Q(name__icontains=query))
    
    return render(request, 'all/search_results.html', {'toy_list': toy_list, 'query': query})

def sortbypriceasc(request):
    toy_list = Toy.objects.all().order_by('price')
    logger.info('Toys sorted by price in ascending order.')
    return render(request, 'all/catalogue.html', {'toy_list': toy_list})

def sortbypricedesc(request):
    toy_list = Toy.objects.all().order_by('-price')
    logger.info('Toys sorted by price in descending order.')
    return render(request, 'all/catalogue.html', {'toy_list': toy_list})

def sortbycategory(request):
    toy_list = Toy.objects.all().order_by('type')
    logger.info('Toys sorted by category.')
    return render(request, 'all/catalogue.html', {'toy_list': toy_list})

@customer_required
def buy(request, id):
    if request.method == 'POST':
        toy = Toy.objects.get(id=id)
        form = SaleForm(request.POST)
        customer = CustomerProfile.objects.get(customer=request.user)
        if form.is_valid():
            sale = Sale(customer=customer, toy=toy, quantity=form.cleaned_data['quantity'], completion_date=form.cleaned_data['completion_date'], promo_code=form.cleaned_data['promo_code'])
            sale.save()
            logger.info('Purchase made by customer {}'.format(request.user.username))
            return redirect('home')  # исправленная строка
        else:
            return HttpResponseBadRequest("Form data is invalid. Please check your input.")
    else:
        toy = Toy.objects.get(id=id)
        form = SaleForm()
        return render(request, 'buying/buy.html', {'toy': toy, 'form': form})

def promocode(request):
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    dog_data = response.json()

    dog_image_url = dog_data.get('message', '')

    response_1 = requests.get('https://dog.ceo/api/breeds/image/random')
    dog_data_1 = response_1.json()

    dog_image_url_1 = dog_data_1.get('message', '')

    code_list = PromoCode.objects.all()
    type_list = ToyType.objects.all()
    logger.info("Promocode page accessed")
    return render(request, 'all/promocode.html', {'code_list': code_list, 'type_list': type_list, 'dog_image': dog_image_url, 'dog_image_1': dog_image_url_1})

def jobs(request):
    job_list = Job.objects.all()
    logger.info("Job page accessed")
    return render(request, 'all/jobs.html', {'job_list': job_list})

@staff_required
def clientinfo(request):
    customer_list = CustomerProfile.objects.all()
    logger.info("Client info page accessed")
    return render(request, 'staff/clientinfo.html', {'customer_list': customer_list})

@staff_required
def salesinfo(request):
    sale_list = Sale.objects.all()
    logger.info("Sales info page accessed")
    return render(request, 'staff/salesinfo.html', {'sale_list': sale_list})

@customer_required
def save_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, toys=Toy.objects.all(), initial={'customer': request.user})
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.customer = request.user.customerprofile
            feedback.save()
            logger.info('Feedback saved by customer {}'.format(request.user.username))
            return redirect('home')
    else:
        form = FeedbackForm(toys=Toy.objects.all(), initial={'customer': request.user})
    
    return render(request, 'customer/feedback.html', {'form': form})

def feedback(request):
    feedback_list = Feedback.objects.all()
    logger.info("Feedback page accessed")
    return render(request, 'all/feedbackinfo.html', {'feedback_list': feedback_list})

@superuser_required
def citygrouped(request):
    customers_by_city = {}
    customers = CustomerProfile.objects.all()
    
    for customer in customers:
        city = customer.city
        if city not in customers_by_city:
            customers_by_city[city] = []
        customers_by_city[city].append(customer)
    logger.info('City grouped page accessed.')
    return render(request, 'admin/citygrouped.html', {'customers_by_city': customers_by_city})

@customer_required
def pickuplist(request):
    point_list = PickUpPoints.objects.all()
    logger.info('Pickup points list page accessed.')
    return render(request, 'customer/pickuppoints.html', {'points_list': point_list})

@superuser_required
def base_stat(request):
    customer_list = CustomerProfile.objects.all().order_by('name')

    total = Sale.objects.all().values_list('price', flat=True)

    average_sale = mean(total)
    median_sale = median(total)
    mode_sale = mode(total)

    average_sale = round(average_sale, 2)
    median_sale = round(median_sale, 2)
    mode_sale = round(mode_sale, 2)

    popular_toy = Sale.objects.values('toy__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity').first()
    unpopular_toy = Sale.objects.values('toy__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity').last()
    logger.info('Base statistics page accessed.')

    return render(request, 'admin/basestat.html', {'customer_list': customer_list, 'av': average_sale, 'median': median_sale, 'mode': mode_sale, 'popular_toy': popular_toy, 'unpopular_toy': unpopular_toy})


@superuser_required
def analysis(request):
    monthly_sales = Sale.objects.annotate(month=TruncMonth('order_date')).values('month', 'toy__name').annotate(total_sales=Sum('quantity'))
    yearly_income = sum(Sale.objects.all().values_list('price', flat=True))

    image_monthly = montlyvol()
    client_sales = clientamoutofsales()
    client_spent = customerspent()
    linear_trend = linear_trend_plot()
    predict_trend = predict()
    logger.info('Analysis page accessed by superuser.')

    return render(request, 'admin/analysis.html', {'monthly_sales': monthly_sales, 'yearly_income': yearly_income, 'image': image_monthly, 'client_image': client_sales, 'client_spent': client_spent, 'linear_trend': linear_trend, 'predict': predict_trend})