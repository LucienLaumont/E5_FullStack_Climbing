import React, { useState } from 'react';

function GenderSelector({ onGenderChange }) {
  const [gender, setGender] = useState('both');

  const handleGenderChange = (event) => {
    setGender(event.target.value);
    onGenderChange(event.target.value); // Informe le parent du changement
  };

  return (
    <div>
      <label>
        <input 
          type="radio" 
          value="male" 
          checked={gender === 'male'} 
          onChange={handleGenderChange} 
        />
        Homme
      </label>
      <label>
        <input 
          type="radio" 
          value="female" 
          checked={gender === 'female'} 
          onChange={handleGenderChange} 
        />
        Femme
      </label>
      <label>
        <input 
          type="radio" 
          value="both" 
          checked={gender === 'both'} 
          onChange={handleGenderChange} 
        />
        Tous
      </label>
    </div>
  );
}

export default GenderSelector;
