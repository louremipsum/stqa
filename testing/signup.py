from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize WebDriver
driver = webdriver.Chrome()  # or webdriver.Firefox()

# Define credentials
new_username = "user"
new_password = "pass1234"


def print_result(test_case, result):
    print(f"{test_case}: {'PASSED' if result else 'FAILED'}")


def test_signup_page():
    # Load the signup.html page
    driver.get("http://127.0.0.1:5500/public/signup.html")  # Adjust path as necessary
    time.sleep(2)  # Wait for the page to load

    # Check the title of the page
    result = "Sign Up" in driver.title
    print_result("Check page title", result)

    # Verify presence of the sign-up form
    signup_form = driver.find_element(By.ID, "signupForm")
    result = signup_form.is_displayed()
    print_result("Sign up form presence", result)

    # Verify form fields are present
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    role_select = driver.find_element(By.ID, "role")
    result = (
        username_input.is_displayed()
        and password_input.is_displayed()
        and role_select.is_displayed()
    )
    print_result("Form fields presence", result)

    # Test a successful sign-up
    username_input.send_keys(new_username)
    password_input.send_keys(new_password)
    role_select.send_keys("User")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(2)

    # Check for success alert
    alert = driver.switch_to.alert
    result = alert is not None and "Account created successfully" in alert.text
    print_result("Successful sign-up", result)
    alert.accept()

    # Check if redirected to the login page
    result = "login.html" in driver.current_url
    print_result("Redirection to login page", result)

    # Test sign-up with existing username
    driver.get("http://127.0.0.1:5500/public/signup.html")
    time.sleep(2)
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    role_select = driver.find_element(By.ID, "role")
    username_input.clear()
    password_input.clear()
    username_input.send_keys(new_username)
    password_input.send_keys("another_password")
    role_select.send_keys("User")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(2)

    # Check for error alert
    alert = driver.switch_to.alert
    result = alert is not None and "User already exists" in alert.text
    print_result("Sign-up with existing username", result)
    alert.accept()

    # Test sign-up with missing username
    driver.get("http://127.0.0.1:5500/public/signup.html")
    time.sleep(2)
    password_input = driver.find_element(By.ID, "password")
    role_select = driver.find_element(By.ID, "role")
    password_input.clear()
    password_input.send_keys(new_password)
    role_select.send_keys("User")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(2)

    # Check for error alert
    alert = driver.switch_to.alert
    result = alert is not None and "Username is required" in alert.text
    print_result("Sign-up with missing username", result)
    alert.accept()

    # Test sign-up with missing password
    driver.get("http://127.0.0.1:5500/public/signup.html")
    time.sleep(2)
    username_input = driver.find_element(By.ID, "username")
    role_select = driver.find_element(By.ID, "role")
    username_input.clear()
    username_input.send_keys(new_username + "2")
    role_select.send_keys("User")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(2)

    # Check for error alert
    alert = driver.switch_to.alert
    result = alert is not None and "Password is required" in alert.text
    print_result("Sign-up with missing password", result)
    alert.accept()

    # Test sign-up with missing role
    driver.get("http://127.0.0.1:5500/public/signup.html")
    time.sleep(2)
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    username_input.clear()
    password_input.clear()
    username_input.send_keys(new_username + "3")
    password_input.send_keys(new_password)
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(2)

    # Check for error alert
    alert = driver.switch_to.alert
    result = alert is not None and "Role is required" in alert.text
    print_result("Sign-up with missing role", result)
    alert.accept()

    print("Sign up page test completed!")


if __name__ == "__main__":
    try:
        test_signup_page()
    finally:
        driver.quit()  # Close the browser
