import os
import time
import random
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

# === Predefined search keywords ===
SEARCH_KEYWORDS = [
    "Ecommerce",
    "Online Shopping",
    "Digital Marketing",
    "E-Commerce Trends",
    "Marketplace",
    "Online Retail",
    "E-Commerce Business",
    "Digital Commerce",
    "Online Business",
    "Retail E-Commerce",
    "uzakitu.com",
    "Uzakitu services",
    "Uzakitu platform"
]

# === Select a random keyword ===
SEARCH_KEYWORD = random.choice(SEARCH_KEYWORDS)

# === Set up Chrome ===
def create_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(options=options)

# === Login Function ===
def login(driver):
    driver.get("https://twitter.com/login")
    wait = WebDriverWait(driver, 20)

    # Step 1: Enter email or username
    input_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
    input_field.send_keys(EMAIL or USERNAME)
    input_field.send_keys(Keys.RETURN)
    time.sleep(2)

    # If Twitter asks for username after email
    if USERNAME and EMAIL:
        try:
            input_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
            input_field.send_keys(USERNAME)
            input_field.send_keys(Keys.RETURN)
            time.sleep(2)
        except:
            pass  # username step skipped

    # Step 2: Enter password
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

    # Wait until logged in (homepage)
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='/home']")))
    print("✅ Logged in successfully.")

