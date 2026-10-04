import folium
from sgp4.api import Satrec
from astropy import coordinates as coord
from astropy import units as u
from astropy.time import Time
from src.ingestion.load_tle import load_tle

lines = load_tle("data/raw/iss.txt")

# The first line is the satellite name
# The next two the orbital data
line1 = lines[1].strip()
line2 = lines[2].strip()

# Create a satellite object from the TLE
satellite = Satrec.twoline2rv(line1, line2)

# Get current UTC time instead of fixed TLE epoch
now = Time.now()

# Propagate orbit at current time using SGP4
error, position, velocity = satellite.sgp4(now.jd1, now.jd2)

# Check if SGP4 propagation succeeded
if error == 0:
    # TEME position (coordinates frame used by SGP4)
    teme = coord.TEME(
        x=position[0] * u.km,
        y=position[1] * u.km,
        z=position[2] * u.km,
        obstime=now
    )

    # Earth coordinates
    itrs = teme.transform_to(coord.ITRS(obstime=teme.obstime))

    # Convert Earth coordinates to Latitude, Longitude, Altitude
    location = coord.EarthLocation.from_geocentric(
        itrs.x, itrs.y, itrs.z
    )

    lat = location.lat.deg
    lon = location.lon.deg
    alt = location.height.to(u.km).value

    # Print results
    print(f"Time (UTC): {now.iso}")
    print(f"Latitude:   {location.lat.deg:.4f}°")
    print(f"Longitude:  {location.lon.deg:.4f}°")
    print(f"Altitude:   {location.height.to(u.km):.2f} km")

    # Create interactive world map centered on ISS position
    iss_map = folium.Map(
        location=[lat, lon], 
        zoom_start=3, 
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri"
    )

    folium.Marker(
        location=[lat, lon],
        popup=f"ISS Position<br>Lat: {lat:.2f}<br>Lon: {lon:.2f}<br>Alt: {alt:.0f} km",
        tooltip="ISS Current Location",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(iss_map)

    iss_map.save("iss_location.html")
    print("Map successfully saved")

else:
    print(f"Error in SGP4 calculation: code {error}")
