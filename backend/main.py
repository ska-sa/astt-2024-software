from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from classes.user import CreateUser, User
from classes.telescope import CreateTelescope, Telescope
from classes.reading import CreateReading, Reading
from classes.source import CreateSource, Source
from classes.command import CreateCommand, Command
from classes.position import CreatePosition, Position
from endpoints.users import get_users, post_user, get_user, auth_user, delete_user, update_user
from endpoints.telescopes import get_telescopes, post_telescope, get_telescope, delete_telescope, update_telescope
from endpoints.readings import get_reading, get_readings, post_reading, update_reading, delete_reading
from endpoints.sources import get_sources, post_source, get_source, delete_source, update_source
from endpoints.commands import get_commands, post_command, get_command, delete_command, update_command
from endpoints.positions import get_positions, post_position, get_position, delete_position, update_position
import uvicorn

BASE_URL = "/api/v1"
app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow cookies, authorization headers, etc.
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],     # Allow all headers
)

# curl -X GET -H "Content-Type: application/json" -d '{}' "http://127.0.0.1:8000/api/v1/users"
@app.get(f"{BASE_URL}/users", response_model=list[User])
def get_users_endpoint():
    return get_users()

# curl -X POST -H "Content-Type: application/json" -d '{"email_address": "ska@sarao.ac.za", "password": "hlabisa"}' "http://127.0.0.1:8000/api/v1/users"
@app.post(f"{BASE_URL}/users", response_model=User)
def post_users_endpoint(user: CreateUser):
    return post_user(user)

# curl -X GET -H "Content-Type: application/json" -d '{}' "http://127.0.0.1:8000/api/v1/users/1"
@app.get(f"{BASE_URL}/users/{{user_id}}", response_model=User)
def get_user_endpoint(user_id: int):
    return get_user(user_id)

# curl -X POST -H "Content-Type: application/json" -d '{"email_address": "test@git.com", "password": "test123"}' "http://127.0.1:8000/api/v1/users/auth"
@app.post(f"{BASE_URL}/users/auth", response_model=User)
def auth_user_endpoint(user: CreateUser):
    return auth_user(user)

# curl -X DELETE -H "Content-Type: application/json" -d '{}' "http://127.0.0.1:8000/api/v1/users/1"
@app.delete(f"{BASE_URL}/users/{{user_id}}", response_model=User)
def delete_user_endpoint(user_id: int):
    return delete_user(user_id)

# curl -X PUT -H "Content-Type: application/json" -d '{"email_address": "new@email.com", "password": "newpassword"}' "http://127.0.0.1:8000/api/v1/users/1"
@app.put(f"{BASE_URL}/users/{{user_id}}", response_model=User)
def update_user_endpoint(user_id: int, user: User):
    return update_user(user_id, user)

"""Telescope"""

# curl -X GET -H "Content-Type: application/json" -d '{}' "http://127.0.0.1:8000/api/v1/telescopes"
@app.get(f"{BASE_URL}/telescopes", response_model=list[Telescope])
def get_telescopes_endpoint():
    return get_telescopes()

# curl -X POST -H "Content-Type: application/json" -d '{"email_address": "ska@sarao.ac.za", "password": "hlabisa"}' "http://127.0.0.1:8000/api/v1/telescopes"
@app.post(f"{BASE_URL}/telescopes", response_model=Telescope)
def post_telescopes_endpoint(telescope: CreateTelescope):
    return post_telescope(telescope)

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
def update_telescope_endpoint(telescope_id: int, telescope: Telescope):
    return update_telescope(telescope_id, telescope)

"""Reading"""

# curl -X GET -H "Content-Type: application/json" -d '{}' "http://127.0.0.1:8000/api/v1/readings"
@app.get(f"{BASE_URL}/readings", response_model=list[Reading])
def get_readings_endpoint():
    return get_readings()

# curl -X POST -H "Content-Type: application/json" -d '{"email_address": "ska@sarao.ac.za", "password": "hlabisa"}' "http://127.0.0.1:8000/api/v1/telescopes"
@app.post(f"{BASE_URL}/readings", response_model=Reading)
def post_readings_endpoint(reading: CreateReading):
    return post_reading(reading)

# curl -X GET -H "Content-Type: application/json" -d '{}' "http://127.0.0.1:8000/api/v1/readings/1"
@app.get(f"{BASE_URL}/readings/{{telescope_id}}", response_model=Reading)
def get_reading_endpoint(id: int):
    return get_reading(id)

# curl -X DELETE -H "Content-Type: application/json" -d '{}' "http://127.0.0.1:8000/api/v1/readings/1"
@app.delete(f"{BASE_URL}/readings/{{telescope_id}}", response_model=Reading)
def delete_reading_endpoint(id: int):
    return delete_reading(id)

# curl -X PUT -H "Content-Type: application/json" -d '{"email_address": "new@email.com", "password": "newpassword"}' "http://127.0.0.1:8000/api/v1/telescopes/1"
@app.put(f"{BASE_URL}/readings/{{telescope_id}}", response_model=Reading)
def update_reading_endpoint(id: int, telescope: Reading):
    return update_reading(id, telescope)

"""Source"""

@app.get(f"{BASE_URL}/sources", response_model=list[Source])
def get_sources_endpoint():
    return get_sources()

@app.post(f"{BASE_URL}/sources", response_model=Source)
def post_source_endpoint(source: CreateSource):
    return post_source(source)

@app.get(f"{BASE_URL}/sources/{{source_id}}", response_model=Source)
def get_source_endpoint(source_id: int):
    return get_source(source_id)

@app.delete(f"{BASE_URL}/sources/{{source_id}}", response_model=Source)
def delete_source_endpoint(source_id: int):
    return delete_source(source_id)

@app.put(f"{BASE_URL}/sources/{{source_id}}", response_model=Source)
def update_source_endpoint(source_id: int, source: Source):
    return update_source(source_id, source)

"""Command"""

@app.get(f"{BASE_URL}/commands", response_model=list[Command])
def get_commands_endpoint():
    return get_commands()

@app.post(f"{BASE_URL}/commands", response_model=Command)
def post_command_endpoint(command: CreateCommand):
    return post_command(command)

@app.get(f"{BASE_URL}/commands/{{command_id}}", response_model=Command)
def get_command_endpoint(command_id: int):
    return get_command(command_id)

@app.delete(f"{BASE_URL}/commands/{{command_id}}", response_model=Command)
def delete_command_endpoint(command_id: int):
    return delete_command(command_id)

@app.put(f"{BASE_URL}/commands/{{command_id}}", response_model=Command)
def update_command_endpoint(command_id: int, command: Command):
    return update_command(command_id, command)

"""Position"""

@app.get(f"{BASE_URL}/positions", response_model=list[Position])
def get_positions_endpoint():
    return get_positions()

@app.post(f"{BASE_URL}/positions", response_model=Position)
def post_position_endpoint(position: CreatePosition):
    return post_position(position)

@app.get(f"{BASE_URL}/positions/{{position_id}}", response_model=Position)
def get_position_endpoint(position_id: int):
    return get_position(position_id)

@app.delete(f"{BASE_URL}/positions/{{position_id}}", response_model=Position)
def delete_position_endpoint(position_id: int):
    return delete_position(position_id)

@app.put(f"{BASE_URL}/positions/{{position_id}}", response_model=Position)
def update_position_endpoint(position_id: int, position: Position):
    return update_position(position_id, position)


def main() -> None:
    uvicorn.run("main:app", host='127.0.0.1', port=8000, workers=2, reload=True)
    #uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()