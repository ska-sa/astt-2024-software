from fastapi import FastAPI, HTTPException
from classes.user import User
from endpoints.users import get_users, post_user
import uvicorn

BASE_URL = "/api/v1"
app = FastAPI()

# curl -X GET -H "Content-Type: application/json" -d '{}' "http://127.0.0.1:8000/api/v1/users"
@app.get(f"{BASE_URL}/users", response_model=list[User])
def get_users_endpoint():
    return get_users()

# curl -X POST -H "Content-Type: application/json" -d '{"email_address": "shlabisa@sarao.ac.za", "password": "hlabisa"}' "http://127.0.0.1:8000/api/v1/users"
@app.post(f"{BASE_URL}/users", response_model=User)
def post_users_endpoint(user_dict: dict):
    return post_user(user_dict)

def main() -> None:
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
if __name__ == "__main__":
    main()