import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from ambito import get_ambito_values
from database import get_connection, get_suscribers, update_suscriber_notification
from whatsapp import send_message, send_messages

# ++
# Setup
app_name = "Rúcula Bot"
whatsapp_web_url = 'https://web.whatsapp.com/'
admin_accounts = [
    "Diego Demarziani"
]
# --

def suscriber_should_be_notified(notification_gap, old_value, new_value):
    return not(old_value - notification_gap < new_value < old_value + notification_gap)

def notify_suscriber(driver, suscriber_id, old_value, new_value):
    return send_message(driver, suscriber_id, 'El blue %s a $%d' % ('subió' if old_value < new_value else 'bajó', new_value))

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

        new_value = int(data['venta'].split(',')[0])
        for suscriber in get_suscribers(connection):
            if suscriber['last_notified_value'] is None:
                # First dummy notification to initialize the value
                update_suscriber_notification(connection, suscriber['id'], new_value)
            
            elif suscriber_should_be_notified(suscriber['gap'], suscriber['last_notified_value'], new_value):
                if notify_suscriber(driver, suscriber['id'], suscriber['last_notified_value'], new_value):
                    update_suscriber_notification(connection, suscriber['id'], new_value)
