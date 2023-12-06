# Orbital Simulator

## Opis

Orbital Simulator to prosty program symulujący trajektorię orbity satelitycznej wokół Ziemi. Program uwzględnia czynniki takie jak grawitacja, opór atmosferyczny, oraz perturbacje grawitacyjne od Księżyca i Słońca.

## Wymagania

- Python 3.x
- Flask
- Skyfield
- Numpy

## Instalacja

Sklonuj repozytorium:
   
    git clone https://github.com/twoj-uzytkownik/orbital-simulator.git

  Przejdź do katalogu projektu:


    cd orbital-simulator

Zainstaluj wymagane biblioteki:



    pip install -r requirements.txt

Uruchomienie

    python app.py

Aplikacja będzie dostępna pod adresem http://127.0.0.1:5000/ w przeglądarce.

Przewidywanie orbity:

Wyślij zapytanie POST na endpoint /predict_orbit.

    curl -X POST -H "Content-Type: application/json" -d '{
    "initial_position": [1.0, 0.0, 0.0],
    "initial_velocity": [0.0, 0.0, 7000.0],
    "time_steps": 100,
    "start_time": "2023-01-01T00:00:00",
    "time_delta_minutes": 1
    }' http://127.0.0.1:5000/predict_orbit

Oczekuj odpowiedzi w formie JSON z wynikami symulacji trajektorii orbity.