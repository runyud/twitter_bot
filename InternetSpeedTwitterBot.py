from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from config import PROMISED_DOWN, PROMISED_UP, TWITTER_EMAIL, TWITTER_USERNAME, TWITTER_PASSWORD


class InternetSpeedTwitterBot:

    def __init__(self):
        chrome_driver_path = ChromeDriverManager().install()  # Install the chromedriver executable local to your project

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)  # Keeps the browser open when the script finishes

        service = ChromeService(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        speed_test_url = "https://www.speedtest.net"
        down_xpath = '//span[@data-download-status-value>0.00]'
        up_xpath = '//span[@data-upload-status-value>0.00]'

        self.driver.get(speed_test_url)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".start-button a")))
        start_test_btn = self.driver.find_element(By.CSS_SELECTOR, ".start-button a")
        start_test_btn.click()

        WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.XPATH, up_xpath)))
        self.down = float(self.driver.find_element(By.XPATH, down_xpath).get_attribute("textContent"))
        self.up = float(self.driver.find_element(By.XPATH, up_xpath).get_attribute("textContent"))

    def tweet_at_provider(self):
        tweet = f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up " \
                f"when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up"
        twitter_url = "https://twitter.com/i/flow/login"
        tweet_area_xpath = '//div[@data-contents]'
        tweet_btn_xpath = '//div[@data-testid="tweetButtonInline"]'

        self.driver.get(twitter_url)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, 'text')))
        login = self.driver.find_element(By.NAME, 'text')
        login.send_keys(TWITTER_EMAIL)
        login.send_keys(Keys.ENTER)

        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, 'text')))
        except NoSuchElementException or TimeoutException:
            print("NoSuchElementException or TimeoutException")
            pass
        else:
            login = self.driver.find_element(By.NAME, 'text')
            login.send_keys(TWITTER_USERNAME)
            login.send_keys(Keys.ENTER)

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "password")))
        password = self.driver.find_element(By.NAME, "password")
        password.send_keys(TWITTER_PASSWORD)
        password.send_keys(Keys.ENTER)

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, tweet_area_xpath)))
        tweet_area = self.driver.find_element(By.XPATH, tweet_area_xpath)
        tweet_area.send_keys(tweet)

        tweet_button = self.driver.find_element(By.XPATH, tweet_btn_xpath)
        tweet_button.click()


