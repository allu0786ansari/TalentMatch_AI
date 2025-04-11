import React from "react";
import ResumeUpload from "../components/ResumeUpload";
import JobListings from "../components/JobListings";

function Dashboard() {
  return (
    <div className="flex-grow-1 p-4">
      <h1 className="mb-4">Dashboard</h1>
      <p>Welcome to your dashboard! Use the navigation to explore the features.</p>
      <div className="row mt-4">
        {/* Resume Upload Section */}
        <div className="col-md-6 mb-4">
          <div>
            <div>
              <h5>Resume Upload</h5>
              <p>Upload resumes and view parsed data.</p>
              <ResumeUpload /> {/* Render ResumeUpload component */}
            </div>
          </div>
        </div>

        {/* Job Listings Section */}
        <div className="col-md-6 mb-4">
          <div>
            <div>
              <h5>Job Listings</h5>
              <p>Manage job postings and descriptions.</p>
              <JobListings /> {/* Render JobListings component */}
            </div>
          </div>
        </div>

        {/* Candidate Matching Section */}
        <div className="col-md-6 mb-4">
          <div>
            <div>
              <h5>Candidate Matching</h5>
              <p>View matched candidates for job postings.</p>
              <a href="/candidate-matching" className="btn btn-primary">
                Go to Candidate Matching
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;