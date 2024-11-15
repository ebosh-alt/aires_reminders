import json

from data.config import DIVISION_ID, REQUIRED_FIELDS
from entities.models import ApiPoint, FieldData, User, Reminder, Deals
from services.Intrum.Base import BaseApi, logger


class ClientIntrum(BaseApi):
    def __init__(self, token):
        super().__init__(token)

    async def get_users(self, overdue: bool = False) -> list[User] | int:  #TODO: изменить проверку статусу(В штате)
        response = await self._post(ApiPoint.worker_filter, {"params[publish]": 1})
        logger.info(response)
        if response.get("status") != "success":
            return 404

        users = []
        for user_data in response.get("data", {}).values():
            if user_data.get("id") == "952":
                logger.info(json.dumps(user_data, indent=4, ensure_ascii=False))
                division_id = user_data.get("division_id")
                fields = user_data.get("fields", {})
                works = fields.get("1707", {}).get("value")
                leads_connected = fields.get("3644", {}).get("value")
                lead_status = fields.get("3657", {}).get("value")
                if not overdue:
                    add_condition = all([
                        works == "Сотрудник в штате" or works == "Новый сотрудник",
                        leads_connected == "1",
                        lead_status == "Лиды Включены"
                    ])
                else:
                    add_condition = all([
                        works == "Сотрудник в штате",
                        leads_connected == "1",
                        lead_status == "Лиды Отключены"
                    ])
                if division_id == DIVISION_ID and add_condition:
                    fields_data = {
                        field_id: FieldData(**field_info)
                        for field_id, field_info in fields.items()
                        if field_id in REQUIRED_FIELDS
                    }
                    users.append(User(
                        id=user_data.get("id"),
                        # telegram_id=telegram_id,
                        division_id=division_id,
                        name=user_data.get("name"),
                        surname=user_data.get("surname"),
                        secondname=user_data.get("secondname"),
                        fields=fields_data
                    ))
        return users

    async def get_users_expired(self):
        return await self.get_users(True)

    async def change_user(self, user_id: int = "1125"):
        # получение сотрудника
        response = await self._post(ApiPoint.worker_filter, {"params[id]": user_id})
        if response.get("status") != "success":
            return 404
        user = response["data"].get(user_id)
        if user:
            logger.info(json.dumps(user, indent=4, ensure_ascii=False))
            fields = user["fields"]
            lead_status = fields.get("3657", {}).get("value")
            if lead_status:
                user["fields"]["3657"]["value"] = "Лиды Отключены"
                logger.info(json.dumps(user, indent=4, ensure_ascii=False))
                # попытка изменить сотрудника
                params = {
                    "params": {
                        "id": user.get("id"),
                        "fields": [{"id": "3657", "value": "Лиды Отключены"}]
                    }}
                response = await self._post(ApiPoint.update_user, params)
                logger.info(response)
                if response.get("status") != "success":
                    return True
                return False

    async def get_deal(self, deal_id):
        params = {
            "params[byid]": deal_id,
            "params[order]": "desc"
        }
        # deals = []
        response = await self._post(ApiPoint.deals, params)
        logger.info(response)
        if response["status"] != "success":
            return 404
        for json_deal in response["data"]["list"]:
            # logger.info(json.dumps(json_deal, indent=4, ensure_ascii=False))
            logger.info(len(response["data"]["list"]))
            return Deals.from_json(json_deal)
        # return deals

    async def get_deals(self, users: list[User]) -> list[Deals] | int:
        user_ids = [user.id for user in users]
        params = {
            "params[manager]": user_ids,
            "params[order]": "desc"
        }
        deals = []
        response = await self._post(ApiPoint.deals, params)
        if response["status"] != "success":
            return 404
        for json_deal in response["data"]["list"]:
            deals.append(Deals.from_json(json_deal))
        return deals

    async def get_reminder(self, reminder_id):
        params = {
            "params[event_id]": reminder_id,
        }
        response = await self._post(ApiPoint.reminder, params)
        if response["status"] != "success":
            return 404
        reminder = Reminder(**response["data"])
        return reminder

    async def get_missed_reminder(self, user_id, reminder_id):  # TODO: модель для json объекта
        params = {
            "params[employee_id]": user_id,
        }
        response = await self._post(ApiPoint.missed_reminder, params)
        if response["status"] != "success":
            return 404
        for result in response["data"]:
            if str(result["event_id"]) == str(reminder_id):
                return result

    async def get_reminders(self, user_id):  # TODO: выборка по конкретному сотруднику
        params = {
            "params[employee]": user_id,
        }
        response = await self._post(ApiPoint.reminders, params)
        if response["status"] != "success":
            return 404
        reminders = []
        for json_reminder in response["data"]["list"]:
            logger.info(json.dumps(json_reminder, indent=4, ensure_ascii=False))
            # reminder = Reminder(**json_reminder)
            # reminders.append(reminder)
        return reminders
