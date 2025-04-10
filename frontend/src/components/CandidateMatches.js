import React, { useEffect, useState } from "react";
import axios from "axios";

function CandidateMatches({ jobId }) {
  const [matches, setMatches] = useState([]);

  useEffect(() => {
    const fetchMatches = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/v1/matches/${jobId}`);
        setMatches(response.data);
      } catch (error) {
        console.error("Error fetching matches:", error);
      }
    };

    fetchMatches();
  }, [jobId]);

  return (
    <div className="p-4 border rounded shadow">
      <h2 className="text-lg font-bold mb-2">Candidate Matches</h2>
      <ul>
        {matches.map((match) => (
          <li key={match.candidate_id} className="mb-2">
            <h3 className="font-bold">{match.name}</h3>
            <p>Match Score: {match.match_score}</p>
            <p>Email: {match.email}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CandidateMatches;