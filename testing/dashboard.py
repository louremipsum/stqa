from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize WebDriver
driver = webdriver.Chrome()  # or webdriver.Firefox()


def test_dashboard_page(role):
    # Load the dashboard.html page
    driver.get(
        f"http://localhost:3000/dashboard.html?role={role}"
    )  # Adjust path as necessary
    time.sleep(2)  # Wait for the page to load

    # Check the title of the page
    assert "Dashboard" in driver.title, "Title does not match"

    # Verify the dashboard content loads based on the role
    dashboard_content = driver.find_element(By.ID, "dashboardContent")
    assert dashboard_content.is_displayed(), "Dashboard content is not displayed"

    if role == "admin":
        # Verify admin specific content
        time.sleep(2)  # Wait for the users to load
        users_table = dashboard_content.find_element(By.TAG_NAME, "table")
        assert users_table.is_displayed(), "User table is not displayed"
        assert "User" in users_table.text, "User column is missing"
        assert "Tasks Completed (%)" in users_table.text, "Completion column is missing"
    else:
        # Verify user specific content (task form)
        task_form = driver.find_element(By.ID, "taskForm")
        assert task_form.is_displayed(), "Task form is not displayed"

        # Test adding a task
        task_input = driver.find_element(By.ID, "taskInput")
        task_input.send_keys("Test Task")
        task_form.submit()
        time.sleep(2)  # Wait for the task to be added

        # Verify the task appears in the task list
        task_list = driver.find_element(By.ID, "taskList")
        assert "Test Task" in task_list.text, "Task was not added to the list"

        # Test task completion
        toggle_button = task_list.find_element(By.CSS_SELECTOR, ".toggle-btn")
        toggle_button.click()
        time.sleep(2)  # Wait for the task to be toggled

        # Verify the task is marked as completed
        assert "text-decoration: line-through;" in toggle_button.find_element(
            By.XPATH, ".."
        ).get_attribute("style"), "Task was not marked as completed"

        # Test editing the task
        edit_button = task_list.find_element(By.CSS_SELECTOR, ".edit-btn")
        edit_button.click()
        time.sleep(1)  # Wait for prompt
        driver.switch_to.alert.send_keys("Edited Task")
        driver.switch_to.alert.accept()
        time.sleep(2)  # Wait for the task to be edited

        # Verify the task is updated
        assert "Edited Task" in task_list.text, "Task was not updated"

        # Test deleting the task
        delete_button = task_list.find_element(By.CSS_SELECTOR, ".delete-btn")
        delete_button.click()
        time.sleep(2)  # Wait for the task to be deleted

        # Verify the task is removed from the list
        assert "Edited Task" not in task_list.text, "Task was not deleted"

    print(f"Dashboard page test passed for role: {role}")


if __name__ == "__main__":
    try:
        test_dashboard_page("admin")  # Test as admin
        test_dashboard_page("user")  # Test as user
    finally:
        driver.quit()  # Close the browser
