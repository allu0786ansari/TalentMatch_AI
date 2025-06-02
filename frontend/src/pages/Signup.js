import React from "react";
import AuthForm from "../components/AuthForm";

function Signup() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="w-full max-w-md p-8 bg-white rounded-lg shadow-md">
        <h1 className="text-3xl font-extrabold mb-6 text-center text-blue-700">
          Create Your Account
        </h1>
        <p className="mb-6 text-center text-gray-600">
          Join SmartRecruit AI and start your journey!
        </p>
        <AuthForm type="signup" />
        <div className="mt-6 text-center text-sm text-gray-500">
          Already have an account?{" "}
          <a href="/login" className="text-blue-600 hover:underline">
            Log in
          </a>
        </div>
      </div>
    </div>
  );
}

export default Signup;