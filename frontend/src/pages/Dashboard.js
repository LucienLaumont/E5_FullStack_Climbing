import React, { useState, useEffect } from 'react';
import AgeRangeSlider from '../components/AgeRangeSlider';
import { Pie } from 'react-chartjs-2';
import axios from 'axios';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js';
import '../styles/Dashboard.css';

ChartJS.register(ArcElement, Tooltip, Legend);

function Dashboard() {
  const [ageMax, setAgeMax] = useState(70);  // État pour l'âge max
  const [genderData, setGenderData] = useState({ male: 0, female: 0 });
  const [experienceData, setExperienceData] = useState({
    "0-2 ans": 0,
    "3-5 ans": 0,
    "6-10 ans": 0,
    "10+ ans": 0,
  });
  const [countryData, setCountryData] = useState({});

  useEffect(() => {
    const fetchGenderData = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/PieChart_Climbers_Genders?max_age=${ageMax}`);
        const data = response.data;
        setGenderData({ male: data["0"], female: data["1"] });
      } catch (error) {
        console.error('Erreur lors de la récupération des données', error);
      }
    };

    fetchGenderData();
  }, [ageMax]);

  useEffect(() => {
    const fetchExperienceData = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/PieChart_Climbers_Experience?max_age=${ageMax}`);
        const data = response.data;
        setExperienceData({
          "0-2 ans": data["0-2 ans"],
          "3-5 ans": data["3-5 ans"],
          "6-10 ans": data["6-10 ans"],
          "10+ ans": data["10+ ans"],
        });
      } catch (error) {
        console.error('Erreur lors de la récupération des données', error);
      }
    };

    fetchExperienceData();
  }, [ageMax]);

  useEffect(() => {
    const fetchCountryData = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/PieChart_Climbers_Countries?max_age=${ageMax}`);
        const data = response.data;
        setCountryData(data);
      } catch (error) {
        console.error('Erreur lors de la récupération des données', error);
      }
    };

    fetchCountryData();
  }, [ageMax]);

  // Options pour la légende
  const legendOptions = {
    plugins: {
      legend: {
        position: 'bottom', // Positionne la légende en bas
        labels: {
          boxWidth: 20, // Réduit la taille des carrés de légende
          padding: 20, // Réduit l'espace autour des labels dans la légende
        },
      },
    },
  };

  // Configuration des données pour les graphiques
  const pieGenderData = {
    labels: ['Hommes', 'Femmes'],
    datasets: [
      {
        label: 'Répartition des grimpeurs par genre',
        data: [genderData.male, genderData.female],
        backgroundColor: ['#36A2EB', '#FF6384'],
        hoverOffset: 4,
      },
    ],
  };

  const pieExperienceData = {
    labels: ['0-2 ans', '3-5 ans', '6-10 ans', '10+ ans'],
    datasets: [
      {
        label: 'Répartition par années d\'expérience',
        data: [
          experienceData["0-2 ans"],
          experienceData["3-5 ans"],
          experienceData["6-10 ans"],
          experienceData["10+ ans"],
        ],
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
        hoverOffset: 4,
      },
    ],
  };

  const pieCountryData = {
    labels: Object.keys(countryData),
    datasets: [
      {
        label: 'Répartition des grimpeurs par pays',
        data: Object.values(countryData),
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
        hoverOffset: 4,
      },
    ],
  };

  return (
    <div className="dashboard-container">
      {/* Bande avec le titre et le slider */}
      <div className="header-container">
        <h1 className="dashboard-title">Répartition des Grimpeurs</h1>
        <div className="slider-section">
          <h3>Sélectionnez l'âge maximum :</h3>
          <AgeRangeSlider setAgeMax={setAgeMax} />
          <span className="age-value">Âge maximum : {ageMax}</span>
        </div>
      </div>

      {/* Conteneur pour les graphiques */}
      <div className="pie-charts-container">
        <div className="pie-chart-container">
          <h2>Genre</h2>
          <Pie data={pieGenderData} options={legendOptions} />
        </div>
        <div className="pie-chart-container">
          <h2>Années d'Expérience</h2>
          <Pie data={pieExperienceData} options={legendOptions} />
        </div>
        <div className="pie-chart-container">
          <h2>Pays</h2>
          <Pie data={pieCountryData} options={legendOptions} />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
