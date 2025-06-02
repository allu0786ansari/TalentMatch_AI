import React, { useState } from "react";
import axios from "axios";

function AuthForm({ type, onAuth }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // Signup validation
    if (type === "signup") {
      if (!name) {
        setError("Name is required.");
        return;
      }
      if (password !== confirmPassword) {
        setError("Passwords do not match.");
        return;
      }
    }

    const endpoint = type === "login" ? "/auth/login" : "/auth/signup";
    try {
      const response = await axios.post(`http://localhost:8000/api/v1${endpoint}`, { email, password });
      console.log(response.data);
      alert(`${type === "login" ? "Logged in" : "Signed up"} successfully!`);
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border rounded shadow">
      <h2 className="text-lg font-bold mb-2">{type === "login" ? "Login" : "Signup"}</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="block mb-2 p-2 border rounded w-full"
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="block mb-2 p-2 border rounded w-full"
      />
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
        {type === "login" ? "Login" : "Signup"}
      </button>
      {type === "login" && (
        <div className="mt-2 text-right">
          <a href="/forgot-password" className="text-blue-500 text-xs hover:underline">
            Forgot password?
          </a>
        </div>
      )}
    </form>
  );
}

export default AuthForm;