document
  .getElementById("signupForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const role = document.getElementById("role").value;

    if (!username) {
      alert("Username is required");
      return;
    }

    if (!password) {
      alert("Password is required");
      return;
    }

    if (!role) {
      alert("Role is required");
      return;
    }

    const response = await fetch("http://localhost:3000/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password, role }),
    });

    const result = await response.json();
    if (response.ok) {
      alert("Account created successfully");
      window.location.href = "login.html";
    } else {
      alert(result.error);
    }
  });
