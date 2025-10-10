from fastapi import HTTPException
from classes.command import CreateCommand, Command
from classes import Database
from datetime import datetime

table_name: str = 'command'

def get_command(command_id: int) -> Command:
    db = Database()
    _, db_select_command_outputs = db.read(table_name, criteria={'id': command_id})
    if db_select_command_outputs:
        id, user_id, telescope_id, target_az_angle, target_el_angle, created_at = db_select_command_outputs[0]
        return Command(
            id=int(id),
            user_id=str(user_id),
            telescope_id=str(telescope_id),
            target_az_angle=float(target_az_angle),
            target_el_angle=float(target_el_angle),
            created_at=datetime.fromisoformat(str(created_at))
        )
    else:
        raise HTTPException(status_code=404, detail=f"Command with ID {command_id} not found.")

def get_commands() -> list[Command]:
    db = Database()
    _, db_select_command_outputs = db.read(table_name)
    commands = []
    for db_select_command_output in db_select_command_outputs:
        id, user_id, telescope_id, target_az_angle, target_el_angle, created_at = db_select_command_output
        commands.append(Command(
            id=int(id),
            user_id=str(user_id),
            telescope_id=str(telescope_id),
            target_az_angle=float(target_az_angle),
            target_el_angle=float(target_el_angle),
            created_at=datetime.fromisoformat(str(created_at))
        ))
    return commands

def post_command(command: CreateCommand) -> Command:
    db = Database()
    _, _ = db.insert(table_name, command.__dict__)
    _, db_select_command_outputs = db.read(table_name, criteria=command.__dict__)
    id, user_id, telescope_id, target_az_angle, target_el_angle, created_at = db_select_command_outputs[-1]
    return Command(
        id=int(id),
        user_id=str(user_id),
        telescope_id=str(telescope_id),
        target_az_angle=float(target_az_angle),
        target_el_angle=float(target_el_angle),
        created_at=datetime.fromisoformat(str(created_at))
    )

def delete_command(command_id: int) -> Command:
    db = Database()
    _, db_select_command_outputs = db.read(table_name, criteria={'id': command_id})
    if db_select_command_outputs:
        id, user_id, telescope_id, target_az_angle, target_el_angle, created_at = db_select_command_outputs[0]
        command = Command(
            id=int(id),
            user_id=str(user_id),
            telescope_id=str(telescope_id),
            target_az_angle=float(target_az_angle),
            target_el_angle=float(target_el_angle),
            created_at=datetime.fromisoformat(str(created_at))
        )
        success, _ = db.delete(table_name, criteria={'id': command_id})
        if success:
            return command
        else:
            raise HTTPException(status_code=500, detail="Failed to delete command.")
    else:
        raise HTTPException(status_code=404, detail=f"Command with ID {command_id} not found.")

def update_command(command_id: int, command: Command) -> Command:
    db = Database()
    success, _ = db.update(table_name, criteria={'id': command_id}, data=command.__dict__)
    if success:
        _, db_select_command_outputs = db.read(table_name, criteria={'id': command_id})
        id, user_id, telescope_id, target_az_angle, target_el_angle, created_at = db_select_command_outputs[0]
        return Command(
            id=int(id),
            user_id=str(user_id),
            telescope_id=str(telescope_id),
            target_az_angle=float(target_az_angle),
            target_el_angle=float(target_el_angle),
            created_at=datetime.fromisoformat(str(created_at))
        )
    else:
        raise HTTPException(status_code=500, detail="Failed to update command.")
