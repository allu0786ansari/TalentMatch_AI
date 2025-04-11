import React from "react";
import { Link, Outlet } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css"; // Import Bootstrap CSS
import "bootstrap-icons/font/bootstrap-icons.css"; // Import Bootstrap Icons

function Layout() {
  return (
    <div className="d-flex vh-100">
      {/* Sidebar */}
      <div className="bg-dark text-white p-3" style={{ width: "250px" }}>
        <h2 className="text-center mb-4">TalentMatchAI</h2>
        <ul className="nav flex-column">
          <li className="nav-item mb-2">
            <Link to="/" className="nav-link text-white d-flex align-items-center">
              <i className="bi bi-house-door-fill me-2"></i> Home
            </Link>
          </li>
          <li className="nav-item mb-2">
            <Link to="/ResumeUpload" className="nav-link text-white d-flex align-items-center">
              <i className="bi bi-upload me-2"></i> Resume Upload
            </Link>
          </li>
          <li className="nav-item mb-2">
            <Link to="/JobListings" className="nav-link text-white d-flex align-items-center">
              <i className="bi bi-file-earmark-text me-2"></i> Job Listings
            </Link>
          </li>
          <li className="nav-item mb-2">
            <Link to="/CandidateMatches" className="nav-link text-white d-flex align-items-center">
              <i className="bi bi-search me-2"></i> Candidate Matching
            </Link>
          </li>
        </ul>
        <hr className="text-white" />
        <h6 className="text-uppercase text-white">Account</h6>
        <ul className="nav flex-column">
          <li className="nav-item mb-2">
            <Link to="/Login" className="nav-link text-white d-flex align-items-center">
              <i className="bi bi-person me-2"></i> Login
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/Signup" className="nav-link text-white d-flex align-items-center">
              <i className="bi bi-shield-lock me-2"></i> Signup
            </Link>
          </li>
        </ul>
      </div>

      {/* Main Content */}
      <div className="flex-grow-1 p-4">
        <Outlet /> {/* This renders the child routes */}
      </div>
    </div>
  );
}

export default Layout;