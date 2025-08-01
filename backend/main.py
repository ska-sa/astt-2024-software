from fastapi import FastAPI, HTTPException
from classes.user import User
from classes.telescope import Telescope
from endpoints.users import get_users, post_user, get_user, delete_user, update_user
from endpoints.telescopes import get_telescopes, post_telescope, get_telescope, delete_telescope, update_telescope
import uvicorn

BASE_URL = "/api/v1"
app = FastAPI()

# curl -X GET -H "Content-Type: application/json" -d '{}' "http://127.0.0.1:8000/api/v1/users"
@app.get(f"{BASE_URL}/users", response_model=list[User])
def get_users_endpoint():
    return get_users()

# curl -X POST -H "Content-Type: application/json" -d '{"email_address": "ska@sarao.ac.za", "password": "hlabisa"}' "http://127.0.0.1:8000/api/v1/users"
@app.post(f"{BASE_URL}/users", response_model=User)
def post_users_endpoint(user_dict: dict):
    return post_user(user_dict)

# curl -X GET -H "Content-Type: application/json" -d '{}' "http://127.0.0.1:8000/api/v1/users/1"
@app.get(f"{BASE_URL}/users/{{user_id}}", response_model=User)
def get_user_endpoint(user_id: int):
    return get_user(user_id)

# curl -X DELETE -H "Content-Type: application/json" -d '{}' "http://127.0.0.1:8000/api/v1/users/1"
@app.delete(f"{BASE_URL}/users/{{user_id}}", response_model=User)
def delete_user_endpoint(user_id: int):
    return delete_user(user_id)

# curl -X PUT -H "Content-Type: application/json" -d '{"email_address": "new@email.com", "password": "newpassword"}' "http://127.0.0.1:8000/api/v1/users/1"
@app.put(f"{BASE_URL}/users/{{user_id}}", response_model=User)
def update_user_endpoint(user_id: int, user_dict: dict):
    return update_user(user_id, user_dict)

"""Telescope"""

# curl -X GET -H "Content-Type: application/json" -d '{}' "http://127.0.0.1:8000/api/v1/telescopes"
@app.get(f"{BASE_URL}/telescopes", response_model=list[Telescope])
def get_telescopes_endpoint():
    return get_telescopes()

# curl -X POST -H "Content-Type: application/json" -d '{"email_address": "ska@sarao.ac.za", "password": "hlabisa"}' "http://127.0.0.1:8000/api/v1/telescopes"
@app.post(f"{BASE_URL}/telescopes", response_model=Telescope)
def post_telescopes_endpoint(telescope_dict: dict):
    return post_telescope(telescope_dict)

# curl -X GET -H "Content-Type: application/json" -d '{}' "http://127.0.0.1:8000/api/v1/telescopes/1"
@app.get(f"{BASE_URL}/telescopes/{{telescope_id}}", response_model=Telescope)
def get_telescope_endpoint(telescope_id: int):
    return get_telescope(telescope_id)

# curl -X DELETE -H "Content-Type: application/json" -d '{}' "http://127.0.0.1:8000/api/v1/telescopes/1"
@app.delete(f"{BASE_URL}/telescopes/{{telescope_id}}", response_model=Telescope)
def delete_telescope_endpoint(telescope_id: int):
    return delete_telescope(telescope_id)

# curl -X PUT -H "Content-Type: application/json" -d '{"email_address": "new@email.com", "password": "newpassword"}' "http://127.0.0.1:8000/api/v1/telescopes/1"
@app.put(f"{BASE_URL}/telescopes/{{telescope_id}}", response_model=Telescope)
def update_telescope_endpoint(telescope_id: int, telescope_dict: dict):
    return update_telescope(telescope_id, telescope_dict)

def main() -> None:
    uvicorn.run("main:app", host='127.0.0.1', port=8000, workers=2, reload=True)
    #uvicorn.run(app, host="127.0.0.1", port=8000)
#anywhere
if __name__ == "__main__":

    main()