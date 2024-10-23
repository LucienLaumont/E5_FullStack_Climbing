import React, { useState } from 'react';

function AgeRangeSelector({ onAgeChange }) {
  const [minAge, setMinAge] = useState(18);
  const [maxAge, setMaxAge] = useState(60);

  const handleMinAgeChange = (event) => {
    const value = parseInt(event.target.value, 10);
    if (value <= maxAge) {
      setMinAge(value);
      onAgeChange(value, maxAge);
    }
  };

  const handleMaxAgeChange = (event) => {
    const value = parseInt(event.target.value, 10);
    if (value >= minAge) {
      setMaxAge(value);
      onAgeChange(minAge, value);
    }
  };

  return (
    <div className="age-range-selector">
      <label>Âge : {minAge} - {maxAge}</label>
      <div className="slider-container">
        <input
          type="range"
          min="18"
          max="100"
          value={minAge}
          onChange={handleMinAgeChange}
          className="slider slider-min"
        />
        <input
          type="range"
          min="18"
          max="100"
          value={maxAge}
          onChange={handleMaxAgeChange}
          className="slider slider-max"
        />
      </div>
    </div>
  );
}

export default AgeRangeSelector;