# === Search Function ===
def search_keyword(driver, keyword):
    wait = WebDriverWait(driver, 15)
    
    print(f"\n🔍 Searching for keyword: {keyword}")
    search_url = f"https://twitter.com/search?q={keyword}&src=typed_query&f=live"
    print(f"🔍 URL: {search_url}")
    driver.get(search_url)
    
    # Wait for the page to load completely
    time.sleep(10)  # Increased wait time
    
    # Debug: Print current URL
    print(f"🔍 Current URL: {driver.current_url}")
    
    # Try multiple methods to find tweets
    try:
        print("🔍 Attempting to find tweets...")
        tweets = []
        
        # Try different selectors for tweets
        selectors = [
            "//article[@data-testid='tweet']",  # X.com
            "//div[@data-testid='tweet']",      # X.com alternative
            "//div[contains(@class, 'tweet')]"  # Legacy Twitter
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                if elements:
                    tweets = elements
                    print(f"✅ Found {len(tweets)} tweets using selector: {selector}")
                    break
            except Exception as e:
                print(f"❌ Failed with selector {selector}: {str(e)}")
        
        if not tweets:
            print("❌ No tweets found using any selector")
            return
            
        # Try to find reply buttons
        reply_buttons = []
        # Updated selectors for X.com
        button_selectors = [
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(@class, 'r-1wyyakw')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(@class, 'r-1wyyakw')][contains(@class, 'r-1udh08x')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(@class, 'r-1wyyakw')][contains(@class, 'r-1udh08x')][contains(@class, 'r-bcqeeo')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(@class, 'r-1wyyakw')][contains(@class, 'r-1udh08x')][contains(@class, 'r-bcqeeo')][contains(@class, 'r-qvutc0')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(@class, 'r-1wyyakw')][contains(@class, 'r-1udh08x')][contains(@class, 'r-bcqeeo')][contains(@class, 'r-qvutc0')][contains(@class, 'r-18u37iz')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(@class, 'r-1wyyakw')][contains(@class, 'r-1udh08x')][contains(@class, 'r-bcqeeo')][contains(@class, 'r-qvutc0')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(@class, 'r-1wyyakw')][contains(@class, 'r-1udh08x')][contains(@class, 'r-bcqeeo')][contains(@class, 'r-qvutc0')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(@class, 'r-1wyyakw')][contains(@class, 'r-1udh08x')][contains(@class, 'r-bcqeeo')][contains(@class, 'r-qvutc0')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(@class, 'r-13qz1uu')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(@class, 'r-1wyyakw')][contains(@class, 'r-1udh08x')][contains(@class, 'r-bcqeeo')][contains(@class, 'r-qvutc0')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-18u37iz')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(@class, 'r-1wyyakw')][contains(@class, 'r-1udh08x')][contains(@class, 'r-bcqeeo')][contains(@class, 'r-qvutc0')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(@class, 'r-1wyyakw')][contains(@class, 'r-1udh08x')][contains(@class, 'r-bcqeeo')][contains(@class, 'r-qvutc0')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(@class, 'r-1wyyakw')][contains(@class, 'r-1udh08x')][contains(@class, 'r-bcqeeo')][contains(@class, 'r-qvutc0')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(@class, 'r-13qz1uu')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(@class, 'r-1wyyakw')][contains(@class, 'r-1udh08x')][contains(@class, 'r-bcqeeo')][contains(@class, 'r-qvutc0')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-18u37iz')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(@class, 'r-1wyyakw')][contains(@class, 'r-1udh08x')][contains(@class, 'r-bcqeeo')][contains(@class, 'r-qvutc0')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(@class, 'r-1wyyakw')][contains(@class, 'r-1udh08x')][contains(@class, 'r-bcqeeo')][contains(@class, 'r-qvutc0')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(., 'Reply')]",
            "//div[contains(@class, 'css-1dbjc4n')][contains(@class, 'css-18t94o4')][contains(@class, 'r-1loqt21')][contains(@class, 'r-1otgn73')][contains(@class, 'r-1i6wzkk')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1fneopy')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-1adg3ll')][contains(@class, 'r-1wyyakw')][contains(@class, 'r-1udh08x')][contains(@class, 'r-bcqeeo')][contains(@class, 'r-qvutc0')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(@class, 'r-13qz1uu')][contains(@class, 'r-18u37iz')][contains(@class, 'r-16y2uox')][contains(@class, 'r-1jgb5lz')][contains(@class, 'r-13qz1uu')][contains(., 'Reply')]"]
        
        # Try different selectors
        selectors = [
            "//article[@data-testid='tweet']",
            "//div[@data-testid='tweet']",
            "//div[contains(@class, 'tweet')]"
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                if elements:
                    tweets = elements
                    print(f"✅ Found {len(tweets)} tweets using selector: {selector}")
                    break
            except Exception as e:
                print(f"❌ Failed with selector {selector}: {str(e)}")
        
        if not tweets:
            print("❌ No tweets found using any selector")
            return
            
        # Try to find reply buttons
        reply_buttons = []
        button_selectors = [
            "//div[contains(@data-testid, 'reply')]",
            "//div[contains(@aria-label, 'Reply')]",
            "//div[contains(@aria-label, 'Reply to')]"
        ]
        
        for selector in button_selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                if elements:
                    reply_buttons = elements
                    print(f"✅ Found {len(reply_buttons)} reply buttons using selector: {selector}")
                    break
            except Exception as e:
                print(f"❌ Failed with reply button selector {selector}: {str(e)}")
        
        if not reply_buttons:
            print("❌ No reply buttons found using any selector")
            return
            
        # Get the first tweet and its reply button
        try:
            first_tweet = tweets[0].text.strip()
            first_reply_button = reply_buttons[0]
            print(f"\n1. {first_tweet}")
            
            try:
                # Click the reply button
                first_reply_button.click()
                time.sleep(2)  # Wait for reply box to appear
                
                # Find the reply input box
                reply_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetTextarea_0']")))
                
                # Generate a comment specific to uzakitu.com
                if "uzakitu" in keyword.lower():
                    comment = "Uzakitu.com is a powerful platform for e-commerce and digital marketing solutions. They provide comprehensive tools for businesses to grow their online presence and manage their digital marketing efforts effectively. check it out! https://uzakitu.com"
                else:
                    comment = f"Interesting! I'm exploring {keyword} trends. Would love to hear more about your experience!"
                
                # Enter the comment
                reply_input.send_keys(comment)
                time.sleep(2)
                
                # Click the tweet button
                tweet_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='tweetButton']")))
                tweet_button.click()
                
                print("✅ Comment posted successfully!")
                
            except Exception as e:
                print(f"❌ Failed to post comment: {str(e)}")
                
        except Exception as e:
            print(f"❌ Failed to access tweet elements: {str(e)}")
            
    except Exception as e:
        print(f"❌ Error in search function: {str(e)}")
        # Find the reply input box
        reply_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetTextarea_0']")))
        
        # Generate a comment specific to uzakitu.com
        if "uzakitu" in keyword.lower():
            comment = "Uzakitu.com is a powerful platform for e-commerce and digital marketing solutions. They provide comprehensive tools for businesses to grow their online presence and manage their digital marketing efforts effectively. check it out! https://uzakitu.com"
        else:
            comment = f"Interesting! I'm exploring {keyword} trends. Would love to hear more about your experience!"
        
        # Enter the comment
        reply_input.send_keys(comment)
        time.sleep(2)
        
        # Click the tweet button
        tweet_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='tweetButton']")))
        tweet_button.click()
        
        print("✅ Comment posted successfully!")
        
    except Exception as e:
        print(f"❌ Failed to post comment: {str(e)}")

# === Main Script ===
def main():
    if not USERNAME or not PASSWORD:
        print("❌ Missing .env configuration. Check TWITTER_USERNAME, TWITTER_PASSWORD.")
        return

    driver = create_driver(headless=False)
    try:
        login(driver)
        time.sleep(5)
        
        # Search through all keywords in sequence
        print(f"🔍 Total keywords to search: {len(SEARCH_KEYWORDS)}")
        for idx, keyword in enumerate(SEARCH_KEYWORDS, 1):
            print(f"\n🔍 Searching keyword {idx}/{len(SEARCH_KEYWORDS)}: {keyword}")
            search_keyword(driver, keyword)
            time.sleep(5)  # Wait between searches

    except Exception as e:
        import traceback
        print("❌ Error during bot execution:")
        traceback.print_exc()
    finally:
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    main()