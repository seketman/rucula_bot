from selenium.webdriver.common.by import By
import time

def get_contacts(driver):
    return driver.find_elements(By.XPATH, '//span[@title]')

def get_contact(driver, contact):
    return driver.find_element(By.XPATH, '//span[@title="%s"]' % contact)

def get_message_field(driver):
    return driver.find_element(By.XPATH, '//div[@contenteditable="true"][@title="Type a message"]')

def get_send_button(driver):
    return driver.find_element(By.XPATH, '//span[@data-testid="send"]')

def print_contacts(driver):
    contactos = get_contacts(driver)
    for contacto in contactos:
        print(contacto.text)

def send_message(driver, target, message_text):
    try:
        # Buscar el contacto al que deseas enviar un mensaje
        contact_button = get_contact(driver, target)
        contact_button.click()

        # Esperar a que la ventana de chat se abra
        time.sleep(2)

        # Escribir el mensaje que deseas enviar
        message_field = get_message_field(driver)
        message_field.send_keys(message_text)

        # Esperar a que el boton de send aparezca
        time.sleep(1)

        # Enviar el mensaje
        send_button = get_send_button(driver)
        send_button.click()
        time.sleep(1)
    except:
        print('+- No se pudo enviar el mensaje "%s" a "%s"' % (message_text, target))
        return False
    else:
        print('+- Se envió el mensaje "%s" a "%s"' % (message_text, target))
        return True

def send_messages(driver, targets, message_text):
    for target in targets:
        send_message(driver, target, message_text)
