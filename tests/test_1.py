from requests import get

print(get('http://127.0.0.1:5000/api/jobs').json())
print(get('http://127.0.0.1:5000/api/jobs/3').json())
print(get('http://127.0.0.1:5000/api/jobs/77777777').json())
print(get('http://127.0.0.1:5000/api/jobs/qbfd').json())
