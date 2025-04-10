import React, { useState, useEffect } from "react";
import axios from "axios";

function JobForm({ fetchJobs, editingJob, setEditingJob }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    if (editingJob) {
      setTitle(editingJob.title);
      setDescription(editingJob.description);
    }
  }, [editingJob]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingJob) {
        // Update job
        await axios.put(`http://localhost:8000/api/v1/jobs/${editingJob.id}`, {
          title,
          description,
        });
        setEditingJob(null);
      } else {
        // Create new job
        await axios.post("http://localhost:8000/api/v1/jobs", {
          title,
          description,
        });
      }
      setTitle("");
      setDescription("");
      fetchJobs();
    } catch (error) {
      console.error("Error saving job:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border rounded shadow mb-4">
      <h2 className="text-lg font-bold mb-2">
        {editingJob ? "Edit Job" : "Create Job"}
      </h2>
      <input
        type="text"
        placeholder="Job Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="block mb-2 p-2 border rounded w-full"
      />
      <textarea
        placeholder="Job Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        className="block mb-2 p-2 border rounded w-full"
      />
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
        {editingJob ? "Update Job" : "Create Job"}
      </button>
    </form>
  );
}

export default JobForm;