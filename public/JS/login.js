document
  .getElementById("loginForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (!username) {
      alert("Username is required");
      return;
    }

    if (!password) {
      alert("Password is required");
      return;
    }

    const response = await fetch("http://localhost:3000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const result = await response.json();
    if (response.ok) {
      localStorage.setItem("token", result.token);
      const role = JSON.parse(atob(result.token.split(".")[1])).role;
      window.location.href = `dashboard.html?role=${role}`;
    } else {
      alert(result.error);
    }
  });
