import React, { useState } from 'react';
import { Link } from 'react-router-dom';  // Import Link from React Router

function DetectionPage() {
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);  // For image preview
  const [result, setResult] = useState('');
  const [detectedImage, setDetectedImage] = useState('');
  const [error, setError] = useState('');

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setImagePreview(URL.createObjectURL(file)); // Preview selected image
      setError('');  // Clear any previous errors
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!image) {
      setError('Please select an image to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('image', image);

    try {
      // Send the image to the backend for detection
      const response = await fetch('http://localhost:5000/api/detection/', {
        method: 'POST',
        body: formData,
      });
      console.error(response);  // Add console logging

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setResult(data.result);
      setDetectedImage(data.image);  // Base64 image returned from the server
    } catch (error) {
      console.error('Error during detection:', error);  // Add console logging
      setError('Error during detection: ' + error.message);
    }
  };

  return (
    <div>
      <Link to="/">Return to Home</Link>
      <h1>Detection</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleImageChange} />
        {imagePreview && (
          <div>
            <h2>Image Preview:</h2>
            <img src={imagePreview} alt="Selected" style={{ width: '300px' }} />
          </div>
        )}
        <button type="submit">Submit</button>
      </form>

      {result && <h2>Detection Result: {result}</h2>}
      {detectedImage && (
        <div>
          <img src={`data:image/jpeg;base64,${detectedImage}`} alt="Processed" />
        </div>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default DetectionPage;