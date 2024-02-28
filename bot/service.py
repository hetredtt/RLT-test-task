import json
import utils.api_query as ApiQuery

async def send_json_to_api(json_data: dict) -> dict:
    try:
        answer = await ApiQuery.answer(json_data)
        return answer
    except Exception as e:
        return {"error": f"Ошибка при обращении к API: {e}"}