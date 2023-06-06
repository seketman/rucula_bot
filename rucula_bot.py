# Setup
# 1. Install Python 3.11.3
# 2. Install pip
# 3. Install Selenium: pip3 install selenium
# 4. Install webdriver-manager: pip3 install webdriver-manager
# 5. Install requests: pip3 install requests
#
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from ambito import get_ambito_values
from database import get_connection, get_subscribers, update_subscriber_notification
from whatsapp import send_message, send_messages

# ++
# Setup
app_name = "Rúcula Bot"
whatsapp_web_url = 'https://web.whatsapp.com/'
admin_accounts = [
    "Diego Demarziani"
]
# --

def subscriber_should_be_notified(notification_gap, old_value, new_value):
    return not(old_value - notification_gap < new_value < old_value + notification_gap)

def notify_subscriber(driver, suscriber_id, old_sell_value, buy_value, new_sell_value):
    variation = 'subió' if old_sell_value < new_sell_value else 'bajó'
    return send_message(driver, suscriber_id, 'El blue %s - Compra $%d, Venta $%d' % (variation, buy_value, new_sell_value))

# Inicializar el navegador web
with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    # Abrir WhatsApp Web
    driver.get(whatsapp_web_url)

    # Esperar a que el usuario escanee el código QR
    input('Escanea el código QR y presiona Enter para continuar... ')
    send_messages(driver, admin_accounts, '%s se inició correctamente' % app_name)

    # Get database connection
    connection = get_connection()

    while True:
        time.sleep(90)
        response = get_ambito_values()
        if response.status_code != 200:
            send_messages(driver, admin_accounts, 'Error %s al obtener los datos' % response.status_code)
            continue

        data = response.json()
        print("%s - Compra: %s - Venta: %s" % (data['fecha'], data['compra'], data['venta']))

        new_sell_value = int(data['venta'].split(',')[0])
        buy_value = int(data['compra'].split(',')[0])
        for subscriber in get_subscribers(connection):
            if subscriber['last_notified_value'] is None:
                # First dummy notification to initialize the value
                update_subscriber_notification(connection, subscriber['id'], new_sell_value)
            
            elif subscriber_should_be_notified(subscriber['gap'], subscriber['last_notified_value'], new_sell_value):
                if notify_subscriber(driver, subscriber['id'], subscriber['last_notified_value'], buy_value, new_sell_value):
                    update_subscriber_notification(connection, subscriber['id'], new_sell_value)
