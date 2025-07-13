from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# === CONFIGURATION ===
USERNAME = "uzakitu@gmail.com"
PASSWORD = "@Uzakitu2024!"
TWEET_TEXT = "This is an automated tweet using Selenium! 🚀"

# === SETUP CHROME OPTIONS ===
options = Options()
# Uncomment to run headless (no browser window)
# options.add_argument('--headless')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")

# === START CHROME DRIVER ===
driver = webdriver.Chrome(options=options)

try:
    # === OPEN TWITTER LOGIN PAGE ===
    driver.get("https://twitter.com/login")
    time.sleep(5)

    # === STEP 1: ENTER USERNAME ===
    username_input = driver.find_element(By.NAME, "text")
    username_input.send_keys(USERNAME)
    username_input.send_keys(Keys.RETURN)
    time.sleep(3)

    # === STEP 2: ENTER PASSWORD ===
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

    # === STEP 3: CLICK ON TWEET TEXT AREA ===
    tweet_box = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Tweet text']")
    tweet_box.click()
    time.sleep(2)
    tweet_box.send_keys(TWEET_TEXT)
    time.sleep(2)

    # === STEP 4: CLICK TWEET BUTTON ===
    tweet_button = driver.find_element(By.XPATH, "//div[@data-testid='tweetButtonInline']")
    tweet_button.click()
    time.sleep(3)

    print("✅ Tweet posted successfully!")

except Exception as e:
    print(f"❌ An error occurred: {e}")

finally:
    driver.quit()
