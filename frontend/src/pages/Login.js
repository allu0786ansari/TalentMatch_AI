import React from "react";
import AuthForm from "../components/AuthForm";

function Login() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Login</h1>
      <AuthForm type="login" />
    </div>
  );
}

export default Login;