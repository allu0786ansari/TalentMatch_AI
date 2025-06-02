import React, { useState } from "react";
import axios from "axios";

function AuthForm({ type, onAuth }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("candidate"); // default role for signup

  const handleSubmit = async (e) => {
    e.preventDefault();
    const endpoint = type === "login" ? "/auth/login" : "/auth/signup";
    const payload =
      type === "signup"
        ? { email, password, name: email.split("@")[0], role }
        : { email, password };

    try {
      const response = await axios.post(
        `http://localhost:8000/api/v1${endpoint}`,
        payload
      );
      if (type === "login") {
        // Save token and role in localStorage
        localStorage.setItem("token", response.data.access_token);
        localStorage.setItem("role", response.data.role); // backend should return role on login
        if (onAuth) onAuth(response.data.role);
        alert("Logged in successfully!");
      } else {
        alert("Signed up successfully!");
      }
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          error.response?.data?.message ||
          "An error occurred."
      );
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border rounded shadow">
      <h2 className="text-lg font-bold mb-2">
        {type === "login" ? "Login" : "Signup"}
      </h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="block mb-2 p-2 border rounded w-full"
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="block mb-2 p-2 border rounded w-full"
        required
      />
      {type === "signup" && (
        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="block mb-2 p-2 border rounded w-full"
        >
          <option value="candidate">Candidate</option>
          <option value="recruiter">Recruiter</option>
        </select>
      )}
      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        {type === "login" ? "Login" : "Signup"}
      </button>
    </form>
  );
}

export default AuthForm;