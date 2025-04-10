import React, { useEffect, useState } from "react";
import axios from "axios";
import JobForm from "./JobForm";

function JobListings() {
  const [jobs, setJobs] = useState([]);
  const [editingJob, setEditingJob] = useState(null);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/v1/jobs");
      setJobs(response.data);
    } catch (error) {
      console.error("Error fetching jobs:", error);
    }
  };

  const handleDelete = async (jobId) => {
    try {
      await axios.delete(`http://localhost:8000/api/v1/jobs/${jobId}`);
      fetchJobs();
    } catch (error) {
      console.error("Error deleting job:", error);
    }
  };

  return (
    <div className="p-4 border rounded shadow">
      <h2 className="text-lg font-bold mb-2">Job Listings</h2>
      <JobForm fetchJobs={fetchJobs} editingJob={editingJob} setEditingJob={setEditingJob} />
      <ul>
        {jobs.map((job) => (
          <li key={job.id} className="mb-2">
            <h3 className="font-bold">{job.title}</h3>
            <p>{job.description}</p>
            <button
              onClick={() => setEditingJob(job)}
              className="bg-yellow-500 text-white px-2 py-1 rounded mr-2"
            >
              Edit
            </button>
            <button
              onClick={() => handleDelete(job.id)}
              className="bg-red-600 text-white px-2 py-1 rounded"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default JobListings;