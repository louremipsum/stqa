from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize WebDriver
driver = webdriver.Chrome()  # or webdriver.Firefox()


def print_result(test_case, result):
    print(f"{test_case}: {'PASSED' if result else 'FAILED'}")


def test_index_page():
    # Load the index.html page
    driver.get("http://127.0.0.1:5500/public/index.html")  # Adjust path as necessary
    time.sleep(2)  # Wait for the page to load

    # Check the title of the page
    result = "Todo List App" in driver.title
    print_result("Check page title", result)

    # Verify the presence of the logo
    logo = driver.find_element(By.CLASS_NAME, "nav-logo")
    result = logo.is_displayed()
    print_result("Logo presence", result)

    # Verify the presence of navigation links
    nav_links = driver.find_elements(By.CSS_SELECTOR, ".nav-links a")
    result = len(nav_links) == 2
    print_result("Navigation links count", result)
    result = nav_links[0].text == "Login"
    print_result("First navigation link text", result)
    result = nav_links[1].text == "Sign Up"
    print_result("Second navigation link text", result)

    # Verify header text
    header = driver.find_element(By.TAG_NAME, "h1")
    result = header.text == "Welcome to TodoApp"
    print_result("Header text", result)

    # Verify paragraph text
    paragraph = driver.find_element(By.TAG_NAME, "p")
    result = paragraph.text == "The ultimate solution to manage your tasks efficiently."
    print_result("Paragraph text", result)

    # Verify list items
    list_items = driver.find_elements(By.TAG_NAME, "li")
    result = len(list_items) == 3
    print_result("List items count", result)
    expected_items = [
        "Create and manage your to-do list.",
        "Filter tasks by status.",
        "Admin dashboard to monitor users and task completion.",
    ]
    for i, item in enumerate(list_items):
        result = item.text == expected_items[i]
        print_result(f"List item {i + 1} text", result)

    # Verify footer text
    footer = driver.find_element(By.TAG_NAME, "footer")
    result = "© 2024 TodoApp. All rights reserved." in footer.text
    print_result("Footer text", result)

    print("Index page test completed!")


if __name__ == "__main__":
    try:
        test_index_page()
    finally:
        driver.quit()  # Close the browser
