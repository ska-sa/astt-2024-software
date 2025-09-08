from fastapi import HTTPException
from classes.position import CreatePosition, Position
from classes import Database
from datetime import datetime

table_name: str = 'position'
datetime_format_str: str = '%Y-%m-%d %H:%M:%S'

def get_position(position_id: int) -> Position:
    db = Database()
    _, db_select_position_outputs = db.read(table_name, criteria={'id': position_id})
    if db_select_position_outputs:
        id, datetime_val, created_at = db_select_position_outputs[0]
        return Position(
            id=int(id),
            datetime=datetime.fromisoformat(str(datetime_val)),
            created_at=datetime.strptime(str(created_at), datetime_format_str)
        )
    else:
        raise HTTPException(status_code=404, detail=f"Position with ID {position_id} not found.")

def get_positions() -> list[Position]:
    db = Database()
    _, db_select_position_outputs = db.read(table_name)
    positions = []
    for db_select_position_output in db_select_position_outputs:
        id, datetime_val, created_at = db_select_position_output
        positions.append(Position(
            id=int(id),
            datetime=datetime.fromisoformat(str(datetime_val)),
            created_at=datetime.fromisoformat(str(created_at))
        ))
    return positions

def post_position(position: CreatePosition) -> Position:
    db = Database()
    _, _ = db.insert(table_name, position.__dict__)
    _, db_select_position_outputs = db.read(table_name, criteria=position.__dict__)
    id, datetime_val, created_at = db_select_position_outputs[-1]
    return Position(
        id=int(id),
        datetime=datetime.fromisoformat(str(datetime_val)),
        created_at=datetime.strptime(str(created_at), datetime_format_str)
    )

def delete_position(position_id: int) -> Position:
    db = Database()
    _, db_select_position_outputs = db.read(table_name, criteria={'id': position_id})
    if db_select_position_outputs:
        id, datetime_val, created_at = db_select_position_outputs[0]
        position = Position(
            id=int(id),
            datetime=datetime.fromisoformat(str(datetime_val)),
            created_at=datetime.strptime(str(created_at), datetime_format_str)
        )
        success, _ = db.delete(table_name, criteria={'id': position_id})
        if success:
            return position
        else:
            raise HTTPException(status_code=500, detail="Failed to delete position.")
    else:
        raise HTTPException(status_code=404, detail=f"Position with ID {position_id} not found.")

def update_position(position_id: int, position: Position) -> Position:
    db = Database()
    success, _ = db.update(table_name, criteria={'id': position_id}, data=position.__dict__)
    if success:
        _, db_select_position_outputs = db.read(table_name, criteria={'id': position_id})
        id, datetime_val, created_at = db_select_position_outputs[0]
        if str(created_at).find("T") != -1:
            created_at = created_at.replace("T", " ")
        return Position(
            id=int(id),
            datetime=datetime.fromisoformat(str(datetime_val)),
            created_at=datetime.fromisoformat(str(created_at))
        )
    else:
        raise HTTPException(status_code=500, detail="Failed to update position.")
