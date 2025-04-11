import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import ResumeUpload from "./components/ResumeUpload";
import JobListings from "./components/JobListings";
import Login from "./pages/Login";
import Signup from "./pages/Signup";

function App() {
  return (
    <Router>
      <Routes>
        {/* Wrap all routes with the Layout */}
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="ResumeUpload" element={<ResumeUpload />} />
          <Route path="JobListings" element={<JobListings />} />
          <Route path="CandidateMatches" element={<Dashboard />} />
          <Route path="Login" element={<Login />} />
          <Route path="Signup" element={<Signup />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;