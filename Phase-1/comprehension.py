users = [
    {"name": "Ali", "age": 17, "email": "ali@x.com"},
    {"name": "Ayşe", "age": 25},
    {"name": "Mehmet", "age": 30, "email": "mehmet@x.com"},
]

adult_users = [user["name"] for user in users if user["age"] >= 18]

print(adult_users)

generate_list = [f"{user['name']}: {user.get('email', 'email yok')}" for user in users]

print(generate_list)

ages = {user["name"]: user['age'] for user in users}

print(ages)

emails = {user['name']: user['email'] for user in users if user.get('email')}

print(emails)