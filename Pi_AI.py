from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pathlib

ScriptDir = pathlib.Path().absolute()
url = "https://pi.ai/talk"
chrome_option = Options()
user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"
chrome_option.add_argument(f"user-agent={user_agent}")
chrome_option.add_argument('--profile-directory-Default')
# chrome_option.add_argument("--headless=new")
chrome_option.add_argument(f'user-data_dir={ScriptDir}\\chromedata')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_option) # Fix is here
driver.maximize_window()
driver.get(url=url)
sleep(100)
