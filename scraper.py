from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
# import random
import random

import subprocess

def rotate_ip():
    command = "protonvpn-cli c -r"
    command = command.split()
    # run the above command and then print the output
    output = subprocess.check_output(command)
    print(output)

def get_idea_links(driver):
    # gets all links that start with "/idea/"
    idea_links = driver.find_elements(By.XPATH, "//a[starts-with(@href, '/idea/')]")
    # sleep(1)
    # idea_links = [link.get_attribute('href') for link in idea_links]
    new_links = []
    for elem in idea_links:
        link = elem.get_attribute("href")
        new_links.append(link)
    return new_links


def save_links(idea_links, filename):
    # save the idea links to a file
    with open(filename, 'w') as f:
        for link in idea_links:
            f.write(link + '\n')

def load_more_ideas(driver):
    # clicks the load more ideas button
    load_more_button = driver.find_element(By.XPATH, "//a[@class='load-more load_more_ideas']")
    load_more_button.click()

def main():

    date_val = '02/27/2023'

    # Create a new instance of the Chrome driver
    # chrome_options = Options()
    #chrome_options.add_argument("--disable-extensions")
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--no-sandbox") # linux only
    # chrome_options.add_argument("--headless")
    # options = Options()
    # options.add_argument(f'user-agent={UserAgent().random}')
    driver = webdriver.Chrome(
        # options=options
    )

    # go to the investorsclub ideas page
    driver.implicitly_wait(10)
    driver.get("https://www.valueinvestorsclub.com/ideas/")


    # click the date filter button
    # This is fragile. It assumes the date filter will remain the sixth element.
    date_filter_button = driver.find_elements(By.ID, "dropdownMenu1")[6]
    date_filter_button.click()
    sleep(.25)
    # enter text into the dash goto date input equal to the date_val
    goto_date_input = driver.find_element(By.ID, "dash_goto_date")
    # clear the existing input in the form.
    goto_date_input.clear()
    goto_date_input.send_keys(date_val)
    sleep(.25)
    # click the go to date button
    goto_date_button = driver.find_element(By.ID, "dash_goto_date_btn")
    goto_date_button.click()
    sleep(.25)

    # get all the idea links
    idea_links = []
    count = 0
    sleep_max = 15
    last_rotated = 0
    max_count = 200
    while count < max_count:
        load_more_ideas(driver)
        # choose a random number of seconds from 1 to 10 to sleep
        sleep_val = random.randint(1, sleep_max)
        sleep(sleep_val)
        if count % 10 == 0:
            try:
                idea_links = get_idea_links(driver)
            except Exception as e:
                print("Error getting idea links: " + str(e))
                rotate_ip()
                last_rotated = count
        if count - last_rotated % 60 == 0:
            rotate_ip()
            last_rotated = count
        if count % 20 == 0:
            date_val = date_val.replace('/', '-')
            save_links(idea_links, f'idea_links-{date_val}.txt')
            print("Count is at: " + str(count) + " of " + str(max_count))
            print(count)
        count += 1
    idea_links = get_idea_links(driver)
    print(len(idea_links))
    print(idea_links[-1])
    # convert slashes to dashes in the date for the filename
    date_val = date_val.replace('/', '-')
    save_links(idea_links, f'idea_links-{date_val}.txt')



if __name__ == '__main__':
    main()

