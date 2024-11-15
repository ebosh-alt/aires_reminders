from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from typing import Optional, List, Any

from pydantic import BaseModel, Field, field_validator

from data.config import REQUIRED_FIELDS_DEALS


@dataclass
class ApiPoint:
    base_url = "http://aires.astoria-tula.ru:80/sharedapi"
    worker_filter = f'{base_url}/worker/filter'
    publication_single = f"{base_url}/publication/single"
    deals = f"{base_url}/sales/filter"
    missed_reminder = f"{base_url}/org_events/missed_alarms"
    reminder = f"{base_url}/org_events/get"
    reminders = f"{base_url}/org_events/list"
    update_user = f"{base_url}/worker/update"


class FieldData(BaseModel):
    id: str
    datatype: str = None
    value: str | int = None


class User(BaseModel):
    id: str
    # telegram_id: str = None
    division_id: str = None
    name: str = None
    surname: str = None
    secondname: str = None
    fields: dict[str, FieldData] = Field(default_factory=dict)


class Deals(BaseModel):
    id: str
    customers_id: str
    employee_id: str
    date_create: Optional[str] = None
    sale_name: Optional[str] = None
    sale_type_id: Optional[int] = None
    fields: Optional[Dict[str, FieldData]] = None

    @classmethod
    def from_json(cls, data: dict[str, Any]):
        # Проверка условия для sale_type_id == 8
        if data.get("sale_type_id") != "8":
            return None
        # Фильтруем только нужные поля в fields
        fields_data = data.get("fields", {})
        filtered_fields = {k: v for k, v in fields_data.items() if k in REQUIRED_FIELDS_DEALS}

        # Обновляем data перед созданием экземпляра
        data["fields"] = {key: FieldData(**value) for key, value in
                          filtered_fields.items()} if filtered_fields else None

        return cls(**data)


class Connection(BaseModel):
    substance_summary: Optional[str] = None
    object_type: Optional[str] = None
    object_id: Optional[str] = None


class Reminder(BaseModel):
    id: str
    publ: Optional[str] = None
    uid: Optional[str] = None
    group_id: Optional[str] = None
    created: datetime
    last_modified: datetime = Field(alias='last-modified')
    status: Optional[str] = None
    author_id: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    dtstart: Optional[datetime] = None
    dtend: Optional[datetime] = None
    dtoffset: Optional[str] = None
    dtendoffset: Optional[str] = None
    allday: Optional[str] = None
    sequence: Optional[str] = None
    transparent: Optional[str] = None
    rrule: Optional[Any] = None
    is_reg: Optional[str] = None
    alarms: Optional[Any] = None
    last_queue: Optional[datetime] = Field(alias='last-queue')
    is_queued: Optional[str] = None
    theme_id: Optional[str] = None
    type_id: Optional[str] = None
    bg_color: Optional[str] = Field(alias='bg-color')
    b_color: Optional[str] = Field(alias='b-color')
    t_color: Optional[str] = Field(alias='t-color')
    queue: Optional[str] = None
    missed_alarms: Optional[Any] = None
    event_connections: Optional[str] = None
    queue_connections: Optional[str] = None
    users: Optional[List[str]] = None
    personal_priority: Optional[Any] = None
    connections: Optional[List[Connection]] = None

    @field_validator("created", "last_modified", "dtstart", "dtend", "last_queue", mode="before")
    def parse_datetime(cls, value):
        # Проверка и преобразование временной метки в datetime, если значение является строкой с цифрами
        if value is None:
            return None
        if isinstance(value, str) and value.isdigit():
            return datetime.fromtimestamp(int(value))
        return datetime.fromisoformat(value)
