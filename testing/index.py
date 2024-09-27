from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize WebDriver
driver = webdriver.Chrome()  # or webdriver.Firefox()

def test_index_page():
    # Load the index.html page
    driver.get("http://localhost:3000/index.html")  # Adjust path as necessary
    time.sleep(2)  # Wait for the page to load

    # Check the title of the page
    assert "Todo List App" in driver.title, "Title does not match"

    # Verify the presence of the logo
    logo = driver.find_element(By.CLASS_NAME, "nav-logo")
    assert logo.is_displayed(), "Logo is not displayed"

    # Verify the presence of navigation links
    login_link = driver.find_element(By.LINK_TEXT, "Login")
    assert login_link.is_displayed(), "Login link is not displayed"
    signup_link = driver.find_element(By.LINK_TEXT, "Sign Up")
    assert signup_link.is_displayed(), "Sign Up link is not displayed"

    # Verify header text
    header = driver.find_element(By.TAG_NAME, "h1")
    assert header.text == "Welcome to TodoApp", "Header text does not match"

    # Verify paragraph text
    paragraph = driver.find_element(By.TAG_NAME, "p")
    assert paragraph.text == "The ultimate solution to manage your tasks efficiently.", "Paragraph text does not match"

    # Verify list items
    list_items = driver.find_elements(By.TAG_NAME, "li")
    assert len(list_items) == 3, "List items count does not match"
    expected_items = [
        "Create and manage your to-do list.",
        "Filter tasks by status.",
        "Admin dashboard to monitor users and task completion."
    ]
    for i, item in enumerate(list_items):
        assert item.text == expected_items[i], f"List item {i + 1} does not match"

    # Verify footer text
    footer = driver.find_element(By.TAG_NAME, "footer")
    assert "© 2024 TodoApp. All rights reserved." in footer.text, "Footer text does not match"

    print("Index page test passed!")

if __name__ == "__main__":
    try:
        test_index_page()
    finally:
        driver.quit()  # Close the browser
