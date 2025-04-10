import React from "react";
import AuthForm from "../components/AuthForm";

function Signup() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Signup</h1>
      <AuthForm type="signup" />
    </div>
  );
}

export default Signup;