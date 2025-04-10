import React, { useState } from "react";
import axios from "axios";

function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [parsedData, setParsedData] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/api/v1/resume/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setParsedData(response.data);
      setMessage("Resume uploaded successfully!");
    } catch (error) {
      setMessage("Failed to upload resume.");
      console.error(error);
    }
  };

  return (
    <div className="p-4 border rounded shadow">
      <h2 className="text-lg font-bold mb-2">Upload Resume</h2>
      <input type="file" onChange={handleFileChange} className="mb-2" />
      <button onClick={handleUpload} className="bg-blue-600 text-white px-4 py-2 rounded">
        Upload
      </button>
      {message && <p className="mt-2 text-sm">{message}</p>}
      {parsedData && (
        <div className="mt-4">
          <h3 className="font-bold">Parsed Resume Data:</h3>
          <pre className="bg-gray-100 p-2 rounded">{JSON.stringify(parsedData, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default ResumeUpload;