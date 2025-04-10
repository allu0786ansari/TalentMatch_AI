import React, { useState } from "react";
import CandidateMatches from "../components/CandidateMatches";

function Matches() {
  const [jobId, setJobId] = useState("");

  const handleJobIdChange = (e) => {
    setJobId(e.target.value);
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Matches</h1>
      <div className="mb-4">
        <input
          type="text"
          placeholder="Enter Job ID"
          value={jobId}
          onChange={handleJobIdChange}
          className="p-2 border rounded w-full"
        />
      </div>
      {jobId && <CandidateMatches jobId={jobId} />}
    </div>
  );
}

export default Matches;