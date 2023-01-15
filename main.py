import time
from random import randint, choice
from selenium import webdriver
from selenium.webdriver.common.by import By

INSTAGRAM_TAGS_TO_SEARCH_START = "https://www.instagram.com/explore/tags/"
INSTAGRAM_TAGS_TO_SEARCH_END = "/?next=%2F"
TAGS_TO_LIKE = ["life", "bodybuilding", "NewYork", "Brasil", "Futebol", "Football", "Corinthians"]


URL_LOGIN = "https://www.instagram.com/accounts/login/"
URL_PAGES = ["https://www.instagram.com/gym_motivation_0.2/followers/",
             "https://www.instagram.com/bodydreamerbrazil/followers/",
             "https://www.instagram.com/gym_lovers._00/followers/",
             "https://www.instagram.com/corinthians/followers/",
             "https://www.instagram.com/90min_football/followers/"]
# URL_PAGE = choice(URL_PAGES)


USERNAME = "YOUR INSTAGRAM USERNAME"
PASSWORD = "YOUR INSTAGRAM PASSWORD"

driver = webdriver.Chrome()
driver.get(URL_LOGIN)

driver.implicitly_wait(5)
time.sleep(2)
user_text_field = driver.find_element(By.NAME, 'username')
user_text_field.send_keys(USERNAME)

password_text_field = driver.find_element(By.NAME, 'password')
password_text_field.send_keys(PASSWORD)

login_button = driver.find_elements(By.CSS_SELECTOR, "._acan")[1]
login_button.click()

driver.implicitly_wait(5)
time.sleep(5)


# Row down page:
# driver.execute_script("window.scrollBy(0,500)", "")


def start_following():
    """Follows people from the followers list of the pages of the URL_PAGES list."""
    driver.get(choice(URL_PAGES))
    driver.implicitly_wait(2)
    time.sleep(2)
    timeout = time.time() + 60 * 2
    while True:
        if time.time() > timeout:
            timeout = time.time() + 60 * 2
            url_page = choice(URL_PAGES)
            driver.get(url_page)
        buttons_div_followers = driver.find_elements(By.CSS_SELECTOR, "div div div div div div div div div div div div "
                                                                      "div div div div div div div div div div button")
        count = 0
        number_of_follows = randint(1, 10)
        for button in buttons_div_followers:
            if count >= number_of_follows:
                return
            try:
                if button.text == "Follow":
                    print(button.text)
                    button.click()
                    driver.implicitly_wait(randint(2, 10))
                    time.sleep(randint(2, 10))
                    count += 1
            except Exception as exp:
                h3_tags = driver.find_elements(By.CSS_SELECTOR, "h3")
                for element in h3_tags:
                    if element.text == "Try Again Later":
                        scroll_timeout_try_again = time.time() + 60 * 30
                        while time.time() < scroll_timeout_try_again:
                            scroll_page()
                        return
                print(exp)


def like_posts():
    """Likes posts from the list of Hashtags TAGS_TO_LIKE list."""
    try:
        final_url = INSTAGRAM_TAGS_TO_SEARCH_START + choice(TAGS_TO_LIKE) + INSTAGRAM_TAGS_TO_SEARCH_END
        driver.get(final_url)
        driver.implicitly_wait(5)
        time.sleep(3)
        posts_to_like = driver.find_elements(By.CSS_SELECTOR, "article div div div div a")
        index = randint(1, len(posts_to_like))
        posts_to_like[index].click()
        driver.implicitly_wait(2)
        time.sleep(1)
        like_button = driver.find_element(By.CSS_SELECTOR, "article div div div div section span button")
        like_button.click()
        driver.implicitly_wait(5)
        time.sleep(1)
    except Exception as exp:
        print(exp)


def scroll_page():
    driver.get("https://instagram.com")
    driver.implicitly_wait(3)
    time.sleep(3)
    scroll_timeout = time.time() + randint(60, 600)
    try:
        buttons = driver.find_elements(By.CSS_SELECTOR, "div div div div div div div div div div div div div div div"
                                                        " div div div button")
        for button in buttons:
            print(button.text)
            if button.text == "Not Now":
                button.click()
    except Exception as exp:
        print(exp)

    while time.time() < scroll_timeout:
        try:
            buttons = driver.find_elements(By.CSS_SELECTOR, "div section span button")
            for button in buttons:
                svg = button.find_element(By.CSS_SELECTOR, "div svg")
                if svg.get_attribute("aria-label") == "Like":
                    driver.implicitly_wait(randint(2, 10))
                    time.sleep(randint(2, 10))
                    button.click()
                    break
        except Exception as exp:
            print(exp)
        time.sleep(randint(0, 10))
        driver.execute_script(f"window.scrollBy({randint(0,1)},{randint(5, 9)}00)", "")


while True:
    scroll_page()
    number_of_likes = randint(0, 13)
    start_following()
    for n in range(number_of_likes):
        like_posts()
        driver.implicitly_wait(randint(0, 10))
        time.sleep(randint(0, 10))
