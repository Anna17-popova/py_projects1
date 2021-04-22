import requests

request = "https://static-maps.yandex.ru/1.x/?z=16&l=map&pt=37.529471,55.822910,pm2rdl"
response = requests.get(request)
if not response:
    print("Ошибка выполнения запроса:")
    print(request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
with open('./static/img/geo.jpg', 'wb') as file:
    file.write(response.content)
