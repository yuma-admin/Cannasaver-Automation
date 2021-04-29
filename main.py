from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
import time 
import os
from datetime import date


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

driver = webdriver.Chrome(resource_path('./driver/chromedriver.exe'))

# driver.get("https://www.google.com")

# Default starting variables
# PATH = "D:\code\Yuma_Way\Cannasaver_Automation\driver\chromedriver.exe"
# driver = webdriver.Chrome(PATH)

userName = 'Rita'
password = 'theyuma1'
today = str(date.today())


# Go to the login webpage and login
driver.get("https://www.cannasaver.com/store-login")
search = driver.find_element_by_name("user[username]")
search.send_keys(userName)
search = driver.find_element_by_name("user[password]")
search.send_keys(password)
time.sleep(0.5)
logIn = driver.find_element_by_name('commit')
logIn.click()

try:
    # Wait until the site loads the next page
    wait = WebDriverWait(driver, 10)
    
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "logo"))
    )
    driver.find_element_by_xpath('//*[@id="DataTables_Table_0_length"]/label/select/option[4]').click()

    actions = ActionChains(driver)

    # Stores the ID of the main window that contains all the coupons 
    original_window = driver.current_window_handle

    time.sleep(1)

    # Generates a list of all coupon links that might need to be updated
    # elems = driver.find_elements_by_xpath("//a[@href]")
    # substring = '/my-coupons/couponpanel'
    coupon_links = []
    substring = '/edit'
    elements = driver.find_elements_by_css_selector("table.dataTable tr td div a")
    for element in elements:
        if element.get_attribute('href'):
            href = element.get_attribute('href')
            if substring in href:
                coupon_links.append(href)

    # remove any duplicate links
    coupon_links = list( dict.fromkeys(coupon_links) )

    # Then we loop though that list with the code below 
    for coupon in coupon_links:
        driver.get(coupon)
        wait.until(
            EC.presence_of_element_located((By.ID, "coupon_publish_start"))
        )
    # modifies the startign date field with todays date and then dismisses all the alerts
        time.sleep(1)
        new_date = driver.find_element_by_id('coupon_publish_start')
        new_date.clear()
        new_date.send_keys(today)
        new_date.send_keys(Keys.RETURN)
        driver.find_element_by_xpath('//*[@id="coupon_country"]/option[2]').click()
        time.sleep(.2)
        driver.find_element_by_name('commit').click()
        time.sleep(.4)
        checking_alerts = True 
        while checking_alerts:
            try:
                WebDriverWait(driver, 0.3).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
            except TimeoutException:
                checking_alerts = False 
        

finally:
    print('im done')
    driver.close()