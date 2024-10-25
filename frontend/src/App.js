import React from 'react';
import GenderSelector from './GenderSelector';
import AgeRangeSelector from './AgeRangeSelector'; 
import './App.css';

import climbingImage from './assets/frontpage.png';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, ArcElement, Tooltip, Legend } from 'chart.js';

// Enregistrement des éléments nécessaires pour le graphique camembert
ChartJS.register(CategoryScale, LinearScale, ArcElement, Tooltip, Legend);

// Composant Home
function Home() {
  return (
    <div className="App">
      <img className="full-screen-image" src={climbingImage} alt="Climbing App Frontpage" />
      <div className="overlay">
        {/* Navigation vers le Dashboard */}
        <Link to="/dashboard" className="clickable-block">
          <h2>Dashboard</h2>
        </Link>
        {/* Lien vers l'API et GitHub */}
        <a href="http://localhost:5000/docs" className="clickable-block" target="_blank" rel="noopener noreferrer">  
          <h2>API</h2>
        </a>
        <a href="https://github.com/LucienLaumont" className="clickable-block" target="_blank" rel="noopener noreferrer">
          <h2>GitHub</h2>
        </a>
      </div>
    </div>
  );
}

// Composant Dashboard avec graphique dynamique
function Dashboard() {
  const [gender, setGender] = useState('both');
  const [ageRange, setAgeRange] = useState({ min: 18, max: 60 });
  const [chartData, setChartData] = useState(null);  // Données pour le graphique
  const [error, setError] = useState(null);  // Gestion des erreurs

  // Fonction pour récupérer les données depuis l'API
  const fetchClimbersData = async () => {
    try {
      let url = `http://localhost:5000/PieChart_Climbers?min_age=${ageRange.min}&max_age=${ageRange.max}`;
      if (gender !== 'both') {
        url += `&sex=${gender}`;
      }
      
      const response = await axios.get(url);
      const data = response.data;

      // Transformation des données pour le graphique
      const countries = Object.keys(data);
      const counts = Object.values(data);

      setChartData({
        labels: countries,
        datasets: [
          {
            label: 'Grimpeurs par pays',
            data: counts,
            backgroundColor: [
              '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
            ],
          },
        ],
      });
      setError(null);  // Réinitialiser l'erreur après récupération des données
    } catch (error) {
      console.error('Erreur lors de la récupération des données', error);
      setError('Erreur lors de la récupération des données.');
    }
  };

  // Appeler fetchClimbersData lorsque les filtres changent
  useEffect(() => {
    fetchClimbersData();
  }, [gender, ageRange]);

  // Gérer les changements de genre et d'âge
  const handleGenderChange = (newGender) => {
    setGender(newGender);
  };

  const handleAgeChange = (min, max) => {
    setAgeRange({ min, max });
  };

  return (
    <div className="dashboard">
      <div className="dashboard-block block1">Bloc 1</div>
      <div className="dashboard-block block2">
        <h3>Filtrer par genre et âge</h3>
        <GenderSelector onGenderChange={handleGenderChange} />
        <AgeRangeSelector onAgeChange={handleAgeChange} />
      </div>
      <div className="dashboard-block block3">Bloc 3</div>

      {/* Bloc 4 avec le graphique camembert */}
      <div className="dashboard-block block4">
        <h3>Nombre de grimpeurs par pays</h3>
        {error ? (
          <p>{error}</p>
        ) : chartData ? (
          <Pie data={chartData} />
        ) : (
          <p>Chargement des données...</p>
        )}
      </div>

      <div className="dashboard-block block5">Bloc 5</div>
      <div className="dashboard-block block6">Bloc 6</div>
      <div className="dashboard-block block7">Bloc 7</div>
    </div>
  );
}

// Configuration du Router
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
