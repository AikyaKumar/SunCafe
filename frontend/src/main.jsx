import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import axios from 'axios';
import L from 'leaflet';
import sunIcon from '/public/sun.png';
import shadeIcon from '/public/shade.png';

// Define Leaflet icons
const sunLeafletIcon = new L.Icon({
  iconUrl: sunIcon,
  iconSize: [32, 32],
  iconAnchor: [16, 32]
});

const shadeLeafletIcon = new L.Icon({
  iconUrl: shadeIcon,
  iconSize: [32, 32],
  iconAnchor: [16, 32]
});

function App() {
  const [cafes, setCafes] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/cafes_with_sunlight')
      .then(response => setCafes(response.data))
      .catch(error => console.error('API error:', error));
  }, []);

  return (
    <MapContainer center={[49.3988, 8.6724]} zoom={15} style={{ height: '100vh', width: '100%' }}>
      <TileLayer
        attribution='&copy; OpenStreetMap'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {cafes.map((cafe, i) => (
        <Marker
          key={i}
          position={[cafe.latitude, cafe.longitude]}
          icon={cafe.has_sun ? sunLeafletIcon : shadeLeafletIcon}
        >
          <Popup>
            <b>{cafe.name}</b><br />
            Status: {cafe.has_sun ? "☀️ Sun" : "🌥️ Shade"}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default App;