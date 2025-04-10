import React from "react";
import ResumeUpload from "../components/ResumeUpload";
import JobListings from "../components/JobListings";

function Dashboard() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <ResumeUpload />
        </div>
        <div>
          <JobListings />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;