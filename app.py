from flask import Flask, render_template
import googlemaps

app = Flask(__name__)
app.static_folder = 'static'

API = open("api.txt", "r")
APIKey = API.read()
Maps = googlemaps.Client(key = APIKey)

A = "ул. Налибокская 14, Город Минск"
B = "ул. Чкалова, Город Витебск" 

geocode_result1 = Maps.geocode(A)
geocode_result2 = Maps.geocode(B)

if geocode_result1 and geocode_result2:
    lat1 = geocode_result1[0]['geometry']['location']['lat']
    lng1 = geocode_result1[0]['geometry']['location']['lng']
    geo1 = f"Latitude: {lat1}, Longitude: {lng1}"
    
    lat2 = geocode_result2[0]['geometry']['location']['lat']
    lng2 = geocode_result2[0]['geometry']['location']['lng']
    geo2 = f"Latitude: {lat2}, Longitude: {lng2}"
else:
    print("error geo")   
    
#----------------------------------------- 
Distance1 = Maps.directions(A, B, "driving")
Distance2 = Maps.directions(A, B, "walking")
Distance3 = Maps.directions(A, B, "bicycling")
Distance4 = Maps.directions(A, B, "transit")

if Distance1 and 'legs' in Distance1[0] and 'distance' in Distance1[0]['legs'][0] and 'text' in Distance1[0]['legs'][0]['distance']:
    driving_distance = Distance1[0]['legs'][0]['distance']['text'].split()[0] + ' km'
    HrsMinsDurationDriving = Distance1[0]['legs'][0]['duration']['text']
else:
    driving_distance = "Недоступно"
    HrsMinsDurationDriving = "Недоступно"       
print(f"Машина: {driving_distance} km, time: {HrsMinsDurationDriving}")

if Distance2 and 'legs' in Distance2[0] and 'distance' in Distance2[0]['legs'][0] and 'text' in Distance2[0]['legs'][0]['distance']:
    walking_distance = Distance2[0]['legs'][0]['distance']['text'].split()[0] + ' km'
    HrsMinsDurationWalking = Distance2[0]['legs'][0]['duration']['text']
else:
    walking_distance = "Недоступно"
    HrsMinsDurationWalking = "Недоступно"
print(f"Пешком: {walking_distance} km, time: {HrsMinsDurationWalking}")

if Distance3 and 'legs' in Distance3[0] and 'distance' in Distance3[0]['legs'][0] and 'value' in Distance3[0]['legs'][0]['distance']:
    bicycling_distance = Distance3[0]['legs'][0]['distance']['value'] + ' km'
    HrsMinsDurationBicycling = Distance3[0]['legs'][0]['duration']['text']
else:
    bicycling_distance = "Недоступно"
    HrsMinsDurationBicycling = "Недоступно"
print(f"Велик: {bicycling_distance / 1000 if isinstance(bicycling_distance, int) else bicycling_distance} km, time: {HrsMinsDurationBicycling}")

if Distance4 and 'legs' in Distance4[0] and 'distance' in Distance4[0]['legs'][0] and 'text' in Distance4[0]['legs'][0]['distance']:
    transit_distance = Distance4[0]['legs'][0]['distance']['text'].split()[0] + ' km'
    HrsMinsDurationTransit = Distance4[0]['legs'][0]['duration']['text']
else:
    transit_distance = "Недоступно"
    HrsMinsDurationTransit = "Недоступно"
print(f"Общественный транспорт: {transit_distance} km, time: {HrsMinsDurationTransit}")
#-----------------------------------------

@app.route('/')
def map():
    api_key = APIKey
    origin = {'lat': lat1, 'lng': lng1}
    destination = {'lat': lat2, 'lng': lng2}
    return render_template('karta.html', api_key=api_key, origin=origin,  destination=destination, A=A, B=B, driving_distance=driving_distance, walking_distance=walking_distance, bicycling_distance=bicycling_distance, transit_distance=transit_distance, HrsMinsDurationDriving=HrsMinsDurationDriving, HrsMinsDurationWalking=HrsMinsDurationWalking, HrsMinsDurationBicycling= HrsMinsDurationBicycling, HrsMinsDurationTransit=HrsMinsDurationTransit )

if __name__ == '__main__':
    app.run(debug=True)
