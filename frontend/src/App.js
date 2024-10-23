import React from 'react';
import GenderSelector from './GenderSelector';
import AgeRangeSelector from './AgeRangeSelector'; 
import './App.css';

import climbingImage from './assets/frontpage.png';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

// Tes pages individuelles
function Home() {
  return (
    <div className="App">
      <img className="full-screen-image" src={climbingImage} alt="Climbing App Frontpage" />
      <div className="overlay">
        {/* Le lien "Dashboard" utilise React Router pour la navigation interne */}
        <Link to="/dashboard" className="clickable-block">
          <h2>Dashboard</h2>
        </Link>
        {/* Les liens "API" et "GitHub" ouvrent des pages externes dans un nouvel onglet */}
        {/* En local remplacer http://localhost:5000/docs par http://127.0.0.1:8000/docs */}
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

function Dashboard() {
  const [gender, setGender] = useState('both');
  const [ageRange, setAgeRange] = useState({ min: 18, max: 60 });

  const handleGenderChange = (newGender) => {
    setGender(newGender);
    console.log("Gender selected:", newGender);
  };

  const handleAgeChange = (min, max) => {
    setAgeRange({ min, max });
    console.log("Age range selected:", min, "-", max);
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
      <div className="dashboard-block block4">Bloc 4</div>
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
