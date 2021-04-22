from requests import post, get, delete

#print(get('http://localhost:8065/api/users').json())
print(get('http://localhost:8065/api/products').json())
print(get('http://localhost:8065/api/products/3').json())
print(post('http://localhost:8065/api/products', json={'name': 'Товар3', 'price': '1000р', 'text': '-'}).json())
print(delete('http://localhost:8065/api/products/1').json())
#print(get('http://localhost:8065/api/users/3').json())
#пользователя с id 999 нет в базе данных
#print(get('http://localhost:8065/api/users/999').json())
#пустой запрос
#print(post('http://localhost:8065/api/users').json())
#запрос с недостаточным количеством параметров
#print(post('http://localhost:8065/api/users', json={'name': 'Anna', 'surname': 'Popova'}).json())
#корректный запрос
#print(post('http://localhost:8065/api/users', json={'name': 'Harry', 'surname': 'Potter',
#                                                    'sity': 'London', 'email': '123@mars.tru', 'age': '11'}).json())
#пользователя с id 999 нет в базе данных
#print(delete('http://localhost:8065/api/users/999').json())
#print(delete('http://localhost:8065/api/users/1').json())
