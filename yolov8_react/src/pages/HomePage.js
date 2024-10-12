import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div>
      <h1>Welcome to the Main Page!</h1>
      <p>Click the link below to go to the Detection Page:</p>
      <div><Link to="/detection">Go to Detection Page</Link></div>
      <div><Link to="/segmentation">Go to Segmentation Page</Link></div>
    </div>
  );
}

export default HomePage;