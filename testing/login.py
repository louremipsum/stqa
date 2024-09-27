from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize WebDriver
driver = webdriver.Chrome()  # or webdriver.Firefox()


def test_login_page():
    # Load the login.html page
    driver.get("http://localhost:3000/login.html")  # Adjust path as necessary
    time.sleep(2)  # Wait for the page to load

    # Check the title of the page
    assert "Login" in driver.title, "Title does not match"

    # Verify presence of the login form
    login_form = driver.find_element(By.ID, "loginForm")
    assert login_form.is_displayed(), "Login form is not displayed"

    # Verify form fields are present
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    assert username_input.is_displayed(), "Username input is not displayed"
    assert password_input.is_displayed(), "Password input is not displayed"

    # Test a successful login (replace with valid credentials)
    username_input.send_keys("valid_username")  # Replace with a valid username
    password_input.send_keys("valid_password")  # Replace with a valid password
    login_form.submit()  # Submit the form

    time.sleep(2)  # Wait for the page to load after login

    # Check if redirected to the dashboard
    assert (
        "dashboard.html" in driver.current_url
    ), "Not redirected to dashboard after login"

    # Check for token in localStorage (this needs to be done through JavaScript)
    token = driver.execute_script("return localStorage.getItem('token');")
    assert token is not None, "Token not set in localStorage after successful login"

    # Log out to reset state (if applicable)
    # This step would depend on how you handle logout in your app

    # Test a failed login
    username_input.clear()
    password_input.clear()
    username_input.send_keys("invalid_username")  # Invalid username
    password_input.send_keys("invalid_password")  # Invalid password
    login_form.submit()  # Submit the form

    time.sleep(2)  # Wait for the error message to appear

    # Check for error alert (this assumes the alert is shown)
    alert = driver.switch_to.alert
    assert alert is not None, "No alert shown for invalid login"
    assert (
        "Invalid credentials" in alert.text
    ), "Incorrect error message for invalid login"
    alert.accept()  # Dismiss the alert

    print("Login page test passed!")


if __name__ == "__main__":
    try:
        test_login_page()
    finally:
        driver.quit()  # Close the browser
