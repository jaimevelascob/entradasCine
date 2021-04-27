# Librerías
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
#mover mouse
import pyautogui
import random

images = ""
contador = 0
driver = ""
otroContador = 0
link = 'https://www.pillalas.com/pase/769517/'
# Inicializamos el navegador

def conectarWeb():
    global driver
    options = Options()
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome('/usr/bin/chromedriver',options=options)
    driver.maximize_window()
    
    time.sleep(1)
    driver.get(link)

    ###quitar cookie
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                          '/html/body/div/p[2]/a')))\
        .click()
    return driver

#mirar butacas disponibles
def obtenerImagenes():
    global images
    html_page = requests.get(link)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    warning = soup.find('div', class_="sala")
    images = warning.findAll('img')
    return images 

def butacasDisponibles(images):
    global contador
    contador = 1
    for image in images:
        if (image.attrs['src'] == '/static/images/butacas/normal.png'):
            contador += 1
    return contador

def entradas(images):
    i = 1
    for image in images:
        if (image.attrs['src'] == '/static/images/butacas/normal.png' and i <= 6 and contador >= 14):
            WebDriverWait(driver, 5)\
                .until(EC.element_to_be_clickable((By.ID,
                                              image.attrs['id'])))\
                .click()
            time.sleep(0.5)
            i += 1
        elif (image.attrs['src'] == '/static/images/butacas/normal.png' and i <= 6 and contador < 14):
            WebDriverWait(driver, 5)\
                .until(EC.element_to_be_clickable((By.ID,
                                              image.attrs['id'])))\
                .click()
            time.sleep(0.5)
            time.sleep(3)
            driver.back()
            
    # clickar boton comprar
    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                          '/html/body/article/div/div/main/div[3]/div[6]/a')))\
        .click()

    # si cambió de url
    if (driver.current_url == 'https://www.pillalas.com/pase/769521/3574175/descuentos/'):
        time.sleep(3)
        driver.back()

    # si saltó el span
    else:
        WebDriverWait(driver, 5)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                            '/html/body/div[5]/div/div/div[1]/button/span')))\
            .click()
        reset()
        
def reset():
    global otroContador
    time.sleep(1)
    driver.close()
    otroContador = 0
    pyautogui.moveTo(random.uniform(100, 200), random.uniform(200, 300))
    time.sleep(120)

if __name__ == '__main__':
    while True: 
        print(otroContador)
        if otroContador == 0:
            conectarWeb()
        obtenerImagenes()
        butacasDisponibles(images)
        print(contador)
        otroContador += 1
        if contador >= 14:
            entradas(images)
        else:
            otroContador = 0
            reset()
                                                