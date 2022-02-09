
/api/users

POST: create user
data: {"username": username, "email": email, "password": password}
email must be valid
password must be minimal 8 characters


/api/users/token
POST: get a JSON token
data: {"username": username, "password": password}

/api/entries
POST: create an entry
data: {"type": "entry_type", "name": name}


create user
# create: {"username": "username", "email": "email", "password": "password"}

update/delete user
# update: {"username": "username", "email": "email", "password": "password", "currentPassword": "currentPassword"}
# delete: {"password": "password"}

get token
# token: {"username": "username", "password": "password"}

# category
# fetch: {"type": "category"}
# create: {"type": "category", "name": "name"}
# update: {"type": "category", "name": "name", "id": "id"}
# delete: {"type": "category", "id": "id"}

# topic
# fetch {"type": "topic", "id": "id"}
# create: {"type": "topic", "topic_type": "topic_type", "name": "name", "category_id": "category_id"}
# update: {"type": "topic", "name": "name", "id": "id"}
# delete: {"type": "topic", "id": "id"}

# journal_entry
# fetch
# create: {"type": "journal", "title": "title", "content": "content", "topic_id": "topic_id"}
# update: {"type": "journal", "title": "title", "content": "content", "id": "id"}
# delete: {"type": "journal", "id": "id"}

# todo_entry
# fetch
# create: {"type": "todo", "title": "title", "due_date": "due_date", "topic_id": "topic_id"}
# update: {"type": "todo", "title": "title", "due_date": "due_date", "completed": "completed", "id": "id"}
# delete: {"type": "todo", "id": "id"}
