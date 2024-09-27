from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize WebDriver
driver = webdriver.Chrome()  # or webdriver.Firefox()


def test_signup_page():
    # Load the signup.html page
    driver.get("http://localhost:3000/signup.html")  # Adjust path as necessary
    time.sleep(2)  # Wait for the page to load

    # Check the title of the page
    assert "Sign Up" in driver.title, "Title does not match"

    # Verify presence of the sign-up form
    signup_form = driver.find_element(By.ID, "signupForm")
    assert signup_form.is_displayed(), "Sign up form is not displayed"

    # Verify form fields are present
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    role_select = driver.find_element(By.ID, "role")
    assert username_input.is_displayed(), "Username input is not displayed"
    assert password_input.is_displayed(), "Password input is not displayed"
    assert role_select.is_displayed(), "Role select is not displayed"

    # Test a successful sign-up (replace with valid credentials)
    username_input.send_keys("new_username")  # Replace with a unique valid username
    password_input.send_keys("new_password")  # Replace with a valid password
    role_select.send_keys("User")  # Select a role
    signup_form.submit()  # Submit the form

    time.sleep(2)  # Wait for the page to load after sign-up

    # Check for success alert and redirection to login
    alert = driver.switch_to.alert
    assert alert is not None, "No alert shown for successful signup"
    assert "Account created successfully" in alert.text, "Incorrect success message"
    alert.accept()  # Dismiss the alert

    # Check if redirected to the login page
    assert "login.html" in driver.current_url, "Not redirected to login after signup"

    # Test a failed sign-up (e.g., existing username)
    username_input.clear()
    password_input.clear()
    username_input.send_keys("existing_username")  # Use a username that already exists
    password_input.send_keys("another_password")
    role_select.send_keys("User")
    signup_form.submit()  # Submit the form

    time.sleep(2)  # Wait for the error message to appear

    # Check for error alert (this assumes the alert is shown)
    alert = driver.switch_to.alert
    assert alert is not None, "No alert shown for invalid signup"
    assert (
        "Username already exists" in alert.text
    ), "Incorrect error message for existing username"
    alert.accept()  # Dismiss the alert

    print("Sign up page test passed!")


if __name__ == "__main__":
    try:
        test_signup_page()
    finally:
        driver.quit()  # Close the browser
