required_keys = {
        "category":{"GET": ["type", "id"],
                    "POST": ["type", "name"], 
                    "PUT": ["type", "name", "id"], 
                    "DELETE": ["type", "id"]},
        "topic": {  "GET": ["type", "id"],
                    "POST": ["type", "topic_type", "name", "category_id"], 
                    "PUT": ["type", "name", "id"], 
                    "DELETE": ["type", "id"]},
        "journal": {"GET": ["type", "id"],
                    "POST": ["type", "title", "content", "topic_id"], 
                    "PUT": ["type", "title", "content", "id"],
                    "DELETE": ["type", "id"]},
        "todo": {   "GET": ["type", "id"],
                    "POST": ["type", "task", "topic_id"], 
                    "PUT": ["type", "task", "completed", "id"], 
                    "DELETE": ["type", "id"]},
        "habit": {  "GET": ["type", "id"],
                    "POST": ["type", "name", "topic_id"],
                    "PUT": ["type", "name", "days_completed", "id"],
                    "DELETE": ["type", "id"]},
        "user": {   "GET": ["type", "id"],
                    "POST": ["type", "username", "email", "password"], 
                    "PUT": ["type", "username", "email", "password", "currentPassword"], 
                    "DELETE": ["type", "password"]},
        "tag": {    "GET": ["type", "id"],
                    "POST": ["type", "name"], 
                    "PUT": ["type", "name", "id"], 
                    "DELETE": ["type", "id"]},
        "token": {  "POST": ["type", "username", "password"]},       
        }

**password** 
Minimum of eight characters
Maximum of 100 characters
Minimum of one letter 
Minimum of one number