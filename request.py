import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json={'xG':30, 'xGA':22, 'pts':30})

print(r.json())