from fastapi import HTTPException
from classes.reading import CreateReading, Reading
from datetime import datetime
from classes import Database

table_name: str = 'reading'
datetime_format_str: str = '%Y-%m-%d %H:%M:%S'

def get_reading(telescope_id: int) -> Reading:
    db = Database()
    _,db_select_reading_outputs = db.read(table_name, criteria={'id': telescope_id})
    if db_select_reading_outputs:
        id, telescope_id, az_angle, el_angle, health_status, movement_status, created_at =db_select_reading_outputs[0]
        return Reading(id=int(id),telescope_id=int(telescope_id),az_angle=float(az_angle), el_angle=float(el_angle),health_status=str(health_status),
                       movement_status=str(movement_status), created_at=datetime.strptime(str(created_at),datetime_format_str))
    else:
        return None
    
def get_readings() -> list[Reading]:
    db = Database()
    _, db_select_reading_outputs = db.read(table_name)
    readings =[]
    for db_select_reading_output in db_select_reading_outputs:
        id, telescope_id, az_angle, el_angle, health_status, movement_status, created_at = db_select_reading_output
        readings.append(Reading(id=int(id), telescope_id=int(telescope_id), az_angle=float(az_angle), el_angle=float(el_angle),health_status=str(health_status),
                                movement_status=str(movement_status), created_at=datetime.strptime(str(created_at), datetime_format_str)))
    return readings

def post_reading(reading: CreateReading) -> Reading:
    db = Database()
    _,_ = db.insert(table_name, reading.__dict__)
    _, db_select_reading_outputs = db.read(table_name, criteria=reading.__dict__)
    id, telescope_id, az_angle, el_angle, health_status, movement_status, created_at = db_select_reading_outputs[-1]
    return Reading(id=int(id), telescope_id=int(telescope_id),az_angle=float(az_angle), el_angle=float(el_angle),
                    health_status= str(health_status),movement_status=str(movement_status), created_at=datetime.strptime(str(created_at), datetime_format_str))

def delete_reading(telescope_id: int) -> Reading:
    db = Database()
    _, db_select_reading_outputs = db.read(table_name, criteria={'id': telescope_id})
    if db_select_reading_outputs:
        id, telescope_id, az_angle, el_angle, health_status, movement_status, created_at = db_select_reading_outputs[0]
        reading = Reading(id=int(id), telescope_id=int(telescope_id),az_angle=float(az_angle), el_angle=float(el_angle), health_status=str(health_status), movement_status=str(movement_status), created_at=datetime.strptime(str(created_at), datetime_format_str))
        success, _ =db.delete(table_name, criteria={'id': telescope_id})
        if success:
            return reading
        else: 
            return HTTPException(status_code=500, detail="Failed to delete reading.")
    else:
        raise HTTPException(status_code=404,detail=f"Reading with ID {telescope_id} not found.")
        
def update_reading(telescope_id: int, reading: Reading) -> Reading:
    db = Database()
    success, _ =db.update(table_name, criteria={'id': telescope_id}, data=reading.__dict__)
    if success:
        _, db_select_reading_outputs = db.read(table_name, criteria={'id': telescope_id})
        id, telescope_id, az_angle, el_angle, health_status, movement_status, created_at = db_select_reading_outputs[0]
        if str(created_at).find("T") != -1:
            created_at = created_at.replace("T", " ")
        return Reading(id=int(id), telescope_id=int(telescope_id),az_angle=float(az_angle),el_angle=float(el_angle), health_status=str(health_status),
                       movement_status=str(movement_status), created_at=datetime.strptime(str(created_at), datetime_format_str))
    else:
        return None
    
