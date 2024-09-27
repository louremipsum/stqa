window.onload = async function () {
  const token = localStorage.getItem("token");
  const urlParams = new URLSearchParams(window.location.search);
  const role = urlParams.get("role");
  const dashboardContent = document.getElementById("dashboardContent");

  if (role === "admin") {
    const response = await fetch("http://localhost:3000/admin/users", {
      headers: { Authorization: `Bearer ${token}` },
    });

    const users = await response.json();
    let tableContent = `<h2>Admin Dashboard</h2><table><tr><th>User</th><th>Tasks Completed (%)</th></tr>`;

    users.forEach((user) => {
      tableContent += `<tr><td>${user.username}</td><td>${user.completionRate}%</td></tr>`;
    });

    tableContent += "</table>";
    dashboardContent.innerHTML = tableContent;
  } else {
    const taskFormHTML = `
    <h2>Your To-Do List</h2>
    <form id="taskForm">
        <input type="text" id="taskInput" placeholder="Enter task" required>
        <button type="submit">Add Task</button>
    </form>
    <div>
        <button id="filterAll">All</button>
        <button id="filterActive">Active</button>
        <button id="filterCompleted">Completed</button>
        <button id="clearCompleted">Clear Completed</button>
    </div>
    <ul id="taskList"></ul>
  `;
    dashboardContent.innerHTML = taskFormHTML;

    document
      .getElementById("taskForm")
      .addEventListener("submit", async function (e) {
        e.preventDefault();
        const task = document.getElementById("taskInput").value;

        const response = await fetch("http://localhost:3000/task", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ task }),
        });

        if (response.ok) {
          loadTasks(); // Refresh the task list
          document.getElementById("taskInput").value = "";
        } else {
          const error = await response.json();
          alert(error.error || "Error creating task");
        }
      });

    document
      .getElementById("clearCompleted")
      .addEventListener("click", async function () {
        const response = await fetch("http://localhost:3000/clear-completed", {
          method: "DELETE",
          headers: { Authorization: `Bearer ${token}` },
        });

        if (response.ok) {
          loadTasks(); // Refresh the task list
        } else {
          const error = await response.json();
          alert(error.error || "Error clearing completed tasks");
        }
      });

    document
      .getElementById("filterAll")
      .addEventListener("click", () => loadTasks());
    document
      .getElementById("filterActive")
      .addEventListener("click", () => loadTasks("active"));
    document
      .getElementById("filterCompleted")
      .addEventListener("click", () => loadTasks("completed"));

    loadTasks(); // Initial load of tasks
  }
};

async function loadTasks(filter = "all") {
  const token = localStorage.getItem("token");
  const response = await fetch("http://localhost:3000/tasks", {
    headers: { Authorization: `Bearer ${token}` },
  });
  const tasks = await response.json();
  const taskList = document.getElementById("taskList");
  taskList.innerHTML = ""; // Clear current task list

  const filteredTasks = tasks.filter((task) => {
    if (filter === "completed") return task.completed;
    if (filter === "active") return !task.completed;
    return true; // "all"
  });

  filteredTasks.forEach((task) => {
    const taskCard = document.createElement("li");
    taskCard.className = "task-card";
    taskCard.innerHTML = `
      <div class="task-content" style="flex-grow: 1;">
        <span class="task-text" style="${
          task.completed ? "text-decoration: line-through;" : ""
        }">
          ${task.task}
        </span>
      </div>
      <button class="toggle-btn" data-id="${task._id}">
        ${task.completed ? "Undo" : "Complete"}
      </button>
      <button class="edit-btn" data-id="${task._id}">Edit</button>
      <button class="delete-btn" data-id="${task._id}">Delete</button>
    `;

    taskList.appendChild(taskCard);

    // Event listeners for buttons
    taskCard
      .querySelector(".toggle-btn")
      .addEventListener("click", async function () {
        const response = await fetch(`http://localhost:3000/task/${task._id}`, {
          method: "PUT",
          headers: { Authorization: `Bearer ${token}` },
        });

        if (response.ok) {
          loadTasks(); // Refresh the task list
        } else {
          const error = await response.json();
          alert(error.error || "Error toggling task completion");
        }
      });

    taskCard
      .querySelector(".edit-btn")
      .addEventListener("click", () => editTask(task._id));
    taskCard
      .querySelector(".delete-btn")
      .addEventListener("click", async function () {
        const response = await fetch(`http://localhost:3000/task/${task._id}`, {
          method: "DELETE",
          headers: { Authorization: `Bearer ${token}` },
        });

        if (response.ok) {
          loadTasks(); // Refresh the task list
        } else {
          const error = await response.json();
          alert(error.error || "Error deleting task");
        }
      });
  });
}

async function editTask(taskId) {
  const newTask = prompt("Edit your task:");
  if (!newTask) return; // If input is empty, do nothing

  const token = localStorage.getItem("token");
  const response = await fetch(`http://localhost:3000/task/${taskId}`, {
    method: "PUT", // This is the correct method for editing
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ task: newTask }), // Send the updated task
  });

  if (response.ok) {
    loadTasks(); // Refresh the task list
  } else {
    const error = await response.json();
    console.error("Error editing task:", error); // Debug log
    alert(error.error || "Error editing task");
  }
}
