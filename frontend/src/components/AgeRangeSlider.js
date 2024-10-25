import React, { useState } from 'react';
import '../styles/AgeRangeSlider.css'; // Assurez-vous que le chemin est correct

function AgeRangeSlider({ setAgeMax }) {
  const [ageMax, setLocalAgeMax] = useState(70);

  const handleMaxChange = (event) => {
    const value = Number(event.target.value);
    setLocalAgeMax(value);
    setAgeMax(value);  // Met à jour l'état dans le composant parent (Dashboard)
  };

  return (
    <div className="age-range-slider">
      <div className="slider-container">
        <input
          type="range"
          min="12"
          max="70"
          value={ageMax}
          onChange={handleMaxChange}
          className="slider"
        />
      </div>
    </div>
  );
}

export default AgeRangeSlider;
