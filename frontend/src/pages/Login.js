import React from "react";
import AuthForm from "../components/AuthForm";

function Login() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="w-full max-w-md p-8 bg-white rounded-lg shadow-md">
        <h1 className="text-3xl font-extrabold mb-6 text-center text-blue-700">
          Welcome Back
        </h1>
        <p className="mb-6 text-center text-gray-600">
          Log in to your SmartRecruit AI account
        </p>
        <AuthForm type="login" />
        <div className="mt-6 text-center text-sm text-gray-500">
          Don't have an account?{" "}
          <a href="/signup" className="text-blue-600 hover:underline">
            Sign up
          </a>
        </div>
      </div>
    </div>
  );
}

export default Login;