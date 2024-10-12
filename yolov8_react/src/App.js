import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";

import HomePage from './pages/HomePage';
import DetectionPage from './pages/DetectionPage';
import SegmentationPage from './pages/SegmentationPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />  {/* Home route */}
        <Route path="/detection" element={<DetectionPage />} />
        <Route path="/segmentation" element={<SegmentationPage />} />
      </Routes>
    </Router>
  );
}

export default App;
