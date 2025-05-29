import React, { useEffect, useState } from 'react';
import { fetchSunlight } from '../api/cafes';
import sunImg from '/sun.png';
import shadeImg from '/shade.png';

export default function CafeMap() {
  const [points, setPoints] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      fetchSunlight().then(setPoints);
    }, 60000); // refresh every 60 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      {points.map((p, idx) => (
        <div key={idx}>
          Lat: {p.location.lat}, Lon: {p.location.lon}
          <img src={p.sunlight === 'sunny' ? sunImg : shadeImg} width="20" />
        </div>
      ))}
    </div>
  );
}
