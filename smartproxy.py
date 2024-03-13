# IMPORTS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import re

#DEFINE CONSTANTS

EMAIL_DF_PATH = "emails.csv"

def create_driver():
    
    #CREATES A DRIVER
    
    options = Options()
    options.add_argument("--incognito")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_new_email():
    
    # GETS A NEW 24H EMAIL AND STORES IT IN THE EMAILS AND RETURNS THE NEW EMAIL
    
    driver.get('https://24hour.email/en')
    get_mail_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "btn-backtoapp"))
    )
    get_mail_btn.click()

    current_mail = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "current-id"))
        )

    email = current_mail.get_attribute("value")
    
    df = pd.read_csv(EMAIL_DF_PATH, sep=";", index_col=0)
    
    new_df = pd.DataFrame([email], columns=["email"])
    
    df = pd.concat([df, new_df], ignore_index=True)
    
    df.to_csv(EMAIL_DF_PATH, sep=";")
    
    return email

def get_verification_site(email):
    driver.get(f"https://24hour.email")
    time.sleep(5)
    driver.get(f"https://24hour.email/mailbox/{email}")
    refresh_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@action='refresh']"))
    )
    time.sleep(random.random())
    refresh_btn.click()
    first_msg = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='mail-item']//div[@class='message']"))
    )
    time.sleep(random.random())
    
    emails_msgs = driver.find_elements(By.XPATH, "//div[@class='mail-item']//div[@class='message']")

    for email in  emails_msgs:
        if "http://url6350.smartproxy.com" in email.text:
            email.click()
            time.sleep(5)
            continue
        
    email_text = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "content"))
    )
    pattern = r"https://dashboard\.smartproxy\.com/verify/[a-zA-Z0-9]+/"
    match = re.search(pattern, email_text.text)
    link = ""
    if match:
        link = match.group()

    return link

def create_smartproxy_account(email, password):
    driver.execute_script("window.open('');")
    time.sleep(2)
    smart_proxy_window = driver.window_handles[1]
    driver.switch_to.window(smart_proxy_window)
    driver.get("https://dashboard.smartproxy.com/register")
    mail_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "newEmail"))
    )
    time.sleep(1)
    mail_input.send_keys(email)
    password_input = driver.find_element(By.XPATH, "//input[@id='newPassword']")
    password_input.send_keys(password)
    accept_terms = driver.find_element(By.ID, "acceptTerms")

    try:
        driver.execute_script("arguments[0].click()", accept_terms)
    except:
        return "Failed to click the accept terms box."
    
    time.sleep(10)
    
    submit_btn = driver.find_element(By.XPATH, "//button[@data-testid='continueRegistration']")
    submit_btn.click()
    
    case_description = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, "//div[@data-testid='useCase_Market Intelligence']"))
    )
    time.sleep(random.random())
    case_description.click()
    
    solution_use = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, "//div[@data-testid='integrateToCode']"))
    )
    time.sleep(random.random())

    solution_use.click()
    
    time.sleep(2)
    
    #Return to mail tab and press refresh
    driver.switch_to.window(driver.window_handles[0])

    time.sleep(3)
    
    verification_link = get_verification_site(email)
    driver.get(verification_link)
    time.sleep(5)
    driver.get("https://dashboard.smartproxy.com/social-media/pricing")
    
    free_plan = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@data-testid, 'regularPlan')]"))
        )
    time.sleep(random.random())
    free_plan.click()

    checkout_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,"//button[@data-testid='proceedToCheckout']"))
    )
    time.sleep(random.random())
    checkout_btn.click()
    time.sleep(5)
    request_btn = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//button/span[text()='Request']"))
    )
    request_btn.click()
    time.sleep(2)
    
    code = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//code[@class='language-bash']")))
    code_pattern = r'Basic \w+='
    match = re.search(code_pattern, code.text)

    if match:
        request_code = match.group()

    return request_code

def store_code(code):
    df = pd.read_csv("codes.csv", index_col=0, sep=";")
    new_df = pd.DataFrame([code], columns=["codes"])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv("codes.csv", sep=";")

if __name__ == "__main__":
    for _ in range(10):
        driver = create_driver()
        email = get_new_email()
        request_code = create_smartproxy_account(email, "Hgjm1234!jweoifaj")
        print(request_code)
        store_code(request_code)
        driver.quit()
    