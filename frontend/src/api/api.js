import axios from "axios";

// Base URL for the backend API
const API_BASE_URL = "http://localhost:8000/api/v1";

// Axios instance for API calls
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Resume Upload
export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  const response = await api.post("/resume/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
};

// Fetch Job Listings
export const fetchJobs = async () => {
  const response = await api.get("/jobs");
  return response.data;
};

// Create Job
export const createJob = async (jobData) => {
  const response = await api.post("/jobs", jobData);
  return response.data;
};

// Update Job
export const updateJob = async (jobId, jobData) => {
  const response = await api.put(`/jobs/${jobId}`, jobData);
  return response.data;
};

// Delete Job
export const deleteJob = async (jobId) => {
  const response = await api.delete(`/jobs/${jobId}`);
  return response.data;
};

// Fetch Candidate Matches
export const fetchMatches = async (jobId) => {
  const response = await api.get(`/matches/${jobId}`);
  return response.data;
};

// Login
export const login = async (credentials) => {
  const response = await api.post("/auth/login", credentials);
  return response.data;
};

// Signup
export const signup = async (credentials) => {
  const response = await api.post("/auth/signup", credentials);
  return response.data;
};

export default api;