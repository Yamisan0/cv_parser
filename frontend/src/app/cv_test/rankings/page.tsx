'use client';

import React, { useState } from 'react';

interface Ranking {
  rank: number;
  file_path: string;
  score: number;
  alerteFort: boolean;
}

const RankingsList: React.FC<{ rankings: Ranking[] }> = ({ rankings }) => {
  return (
    <div className="max-w-2xl mx-auto mt-10 bg-black p-6 rounded-lg shadow-md">
      <h1 className="text-3xl font-bold mb-6 text-center">Ranking</h1>
      <p className="text-sm text-center text-gray-500 mb-4">
        <span className="inline-block h-3 w-3 bg-red-500 rounded-full mr-2"></span>
         = Aucun point fort trouvé
          </p>
        <ul className="space-y-4">
        {rankings.map((item, index) => (
          <li key={index} className="bg-gray-100 p-4 rounded-lg flex justify-between items-center shadow">
            <span className="text-xl text-black font-medium flex-grow">{index + 1}. {item.file_path.split('/').pop()}</span>
            <div className="flex items-center">
              <span className="text-lg text-gray-600 mr-2">{item.score} points</span>
              <span className={`h-3 w-3 rounded-full ${item.alerteFort ? "bg-red-500" : "opacity-0"}`} title="Alerte Fort"></span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

const Home = () => {
  const [rankings, setRankings] = useState<Ranking[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRankings = async () => {
    setLoading(true);
    setError(null);

    const token = localStorage.getItem('token');
      if (!token) {
        console.error('No token found in local storage.');
        return;
      }

    try {
      const response = await fetch('http://localhost:8000/cv/rankings', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      console.log("Response: ", response);
      if (!response.ok) {
        throw new Error('Failed to fetch rankings');
      }
      const data = await response.json();
      console.log("API Response Data: ", data);
      setRankings(data);
    } catch (err: any) {
      console.error("Error: ", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gradient-to-r from-blue-500 to-purple-500 min-h-screen flex flex-col items-center justify-center">
      <button
        onClick={fetchRankings}
        className="bg-green-500 text-white font-bold py-2 px-4 rounded mb-6"
        disabled={loading}
      >
        {loading ? 'Loading...' : 'Fetch Rankings'}
      </button>
      {error && <p className="text-red-500">{error}</p>}
      {rankings.length > 0 && <RankingsList rankings={rankings} />}
    </div>
  );
};

export default Home;
