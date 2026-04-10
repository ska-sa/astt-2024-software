from datetime import datetime
from fastapi import HTTPException
from classes.source import CreateSource, Source
from classes import Database

table_name: str = 'source'

def get_source(source_id: int) -> Source:
    db = Database()
    _, db_select_source_outputs = db.read(table_name, criteria={'id': source_id})
    if db_select_source_outputs:
        id, source_name, initial_right_ascension, initial_declination, rate_right_ascension, rate_declination, reset_period, created_at = db_select_source_outputs[0]
        return Source(
            id=id,
            source_name=source_name,
            initial_right_ascension=initial_right_ascension,
            initial_declination=initial_declination,
            rate_right_ascension=rate_right_ascension,
            rate_declination=rate_declination,
            reset_period=reset_period,
            created_at=datetime.fromisoformat(str(created_at))
        )
    else:
        raise HTTPException(status_code=404, detail=f"Source with ID {source_id} not found.")

def get_sources() -> list[Source]:
    db = Database()
    _, db_select_source_outputs = db.read(table_name)
    sources = []
    for db_select_source_output in db_select_source_outputs:
        id, source_name, initial_right_ascension, initial_declination, rate_right_ascension, rate_declination, reset_period, created_at = db_select_source_output
        sources.append(Source(
            id=id,
            source_name=source_name,
            initial_right_ascension=initial_right_ascension,
            initial_declination=initial_declination,
            rate_right_ascension=rate_right_ascension,
            rate_declination=rate_declination,
            reset_period=reset_period,
            created_at=datetime.fromisoformat(str(created_at))
        ))
    return sources

def post_source(source: CreateSource) -> Source:
    db = Database()
    _, _ = db.insert(table_name, source.__dict__)
    _, db_select_source_outputs = db.read(table_name, criteria=source.__dict__)
    id, source_name, initial_right_ascension, initial_declination, rate_right_ascension, rate_declination, reset_period, created_at = db_select_source_outputs[-1]
    return Source(
        id=id,
        source_name=source_name,
        initial_right_ascension=initial_right_ascension,
        initial_declination=initial_declination,
        rate_right_ascension=rate_right_ascension,
        rate_declination=rate_declination,
        reset_period=reset_period,
        created_at=datetime.fromisoformat(str(created_at))
    )

def delete_source(source_id: int) -> Source:
    db = Database()
    _, db_select_source_outputs = db.read(table_name, criteria={'id': source_id})
    if db_select_source_outputs:
        id, source_name, initial_right_ascension, initial_declination, rate_right_ascension, rate_declination, reset_period, created_at = db_select_source_outputs[0]
        source = Source(
            id=id,
            source_name=source_name,
            initial_right_ascension=initial_right_ascension,
            initial_declination=initial_declination,
            rate_right_ascension=rate_right_ascension,
            rate_declination=rate_declination,
            reset_period=reset_period,
            created_at=datetime.fromisoformat(str(created_at))
        )
        success, _ = db.delete(table_name, criteria={'id': source_id})
        if success:
            return source
        else:
            raise HTTPException(status_code=500, detail="Failed to delete source.")
    else:
        raise HTTPException(status_code=404, detail=f"Source with ID {source_id} not found.")

def update_source(source_id: int, source: Source) -> Source:
    db = Database()
    success, _ = db.update(table_name, criteria={'id': source_id}, data=source.__dict__)
    if success:
        _, db_select_source_outputs = db.read(table_name, criteria={'id': source_id})
        id, source_name, initial_right_ascension, initial_declination, rate_right_ascension, rate_declination, reset_period, created_at = db_select_source_outputs[0]
        return Source(
            id=id,
            source_name=source_name,
            initial_right_ascension=initial_right_ascension,
            initial_declination=initial_declination,
            rate_right_ascension=rate_right_ascension,
            rate_declination=rate_declination,
            reset_period=reset_period,
            created_at=datetime.fromisoformat(str(created_at))
        )
    else:
        raise HTTPException(status_code=500, detail="Failed to update source.")
