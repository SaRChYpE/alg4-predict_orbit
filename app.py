from flask import Flask, request, jsonify
from skyfield.api import load, Topos, utc
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)

#funkcja która przy pomocy skyfield api określa położenie księzyca oraz słońca. Obserwator ustawiony na ziemi.
def get_moon_and_sun_positions(time):
    eph = load('de421.bsp')
    observer = Topos(latitude_degrees=0, longitude_degrees=0)

    ts = load.timescale()
    t = ts.utc(time)

    observer_at_time = eph['earth'] + observer
    moon_position = observer_at_time.at(t).observe(eph['moon']).apparent().position.km
    sun_position = observer_at_time.at(t).observe(eph['sun']).apparent().position.km

    return moon_position, sun_position #Zwracane są wektory pozycji Księzyca i Słońca

#funkcja która symuluje orbitę satelity
def simulate_orbit(initial_position, initial_velocity, start_time, time_steps, time_delta):
    G = 6.674 * (10 ** -11)
    M_earth = 5.972 * (10 ** 24)
    atmospheric_density = 1.2

    delta_t = 1.0
    positions = [initial_position]
    velocities = [initial_velocity]

    current_time = start_time
    for _ in range(time_steps):
        r = np.linalg.norm(positions[-1])
        gravitational_force_earth = -G * M_earth / r ** 3 * positions[-1]

        velocity = velocities[-1]
        speed = np.linalg.norm(velocity)
        atmospheric_force = -0.5 * atmospheric_density * speed ** 2 * velocity / speed

        #Uwzględnienie perturbacji grawitacyjnych od Księżyca i Słońca
        moon_position, sun_position = get_moon_and_sun_positions(current_time)
        gravitational_force_moon = -G * M_earth / np.linalg.norm(moon_position - positions[-1]) ** 3 * (
                moon_position - positions[-1])
        gravitational_force_sun = -G * M_earth / np.linalg.norm(sun_position - positions[-1]) ** 3 * (
                sun_position - positions[-1])

        gravitational_force = gravitational_force_earth + gravitational_force_moon + gravitational_force_sun

        acceleration = (gravitational_force + atmospheric_force) / M_earth
        new_velocity = velocities[-1] + acceleration * delta_t
        new_position = positions[-1] + new_velocity * delta_t

        positions.append(new_position)
        velocities.append(new_velocity)

        #Aktualizacja czasu na podstawie czasu delta
        current_time += time_delta

    return np.array(positions) #Zwracane jest tablica z kolejnymi pozycjami satelity w trakcie symulacji


@app.route('/predict_orbit', methods=['POST'])
def predict_orbit():
    try:
        data = request.get_json()

        initial_position = np.array(data['initial_position'])
        initial_velocity = np.array(data['initial_velocity'])
        time_steps = data['time_steps']

        start_time_str = data.get('start_time', '2023-01-01T00:00:00')  #Jeśli start_time nie zostanie podany wtedy jest przypisana domyślna wartość
        start_time = datetime.fromisoformat(start_time_str).replace(tzinfo=utc)

        time_delta_minutes = data.get('time_delta_minutes', 1) #Jeśli time_delta nie zostanie podany wtedy jest przypisana domyślna wartość
        time_delta = timedelta(minutes=time_delta_minutes)

        orbit_positions = simulate_orbit(initial_position, initial_velocity, start_time, time_steps, time_delta)

        return jsonify({'orbit_positions': orbit_positions.tolist()}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
