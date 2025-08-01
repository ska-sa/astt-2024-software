from fastapi import HTTPException
from classes.telescope import Telescope
from datetime import datetime
from classes import Database

table_name: str = 'telescope'
datetime_format_str: str = '%Y-%m-%d %H:%M:%S'

def get_telescopes() -> list[Telescope]:
    # Read telescopes from db
    db = Database()
    _, db_select_telescope_outputs = db.read(table_name)
    telescopes = []
    for db_select_telescope_output in db_select_telescope_outputs:
        id, name, health_status, created_at = db_select_telescope_output
        telescopes.append(Telescope(id=int(id), name=str(name), health_status=str(health_status), created_at=datetime.strptime(str(created_at), datetime_format_str)))

    return telescopes

def post_telescope(telescope_dict: dict) -> Telescope:
    # Insert new telescope data
    db = Database()
    _, _ = db.insert(table_name, telescope_dict)

    # Read newly inserted telescope from db
    _, db_select_telescope_outputs = db.read(table_name, criteria=telescope_dict)
    id, name, health_status, created_at = db_select_telescope_outputs[-1]

    return Telescope(id=int(id), name=str(name), health_status=str(health_status), created_at=datetime.strptime(str(created_at), datetime_format_str))

def get_telescope(telescope_id: int) -> Telescope:
    # Read telescope from db by id
    db = Database()
    _, db_select_telescope_outputs = db.read(table_name, criteria={'id': telescope_id})
    if db_select_telescope_outputs:
        id, name, health_status, created_at = db_select_telescope_outputs[0]
        return Telescope(id=int(id), name=str(name), health_status=str(health_status), created_at=datetime.strptime(str(created_at), datetime_format_str))
    else:
        return None

def delete_telescope(telescope_id: int) -> Telescope:
    # Delete telescope from db by id
    db = Database()
    _, db_select_telescope_outputs = db.read(table_name, criteria={'id': telescope_id})
    if db_select_telescope_outputs:
        id, name, health_status, created_at= db_select_telescope_outputs[0]
        telescope = Telescope(id=int(id), name=str(name), health_status=str(health_status), created_at=datetime.strptime(str(created_at), datetime_format_str))
        success, _ = db.delete(table_name, criteria={'id': telescope_id})
        if success:
            return telescope
        else:
            raise HTTPException(status_code=500, detail="Failed to delete telescope.")
    else:
        raise HTTPException(status_code=404, detail=f"Telescope with ID {telescope_id} not found.")

def update_telescope(telescope_id: int, telescope_dict: dict) -> Telescope:
    # Update telescope in db by id
    db = Database()
    success, _ = db.update(table_name, criteria={'id': telescope_id}, data=telescope_dict)
    if success:
        _, db_select_telescope_outputs = db.read(table_name, criteria={'id': telescope_id})
        id, name, health_status, created_at = db_select_telescope_outputs[0]
        return Telescope(id=int(id), name=str(name), health_status=str(health_status), created_at=datetime.strptime(str(created_at), datetime_format_str))
    else:
        return None