import React, { useState, useEffect } from 'react';

function App() {
  const [climbers, setClimbers] = useState([]);

  // Effectuer un appel à l'API pour récupérer la liste des grimpeurs
  useEffect(() => {
    fetch('http://localhost:5000/climbers/?skip=0&limit=10') // Assurez-vous que cette route existe dans votre API FastAPI
      .then(response => response.json())
      .then(data => setClimbers(data))
      .catch(error => console.error('Error fetching climbers:', error));
  }, []);

  return (
    <div className="App">
      <h1>Climbing Profiles</h1>
      <ul>
        {climbers.map(climber => (
          <li key={climber.user_id}>
            <strong>Country:</strong> {climber.country} <br />
            <strong>Sex:</strong> {climber.sex === 1 ? "Male" : "Female"} <br />
            <strong>Height:</strong> {climber.height} cm <br />
            <strong>Weight:</strong> {climber.weight} kg <br />
            <strong>Age:</strong> {climber.age} years <br />
            <strong>Years Climbing:</strong> {climber.years_cl} <br />
            <strong>First Climb Date:</strong> {new Date(climber.date_first).toLocaleDateString()} <br />
            <strong>Last Climb Date:</strong> {new Date(climber.date_last).toLocaleDateString()} <br />
            <strong>Grades Count:</strong> {climber.grades_count} <br />
            <strong>Grades First:</strong> {climber.grades_first} <br />
            <strong>Grades Last:</strong> {climber.grades_last} <br />
            <strong>Grades Max:</strong> {climber.grades_max} <br />
            <strong>Grades Mean:</strong> {climber.grades_mean.toFixed(2)} <br />
            <strong>First Climb Year:</strong> {climber.year_first} <br />
            <strong>Last Climb Year:</strong> {climber.year_last} <br />
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
