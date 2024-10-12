import React, { useState } from 'react';

function SegmentationPage() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState('');

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('image', image);

    // Send the image to the backend for segmentation
    const response = await fetch('http://localhost:8000/segmentation/', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    setResult(data.result);
  };

  return (
    <div>
      <h1>Segmentation</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleImageChange} />
        <button type="submit">Submit</button>
      </form>
      {result && <p>Segmentation Result: {result}</p>}
    </div>
  );
}

export default SegmentationPage;