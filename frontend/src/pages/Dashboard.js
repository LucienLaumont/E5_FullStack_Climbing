import React, { useState, useEffect } from 'react';
import AgeRangeSlider from '../components/AgeRangeSlider';
import { Pie, Scatter, Bar } from 'react-chartjs-2'; // Ajout de Bar
import axios from 'axios';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  PointElement,
  LinearScale,
  Title,
  BarElement, // Ajout de BarElement
  CategoryScale // Pour les barres
} from 'chart.js';
import '../styles/Dashboard.css';

// Enregistrement des composants Chart.js nécessaires pour le bar chart
ChartJS.register(ArcElement, Tooltip, Legend, PointElement, LinearScale, Title, BarElement, CategoryScale);

function Dashboard() {
  const [ageMax, setAgeMax] = useState(30);  // État pour l'âge max
  const [experienceData, setExperienceData] = useState({
    "0-2 ans": 0,
    "3-5 ans": 0,
    "6-10 ans": 0,
    "10+ ans": 0,
  });
  const [countryData, setCountryData] = useState({});
  const [scatterData, setScatterData] = useState([]); // État pour les données du scatter plot
  const [genderData, setGenderData] = useState({ male: 0, female: 0 }); // État pour les données du bar chart

  // Récupération des données du bar chart via l'API BarChart_Climbers_Genders
  useEffect(() => {
    const fetchGenderData = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/BarChart_Climbers_Genders?max_age=${ageMax}`);
        const data = response.data;
        setGenderData({ male: data["0"], female: data["1"] });
      } catch (error) {
        console.error('Erreur lors de la récupération des données du bar chart', error);
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

  useEffect(() => {
    const fetchScatterData = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/scatterGradesByAge?max_age=${ageMax}`);
        setScatterData(response.data);
      } catch (error) {
        console.error('Erreur lors de la récupération des données', error);
      }
    };

    fetchScatterData();
  }, [ageMax]);

  // Options pour la légende
  const legendOptions = {
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          boxWidth: 30,
          padding: 20,
          color: '#ffffff',
        },
      },
    },
  };

  // Configuration des données pour le bar chart (répartition par genre)
  const barChartData = {
    labels: ['Hommes', 'Femmes'],
    datasets: [
      {
        label: 'Répartition par genre',
        data: [genderData.male, genderData.female], // Utilisation des données récupérées
        backgroundColor: ['#8E412E', '#E6CEBC'], // Couleurs pour hommes et femmes
      }
    ]
  };

  const barChartOptions = {
    maintainAspectRatio: false,
    indexAxis: 'y',
    plugins: {
      legend: {
        display: false
      },
    },
    scales: {
      x: {
        ticks: {
          color: '#ffffff', // Couleur blanche pour les ticks sur l'axe X
        },
        grid: {
          color: '#ffffff33', // Lignes de la grille en blanc transparent
        }
      },
      y: {
        ticks: {
          color: '#ffffff', // Couleur blanche pour les ticks sur l'axe Y
        },
        grid: {
          color: '#ffffff33', // Lignes de la grille en blanc transparent
        }
      }
    }
  };  

  // Configuration des données pour le scatter plot
  const scatterPlotData = {
    datasets: [
      {
        label: 'Moyenne des Grades Max par Âge',
        data: scatterData.map(item => ({ x: item.age, y: item.average_grade_max })),
        backgroundColor: '#A2A182',
        borderColor: '#687259',
      }
    ]
  };

  const scatterOptions = {
    maintainAspectRatio: false, // Permet de forcer l'adaptation du scatter plot à la taille spécifiée
    scales: {
      x: {
        type: 'linear',
        position: 'bottom',
        title: {
          display: true,
          text: 'Âge',
          color: '#ffffff' // Définit la couleur du texte de l'axe des X en blanc
        },
        ticks: {
          color: '#ffffff' // Définit la couleur des ticks (graduations) sur l'axe des X en blanc
        },
        grid: {
          color: '#ffffff33' // Définit la couleur de la grille (ligne) de l'axe X en blanc semi-transparent
        }
      },
      y: {
        title: {
          display: true,
          text: 'Grades Max Moyens',
          color: '#ffffff' // Définit la couleur du texte de l'axe des Y en blanc
        },
        ticks: {
          color: '#ffffff' // Définit la couleur des ticks (graduations) sur l'axe des Y en blanc
        },
        grid: {
          color: '#ffffff33' // Définit la couleur de la grille (ligne) de l'axe Y en blanc semi-transparent
        }
      }
    },
    plugins: {
      legend: {
        display: false
      },
    }
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
        backgroundColor: ['#8E412E', '#BA6F4D', '#E6CEBC', '#A2A182'],
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
        backgroundColor: ['#8E412E', '#BA6F4D', '#E6CEBC', '#A2A182', '#687259','#F4ECE2'],
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
          <h3>Sélectionnez l'âge maximum : {ageMax}</h3>
          <div className="slider">
            <AgeRangeSlider setAgeMax={setAgeMax} />
          </div>
        </div>
      </div>

      {/* Première ligne : Pie charts et scatter plot */}
      <div className='line'>
        <div className="pie-charts-container">
          <div className="pie-chart-container">
            <h2>Années d'Expérience</h2>
            <Pie data={pieExperienceData} options={legendOptions} />
          </div>
          <div className="pie-chart-container">
            <h2>Pays</h2>
            <Pie data={pieCountryData} options={legendOptions} />
          </div>
        </div>

        <div className="scatter-plot-container">
          <div className='scatter-plot'>
            <h2>Moyenne des Grades Max par Âge</h2>
            <Scatter data={scatterPlotData} options={scatterOptions} />
          </div>
        </div>
      </div>

      {/* Deuxième ligne : Bar chart */}
      <div className='line'>
        <div className="bar-chart-container">
          <div className='bar-chart'>
            <h2>Répartition des Grimpeurs par Genre</h2>
            <Bar data={barChartData} options={barChartOptions} />
          </div>
        </div>
        <div className="source-link">
          <h2>Source</h2>
        </div>
      </div>
    </div>
  );
}
export default Dashboard;
