import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
USERNAME = os.getenv("TWITTER_USERNAME")
EMAIL = os.getenv("TWITTER_EMAIL")
PASSWORD = os.getenv("TWITTER_PASSWORD")
TWEET_TEXT = os.getenv("TWEET_TEXT")

# === Set up Chrome ===
def create_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(options=options)

# === Login Function ===
def login(driver):
    driver.get("https://twitter.com/login")
    wait = WebDriverWait(driver, 15)

    # Step 1: Enter username/email
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "text")))
    username_input.send_keys(EMAIL)
    username_input.send_keys(Keys.RETURN)
    time.sleep(2)

    # step 1.1: Enter username/email
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "text")))
    username_input.send_keys(USERNAME)
    username_input.send_keys(Keys.RETURN)
    time.sleep(2)

    # Step 2: Enter password
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

    # Wait for homepage
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='/home']")))
    print("✅ Logged in successfully.")

# === Tweet Function ===
def post_tweet(driver, text):
    wait = WebDriverWait(driver, 15)

    try:
        tweet_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetTextarea_0']")))
        tweet_box.click()
        tweet_box.send_keys(text)
        time.sleep(1)

        tweet_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='tweetButtonInline']")))
        tweet_button.click()
        print("✅ Tweet posted!")

    except Exception as e:
        print(f"❌ Failed to post tweet: {e}")

# === Main Script ===
def main():
    if not USERNAME or not PASSWORD or not TWEET_TEXT:
        print("❌ Missing .env configuration. Check TWITTER_USERNAME, TWITTER_PASSWORD, TWEET_TEXT.")
        return

    driver = create_driver(headless=False)
    try:
        login(driver)
        time.sleep(5)
        post_tweet(driver, TWEET_TEXT)
    except Exception as e:
        import traceback
        print("❌ Error during bot execution:")
        traceback.print_exc()
    finally:
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    main()
