from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
driver = webdriver.Chrome()  # or webdriver.Firefox()

# Define credentials
user_credentials = {"username": "user", "password": "pass1234"}
admin_credentials = {"username": "admin", "password": "passadmin"}


def print_result(test_case, result):
    print(f"{test_case}: {'PASSED' if result else 'FAILED'}")


def login(username, password):
    driver.get("http://127.0.0.1:5500/public/login.html")
    time.sleep(2)
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    username_input.send_keys(username)
    password_input.send_keys(password)
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(2)


def logout():
    driver.find_element(By.LINK_TEXT, "Logout").click()
    time.sleep(2)


def test_dashboard_page(role):
    # Use appropriate credentials based on the role
    credentials = admin_credentials if role == "admin" else user_credentials
    login(credentials["username"], credentials["password"])

    # Load the dashboard.html page
    driver.get(
        f"http://127.0.0.1:5500/public/dashboard.html?role={role}"
    )  # Adjust path as necessary
    time.sleep(2)  # Wait for the page to load

    # Check the title of the page
    result = "Dashboard" in driver.title
    print_result("Check page title", result)

    # Verify the dashboard content loads based on the role
    dashboard_content = driver.find_element(By.ID, "dashboardContent")
    result = dashboard_content.is_displayed()
    print_result("Dashboard content presence", result)

    if role == "admin":
        # Wait for the users table to be present
        users_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        result = (
            users_table.is_displayed()
            and "User" in users_table.text
            and "Tasks Completed (%)" in users_table.text
        )
        print_result("Admin dashboard content", result)
    else:
        # Verify user specific content (task form)
        task_form = driver.find_element(By.ID, "taskForm")
        result = task_form.is_displayed()
        print_result("Task form presence", result)

        # Create tasks
        tasks = ["Task 1", "Task 2", "Task 3"]
        for task in tasks:
            task_input = driver.find_element(By.ID, "taskInput")
            task_input.send_keys(task)
            task_form.submit()
            time.sleep(1)  # Wait for the task to be added

        # Verify tasks appear in the task list
        task_list = driver.find_element(By.ID, "taskList")
        for task in tasks:
            result = task in task_list.text
            print_result(f"Task '{task}' added", result)

        # Test task completion
        toggle_buttons = task_list.find_elements(By.CSS_SELECTOR, ".toggle-btn")
        toggle_buttons[0].click()  # Complete the first task
        time.sleep(1)  # Wait for the task to be toggled

        # Verify the task is marked as completed
        completed_task = task_list.find_element(
            By.CSS_SELECTOR, ".task-card .task-text"
        )
        result = "text-decoration: line-through;" in completed_task.get_attribute(
            "style"
        )
        print_result("Task completion", result)

        # Re-locate the toggle button before unchecking the task
        toggle_buttons = task_list.find_elements(By.CSS_SELECTOR, ".toggle-btn")
        toggle_buttons[0].click()  # Uncheck the first task
        time.sleep(1)  # Wait for the task to be toggled

        # Verify the task is marked as active
        completed_task = task_list.find_element(
            By.CSS_SELECTOR, ".task-card .task-text"
        )
        result = "text-decoration: line-through;" not in completed_task.get_attribute(
            "style"
        )
        print_result("Task unchecking", result)

        # Test filtering tasks
        driver.find_element(By.ID, "filterCompleted").click()
        time.sleep(1)  # Wait for the filter to apply
        result = "Task 1" not in task_list.text
        print_result("Filter completed tasks", result)

        driver.find_element(By.ID, "filterActive").click()
        time.sleep(1)  # Wait for the filter to apply
        result = "Task 1" in task_list.text
        print_result("Filter active tasks", result)

        driver.find_element(By.ID, "filterAll").click()
        time.sleep(1)  # Wait for the filter to apply
        for task in tasks:
            result = task in task_list.text
            print_result(f"Filter all tasks - '{task}'", result)

        # Test editing a task
        edit_buttons = task_list.find_elements(By.CSS_SELECTOR, ".edit-btn")
        edit_buttons[0].click()  # Edit the first task
        time.sleep(1)  # Wait for the edit prompt

        driver.switch_to.alert.send_keys("Edited Task")
        driver.switch_to.alert.accept()
        time.sleep(2)  # Wait for the task to be edited

        # Verify the task is updated
        result = "Edited Task" in task_list.text
        print_result("Task editing", result)

        # Test deleting the task
        delete_button = task_list.find_element(By.CSS_SELECTOR, ".delete-btn")
        delete_button.click()
        time.sleep(2)  # Wait for the task to be deleted

        # Verify the task is removed from the list
        result = "Edited Task" not in task_list.text
        print_result("Task deletion", result)

    # Test successful logout
    logout()
    result = "index.html" in driver.current_url
    print_result("Successful logout redirection", result)

    print(f"Dashboard page test passed for role: {role}")


def test_dashboard_without_login():
    # Load the dashboard.html page without logging in
    driver.get(
        "http://127.0.0.1:5500/public/dashboard.html?role=user"
    )  # Adjust path as necessary
    time.sleep(2)  # Wait for the page to load

    # Verify no tasks are visible
    task_list = driver.find_element(By.ID, "taskList")
    result = task_list.text == ""
    print_result("Dashboard without login - no tasks visible", result)

    print("Dashboard without login test completed!")


if __name__ == "__main__":
    try:
        test_dashboard_without_login()  # Test accessing dashboard without login
        test_dashboard_page("admin")  # Test as admin
        test_dashboard_page("user")  # Test as user
    finally:
        driver.quit()  # Close the browser
