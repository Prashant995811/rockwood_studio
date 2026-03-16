from sqlalchemy import inspect, text

from app.extensions import db
from app.models import SiteSetting


def ensure_schema_updates():
    inspector = inspect(db.engine)
    table_name = SiteSetting.__tablename__

    if table_name not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns(table_name)}
    if "logo_filename" not in existing_columns:
        db.session.execute(
            text(f"ALTER TABLE {table_name} ADD COLUMN logo_filename VARCHAR(255)")
        )
        db.session.commit()
