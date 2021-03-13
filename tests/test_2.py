from requests import get, post

print(post('http://localhost:5000/api/add_job').json())

print(post('http://localhost:5000/api/add_job',
           json={'job': 'Название работы'}).json())

print(post('http://localhost:5000/api/add_job',
           json={'job': 'Название работы',
                 'work_size': 15,
                 'collaborators': '1,4',
                 'team_leader': 1,
                 'qwer': 'qffvqf'}).json())
