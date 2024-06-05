import base64
from collections import Counter, defaultdict
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import io
import urllib 
from django.db.models.functions import TruncMonth
import pandas as pd
from .models import Sale
from django.db.models import Count, Sum
import matplotlib.dates as mdates

def montlyvol():
    monthly_sales = Sale.objects.annotate(month=TruncMonth('order_date')).values('month', 'toy__name').annotate(total_sales=Sum('quantity'))
    
    plt.figure(figsize=(10, 6))
    for sale in monthly_sales:
        plt.bar(sale['toy__name'], sale['total_sales'], color='teal')
    plt.xlabel('Игрушка')
    plt.ylabel('Объем продаж')
    plt.title('Ежемесячный объем продаж игрушек за текущий месяц')
    plt.xticks()
    
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    return url

def clientamoutofsales():
    sales = Sale.objects.all()
    customer_orders = Counter([sale.customer for sale in sales])
    customers = list(customer_orders.keys())
    orders = list(customer_orders.values())
    
    customer_indices = range(len(customers))  # Используем индексы вместо объектов клиентов
    plt.figure(figsize=(12, 6))
    plt.bar(customer_indices, orders, color='aquamarine')
    plt.xlabel('Клиенты')
    plt.ylabel('Количество заказов')
    plt.title('Количество заказов для каждого клиента')
    plt.xticks(customer_indices, customers)  # Устанавливаем метки оси X
    
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    return url

def customerspent():
    sales = Sale.objects.all()
    customer_total_spent = defaultdict(int) 
    
    for sale in sales:
        customer_total_spent[sale.customer] += sale.price

    customers = list(customer_total_spent.keys())
    total_spent = list(customer_total_spent.values())

    customer_indices = range(len(customers))

    plt.figure(figsize=(12, 6))
    bars = plt.bar(customer_indices, total_spent, color='deepskyblue')
    plt.xlabel('Клиенты')
    plt.ylabel('Сумма потраченная в магазине')
    plt.title('Сумма потраченная каждым клиентом')
    plt.xticks(customer_indices, customers)

    for bar, value in zip(bars, total_spent):
        plt.text(bar.get_x() + bar.get_width() / 2, value, str(value), ha='center', va='bottom')

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    return url

def linear_trend_plot():
    sales = Sale.objects.all()
    
    # Преобразование данных о продажах во временной ряд
    sales_data = pd.DataFrame(list(sales.values('order_date', 'price')))
    sales_data['order_date'] = pd.to_datetime(sales_data['order_date'])
    
    x = sales_data['order_date']  # Используем даты как ось X
    y = sales_data['price'].astype(float)  # Преобразуем значения продаж в тип float
    
    # Вычисление коэффициентов a и b уравнения линейного тренда
    x_serial = mdates.date2num(x)  # Преобразуем даты в серию чисел
    b = (np.mean(x_serial * y) - np.mean(x_serial) * np.mean(y)) / (np.mean(x_serial**2) - np.mean(x_serial)**2)
    a = np.mean(y) - b * np.mean(x_serial)
    
    # Построение линейного тренда
    linear_trend = a + b * x_serial
    
    # Построение графика с данными и линейным трендом
    plt.figure(figsize=(12, 6))
    plt.scatter(x, y, label='Данные о продажах')
    plt.plot(x, linear_trend, color='red', label='Линейный тренд')
    plt.xlabel('Дата')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))  # Форматирование даты на оси X
    plt.ylabel('Сумма продаж')
    plt.title('Линейный тренд продаж')
    plt.legend()
    
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    return url


def predict():
    sales = Sale.objects.all().order_by('order_date')

    # Создаем DataFrame с данными о продажах
    sales_data = pd.DataFrame(list(sales.values('order_date', 'price')))
    sales_data['order_date'] = pd.to_datetime(sales_data['order_date'])
    sales_data.set_index('order_date', inplace=True)

    # Рассчитываем скользящее среднее за определенный период (например, 3 месяца)
    sales_data['moving_average'] = sales_data['price'].rolling(window=3).mean()

    # Построение графика с данными о продажах и прогнозом
    plt.figure(figsize=(12, 6))
    plt.plot(sales_data['price'], label='Продажи')
    plt.plot(sales_data['moving_average'], label='Прогноз продаж (скользящее среднее)')
    plt.xlabel('Дата')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))  # Форматирование даты на оси X
    plt.ylabel('Сумма продаж')
    plt.title('Прогноз продаж с использованием скользящего среднего')
    plt.legend()

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    return url
