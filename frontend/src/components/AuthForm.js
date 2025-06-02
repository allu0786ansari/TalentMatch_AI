import React, { useState } from "react";
import axios from "axios";

function AuthForm({ type }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  // Additional fields for signup
  const [name, setName] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");

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
    const payload =
      type === "login"
        ? { email, password }
        : { name, email, password };

    try {
      const response = await axios.post(
        `http://localhost:8000/api/v1${endpoint}`,
        payload
      );
      console.log(response.data);
      alert(`${type === "login" ? "Logged in" : "Signed up"} successfully!`);
      // Optionally, redirect or clear form here
    } catch (error) {
      console.error("Error:", error);
      setError(
        error.response?.data?.message ||
          "An error occurred. Please try again."
      );
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border rounded shadow bg-white">
      <h2 className="text-lg font-bold mb-2">
        {type === "login" ? "Login" : "Signup"}
      </h2>
      {error && (
        <div className="mb-2 text-red-600 text-sm">{error}</div>
      )}
      {type === "signup" && (
        <input
          type="text"
          placeholder="Full Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="block mb-2 p-2 border rounded w-full"
          autoComplete="name"
        />
      )}
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="block mb-2 p-2 border rounded w-full"
        autoComplete="email"
      />
      <div className="relative mb-2">
        <input
          type={showPassword ? "text" : "password"}
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="block p-2 border rounded w-full pr-10"
          autoComplete={type === "login" ? "current-password" : "new-password"}
        />
        <button
          type="button"
          className="absolute right-2 top-2 text-xs text-gray-500"
          onClick={() => setShowPassword((prev) => !prev)}
          tabIndex={-1}
        >
          {showPassword ? "Hide" : "Show"}
        </button>
      </div>
      {type === "signup" && (
        <input
          type={showPassword ? "text" : "password"}
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          className="block mb-2 p-2 border rounded w-full"
          autoComplete="new-password"
        />
      )}
      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded w-full mt-2"
      >
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