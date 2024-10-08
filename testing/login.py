from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize WebDriver
driver = webdriver.Chrome()  # or webdriver.Firefox()

# Define credentials (same as used in signup.py)
new_username = "user"
new_password = "pass1234"


def print_result(test_case, result):
    print(f"{test_case}: {'PASSED' if result else 'FAILED'}")


def test_login_page():
    # Load the login.html page
    driver.get("http://127.0.0.1:5500/public/login.html")  # Adjust path as necessary
    time.sleep(2)  # Wait for the page to load

    # Check the title of the page
    result = "Login" in driver.title
    print_result("Check page title", result)

    # Verify presence of the login form
    login_form = driver.find_element(By.ID, "loginForm")
    result = login_form.is_displayed()
    print_result("Login form presence", result)

    # Verify form fields are present
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    result = username_input.is_displayed() and password_input.is_displayed()
    print_result("Form fields presence", result)

    # Test a successful login (using credentials from signup)
    username_input.send_keys(new_username)  # Use the username from signup
    password_input.send_keys(new_password)  # Use the password from signup
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(2)  # Wait for the page to load after login

    # Check if redirected to the dashboard
    result = "dashboard.html" in driver.current_url
    print_result("Successful login redirection", result)

    # Check for token in localStorage (this needs to be done through JavaScript)
    token = driver.execute_script("return localStorage.getItem('token');")
    result = token is not None
    print_result("Token set in localStorage", result)

    # Test a failed login
    driver.get("http://127.0.0.1:5500/public/login.html")  # Reload the login page
    time.sleep(2)  # Wait for the page to load

    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    username_input.clear()
    password_input.clear()
    username_input.send_keys("invalid_username")  # Invalid username
    password_input.send_keys("invalid_password")  # Invalid password
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(2)  # Wait for the error message to appear

    # Handle the alert
    alert = driver.switch_to.alert
    alert_text = alert.text
    result = alert_text is not None and "Invalid credentials" in alert_text
    print_result("Login with invalid credentials", result)
    alert.accept()  # Dismiss the alert

    # Test login with missing username
    driver.get("http://127.0.0.1:5500/public/login.html")
    time.sleep(2)
    password_input = driver.find_element(By.ID, "password")
    password_input.clear()
    password_input.send_keys(new_password)
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(2)

    # Handle the alert
    alert = driver.switch_to.alert
    alert_text = alert.text
    result = alert_text is not None and "Username is required" in alert_text
    print_result("Login with missing username", result)
    alert.accept()  # Dismiss the alert

    # Test login with missing password
    driver.get("http://127.0.0.1:5500/public/login.html")
    time.sleep(2)
    username_input = driver.find_element(By.ID, "username")
    username_input.clear()
    username_input.send_keys(new_username)
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(2)

    # Handle the alert
    alert = driver.switch_to.alert
    alert_text = alert.text
    result = alert_text is not None and "Password is required" in alert_text
    print_result("Login with missing password", result)
    alert.accept()  # Dismiss the alert

    print("Login page test completed!")


if __name__ == "__main__":
    try:
        test_login_page()
    finally:
        driver.quit()  # Close the browser
