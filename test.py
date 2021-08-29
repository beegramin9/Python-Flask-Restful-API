import requests

BASE = "http://127.0.0.1:5000/"

data = [{
    "likes": 78,
    "name": "Joe",
    "views": 100
}, {
    "likes": 10000,
    "name": "How to make Rest Api",
    "views": 80000
}, {
    "likes": 35,
    "name": "Tim",
    "views": 2000
}]

""" Post request """
print('Create Data')
for i in range(len(data)):
    response = requests.post(BASE + 'video/' + str(i), data[i])
    print(response.json())


""" Get request """
print('Read Data')
for i in range(len(data)):
    response = requests.get(BASE + 'video/' + str(i))
    print(response.json())

updated_data = [{
    "likes": 78,
    "name": "John Doe",
    "views": 100
}, {
    "likes": 20000,
    "name": "How to make Rest Api",
    "views": 180000
}, {
    "likes": 64,
    "name": "Tim Cicada",
    "views": 2000
}]

""" Patch request """
print('Updated Data')
for i in range(len(updated_data)):
    response = requests.patch(BASE + 'video/' + str(i), updated_data[i])
    print(response.json())
    
""" Delete request """
print('Deleted Data')
for i in range(len(data)):
    response = requests.delete(BASE + 'video/' + str(i))
    print("Successfully deleted")
    # delete는 따로 object를 return하지 않으므로 jsonify 하지 않는다.
    print(response)

""" is Data deteted? """
print('is Data deteted?')
for i in range(len(data)):
    response = requests.get(BASE + 'video/' + str(i))
    print(response.json())