import React from 'react';
import './App.css';
import climbingImage from './assets/frontpage.png'; // Assure-toi que l'image soit dans le bon dossier

function App() {
  return (
    <div className="App">
      {/* Image de fond */}
      <img className="full-screen-image" src={climbingImage} alt="Climbing App Frontpage" />

      {/* Boutons superposés */}
      <div className="overlay">
        <a href="https://example.com/climbers" className="clickable-block">
          <h2>Dashboard</h2>
        </a>
        <a href="http://localhost:5000/docs" className="clickable-block">
          <h2>API</h2>
        </a>
        <a href="https://github.com/LucienLaumont" className="clickable-block">
          <h2>GitHub</h2>
        </a>
      </div>
    </div>
  );
}

export default App;
