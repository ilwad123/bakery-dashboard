 // Initialize the map and set it to Bristol
 const map = L.map('map').setView([51.455084, -2.591765], 13); // Centered on Bristol City Centre

 // Add OpenStreetMap tiles
 L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
 }).addTo(map);

 // Define locations
 const locations = {
     'City Centre': [51.455084, -2.591765],
     'Clifton': [51.455280, -2.619340],
     'Cotham': [51.464000, -2.598000],
     'Montpelier': [51.468000, -2.589000],
     'Stokes Croft': [51.462000, -2.590000],
     'Gloucester Road': [51.476000, -2.592000],
     'Bedminster': [51.440000, -2.600000],
     'Southville': [51.442000, -2.606000],
     'Easton': [51.463000, -2.561000],
     'St George': [51.464000, -2.548000],
     'Barton Hill': [51.454000, -2.570000],
     'Lawrence Hill': [51.457000, -2.574000],
     'Redfield': [51.459000, -2.558000],
     'Totterdown': [51.442000, -2.576000],
     'Kingsdown': [51.462000, -2.598000],
     'Ashley Down': [51.478000, -2.583000],
     'Old Market': [51.456000, -2.582000],
     'Brislington': [51.441000, -2.535000]
 };

 const customIcon = L.icon({
    iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
    iconSize: [48, 48], // Make the icon bigger
    iconAnchor: [24, 48], // So it points properly
    popupAnchor: [0, -40] // Adjust popup position if needed
});

for (const [name, coords] of Object.entries(locations)) {
    L.marker(coords, { icon: customIcon }).addTo(map)
        .bindPopup(`<b>${name}</b>`);
}

//  // Add markers for each location
//  for (const [name, coords] of Object.entries(locations)) {
//      L.marker(coords).addTo(map)
//          .bindPopup(`<b>${name}</b>`) // Popup displays location name
//          .openPopup();
//  }
const mapTitle = L.control({ position: 'topcenter' });

mapTitle.onAdd = function () {
    const div = L.DomUtil.create('div', 'map-title');
    div.innerHTML = '<h2>Bristol Map with Markers</h2>'; // Add your title here
    return div;
};

mapTitle.addTo(map);

