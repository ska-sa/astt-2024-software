from fastapi import HTTPException
from classes.reading import CreateReading, Reading
from datetime import datetime
from classes import Database

table_name: str = 'reading'

def get_reading(reading_id: int) -> Reading:
    db = Database()
    _,db_select_reading_outputs = db.read(table_name, criteria={'id': reading_id})
    if db_select_reading_outputs:
        id, telescope_id, az_angle, el_angle, health_status, movement_status, created_at =db_select_reading_outputs[0]
        return Reading(id=int(id),telescope_id=int(telescope_id),az_angle=float(az_angle), el_angle=float(el_angle),health_status=str(health_status),
                       movement_status=str(movement_status), created_at=datetime.fromisoformat(str(created_at)))
    else:
        return None
    
def get_readings() -> list[Reading]:
    db = Database()
    _, db_select_reading_outputs = db.read(table_name)
    readings =[]
    for db_select_reading_output in db_select_reading_outputs:
        id, telescope_id, az_angle, el_angle, health_status, movement_status, created_at = db_select_reading_output
        readings.append(Reading(id=int(id), telescope_id=int(telescope_id), az_angle=float(az_angle), el_angle=float(el_angle),health_status=str(health_status),
                                movement_status=str(movement_status), created_at=datetime.fromisoformat(str(created_at))))
    return readings
def  get_latest_reading(telescope_id: int) -> Reading:
    db = Database()
    _, db_select_reading_outputs = db.read(table_name, criteria={'telescope_id': telescope_id})
    if db_select_reading_outputs:
        id, telescope_id, az_angle, el_angle, health_status, movement_status, created_at = db_select_reading_outputs[-1]
        return Reading(id=int(id), telescope_id=int(telescope_id),az_angle=float(az_angle), el_angle=float(el_angle), health_status=str(health_status),
                       movement_status=str(movement_status), created_at=datetime.fromisoformat(str(created_at)))
    else:
        raise HTTPException(status_code=404, detail=f"No readings found for telescope ID {telescope_id}.")
def post_reading(reading: CreateReading) -> Reading:
    db = Database()
    _,_ = db.insert(table_name, reading.__dict__)
    _, db_select_reading_outputs = db.read(table_name, criteria=reading.__dict__)
    id, telescope_id, az_angle, el_angle, health_status, movement_status, created_at = db_select_reading_outputs[-1]
    return Reading(id=int(id), telescope_id=int(telescope_id),az_angle=float(az_angle), el_angle=float(el_angle),
                    health_status= str(health_status),movement_status=str(movement_status), created_at=datetime.fromisoformat(str(created_at)))

def delete_reading(reading_id: int) -> Reading:
    db = Database()
    _, db_select_reading_outputs = db.read(table_name, criteria={'id': reading_id})
    if db_select_reading_outputs:
        id, telescope_id, az_angle, el_angle, health_status, movement_status, created_at = db_select_reading_outputs[0]
        reading = Reading(id=int(id), telescope_id=int(telescope_id),az_angle=float(az_angle), el_angle=float(el_angle), health_status=str(health_status), movement_status=str(movement_status), created_at=datetime.fromisoformat(str(created_at)))
        success, _ =db.delete(table_name, criteria={'id': reading_id})
        if success:
            return reading
        else: 
            return HTTPException(status_code=500, detail="Failed to delete reading.")
    else:
        raise HTTPException(status_code=404,detail=f"Reading with ID {reading_id} not found.")
   
        
def update_reading(reading_id: int, reading: Reading) -> Reading:
    db = Database()
    success, _ =db.update(table_name, criteria={'id': reading_id}, data=reading.__dict__)
    if success:
        _, db_select_reading_outputs = db.read(table_name, criteria={'id': reading_id})
        id, telescope_id, az_angle, el_angle, health_status, movement_status, created_at = db_select_reading_outputs[0]
        return Reading(id=int(id), telescope_id=int(telescope_id),az_angle=float(az_angle),el_angle=float(el_angle), health_status=str(health_status),
                       movement_status=str(movement_status), created_at=datetime.fromisoformat(str(created_at)))
    else:
        return None
    
