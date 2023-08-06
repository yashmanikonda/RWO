from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
driver = webdriver.Chrome()

def get_login_credentials():
    login_element_input = input("Enter your GitHub username: ")
    password_element_input = input("Enter your GitHub password: ")
    return login_element_input, password_element_input

def get_repository_links():
    # Wait for the repositories list to load
    repositories_list_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'user-repositories-list'))
    )

    # Find all anchor elements (links) within the div
    links = repositories_list_div.find_elements(By.TAG_NAME, 'a')

    # Extract and return the repository URLs
    return [link.get_attribute('href') for link in links]

if __name__ == "__main__":
    authenticated = False
    while not authenticated:
        login_element_input, password_element_input = get_login_credentials()
        driver.maximize_window()
        driver.get('https://github.com/login')

        login_element = driver.find_element(By.ID, 'login_field')
        login_element.clear()
        login_element.send_keys(login_element_input)

        password_element = driver.find_element(By.ID, 'password')
        password_element.clear()
        password_element.send_keys(password_element_input)

        sign_in_button = driver.find_element(By.CLASS_NAME, 'js-sign-in-button')
        sign_in_button.click()

        try:
            error_message = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'js-flash-alert'))
            )
            print("Incorrect username or password")

        except TimeoutException:
            authenticated = True

        except NoSuchElementException:
            authenticated = True

    profile_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'AppHeader-user'))
    )
    profile_button.click()

    repo_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//span[@data-view-component="true" and contains(@class, "ActionListItem-label") and contains(text(), "Your repositories")]'))
    )
    repo_button.click()

    while True:
        # Get the current list of repository links
        repository_urls = get_repository_links()

        # Check if there are repositories to delete
        if not repository_urls:
            break  # Exit the loop if no repositories are found

        # Iterate through the repository URLs
        for repo_url in repository_urls:
            # Open the repository
            driver.get(repo_url)

            settings_button = driver.find_element(By.ID, 'settings-tab')
            settings_button.click()

            delete_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f'//span[@class="Button-label" and contains(text(), "Delete this repository")]'))
            )

            while not delete_button.is_displayed():
                driver.execute_script("window.scrollBy(0,5000);")
            delete_button.click()

            delete_button2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            f'//span[@class="Button-label" and contains(text(), "I want to delete this repository")]'))
            )
            delete_button2.click()

            delete_button3 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            '//span[@class="Button-label" and contains(text(), "I have read and understand these effects")]'))
            )
            delete_button3.click()

            final_delete_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="verification_field"]'))
            )

            # Extract the repository name and type it in the box below
            repository_name = driver.find_element(By.XPATH, '//label[contains(text(), "To confirm, type")]').text
            repository_name = repository_name.replace('To confirm, type "', '').replace('" in the box below', '')
            final_delete_element.send_keys(repository_name)

            final_delete_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'repo-delete-proceed-button'))
            )
            final_delete_button.click()

            driver.refresh()

    print("All repositories deleted.")

    driver.quit()
