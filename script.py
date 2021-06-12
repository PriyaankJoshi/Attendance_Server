from selenium import webdriver
from datetime import datetime, timedelta
from time import sleep
import os


def sign_in(username, password):
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('loginbtn').click()


def log_out():
    driver.find_element_by_id("action-menu-toggle-1").click()
    driver.find_element_by_id("actionmenuaction-6").click()


def fetch_attendance_links():
    a_tags = driver.find_elements_by_tag_name('a')

    for i in a_tags:
        if 'attendance' in i.get_attribute("href").lower():
            attendance_links.append(i.get_attribute("href"))


def mark_attendance():
    try:
        driver.find_element_by_link_text('Submit attendance').click()
        driver.find_element_by_xpath("//span[.='Present']").click()
        driver.find_element_by_id('id_submitbutton').click()
        return True
    except:
        return False


def fetch_course():
    course = driver.find_element_by_xpath('//*[@id="page-navbar"]/nav/ol/li[3]/a').text
    return course


def curr_timestamp():
    curr_datetime = datetime.now()
    curr_timestamp = (curr_datetime+ist_delta).strftime("%Y-%m-%d %H:%M:%S")
    return curr_timestamp


def curr_day():
    curr_datetime = datetime.now()
    curr_day = (curr_datetime+ist_delta).weekday()
    return curr_day


def curr_time():
    curr_datetime = datetime.now()
    curr_time = (curr_datetime+ist_delta).strftime("%H:%M")
    return curr_time


def log(timestamp, thing, status):
    return (f'{timestamp}  {thing} : {status}\n')


if __name__ == '__main__':
    attendance_links = []
    username = "200111096"
    password = "Moodle@123"
    link = "http://45.116.207.81/moodle/calendar/view.php?view=day"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')

    ist_delta = timedelta(hours=5, minutes=30)

    times = ["09:10", "10:10", "11:10", "12:10", "13:10", "14:10", "15:10", "16:10"]

    print(log(curr_timestamp(), 'APP', 'START'))

    while True:
        if curr_day() != 6:
            if curr_time() in times:
                print(log(curr_timestamp(), 'SESSION', 'START'))

                driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), options=chrome_options)
                driver.get(link)

                sign_in(username, password)
                fetch_attendance_links()

                for attendance_link in attendance_links:
                    driver.get(attendance_link)
                    if mark_attendance():
                        print(log(curr_timestamp(), fetch_course(), 'MARKED'))

                log_out()
                driver.close()
                print(log(curr_timestamp(), 'SESSION', 'ENDED'))
                sleep(60)

    print(log(curr_timestamp(), 'APP', 'ENDED'))
