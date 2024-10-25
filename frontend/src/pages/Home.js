import React from 'react';
import { Link } from 'react-router-dom';
import climbingImage from '../assets/frontpage.png';
import '../styles/Home.css'; // Import du CSS

function Home() {
  return (
    <div className="App">
      <img className="full-screen-image" src={climbingImage} alt="Climbing App Frontpage" />
      <div className="overlay">
        <Link to="/dashboard" className="clickable-block">
          <h2>Dashboard</h2>
        </Link>
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

export default Home;
