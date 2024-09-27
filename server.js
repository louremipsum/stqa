const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const bodyParser = require("body-parser");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const dotenv = require("dotenv");

dotenv.config(); // Load .env variables
const app = express();

app.use(cors());
app.use(bodyParser.json());

// User Schema
const UserSchema = new mongoose.Schema({
  username: String,
  password: String,
  role: String,
});

const User = mongoose.model("User", UserSchema);

// Task Schema
const TaskSchema = new mongoose.Schema({
  userId: mongoose.Schema.Types.ObjectId,
  task: String,
  completed: Boolean,
});

const Task = mongoose.model("Task", TaskSchema);

// JWT secret
const JWT_SECRET = "your_secret_key";

// Signup Route
app.post("/signup", async (req, res) => {
  const { username, password, role } = req.body;

  // Check if the user already exists
  const existingUser = await User.findOne({ username });
  if (existingUser) {
    return res.status(400).json({ error: "User already exists" });
  }

  const hashedPassword = await bcrypt.hash(password, 10);
  const newUser = new User({
    username,
    password: hashedPassword,
    role,
  });

  await newUser.save();
  res.json({ message: "User registered successfully" });
});

// Login Route
app.post("/login", async (req, res) => {
  const { username, password } = req.body;
  const user = await User.findOne({ username });

  if (!user) {
    return res.status(400).json({ error: "Invalid credentials" });
  }

  const isPasswordValid = await bcrypt.compare(password, user.password);
  if (!isPasswordValid) {
    return res.status(400).json({ error: "Invalid credentials" });
  }

  const token = jwt.sign({ userId: user._id, role: user.role }, JWT_SECRET, {
    expiresIn: "1h",
  });

  res.json({ token });
});

// Middleware to authenticate JWT
const authenticate = (req, res, next) => {
  const token = req.headers["authorization"];
  if (!token) return res.status(401).send("Access Denied");

  try {
    const verified = jwt.verify(token.split(" ")[1], JWT_SECRET);
    req.user = verified;
    next();
  } catch (err) {
    res.status(400).send("Invalid Token");
  }
};

// Create Task Route (protected)
app.post("/task", authenticate, async (req, res) => {
  const { task } = req.body;
  const newTask = new Task({
    userId: req.user.userId,
    task,
    completed: false,
  });

  await newTask.save();
  res.json({ message: "Task created successfully" });
});

// Get Tasks Route (protected)
app.get("/tasks", authenticate, async (req, res) => {
  const tasks = await Task.find({ userId: req.user.userId });
  res.json(tasks);
});

// Clear Completed Tasks Route (protected)
app.delete("/clear-completed", authenticate, async (req, res) => {
  try {
    await Task.deleteMany({ userId: req.user.userId, completed: true });
    res.json({ message: "Completed tasks cleared successfully" });
  } catch (error) {
    res.status(500).json({ error: "Could not clear completed tasks" });
  }
});

// Delete Task Route (protected)
app.delete("/task/:id", authenticate, async (req, res) => {
  const { id } = req.params;
  try {
    const task = await Task.findByIdAndDelete(id);
    if (!task) return res.status(404).json({ error: "Task not found" });
    res.json({ message: "Task deleted successfully" });
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: "Could not delete task" });
  }
});

// Update Task
app.put("/task/:id", authenticate, async (req, res) => {
  const { id } = req.params;
  try {
    const task = await Task.findById(id);
    if (!task) return res.status(404).json({ error: "Task not found" });

    // If the request body contains a task field, update the task content
    if (req.body.task) {
      task.task = req.body.task;
    }
    // Toggle completion status if no task field is present
    else {
      task.completed = !task.completed;
    }

    await task.save();
    res.json({
      message: "Task updated successfully",
      completed: task.completed,
    });
  } catch (error) {
    console.error("Error updating task:", error); // Debug log
    res.status(500).json({ error: "Could not update task" });
  }
});

// Admin Route to Get All Users and Task Completion
app.get("/admin/users", authenticate, async (req, res) => {
  if (req.user.role !== "admin") {
    return res.status(403).send("Access denied");
  }

  const users = await User.find({});
  const userTaskData = await Promise.all(
    users.map(async (user) => {
      const tasks = await Task.find({ userId: user._id });
      const completedTasks = tasks.filter((task) => task.completed).length;
      const completionRate =
        tasks.length > 0 ? (completedTasks / tasks.length) * 100 : 0;
      return {
        username: user.username,
        completionRate,
      };
    })
  );

  res.json(userTaskData);
});
mongoose
  .connect(process.env.MONGO_URI, {})
  .then(() => console.log("Connected to MongoDB Atlas"))
  .catch((error) => console.error("MongoDB connection error:", error));

// Start server
app.listen(3000, () => {
  console.log("Server is running on http://localhost:3000");
});
