from fastapi import APIRouter
import AggregationModule.service as Service
import AggregationModule.model as Model
from utils.logger import ModuleLogger


logger = ModuleLogger(__name__).get_logger()


router = APIRouter()

@router.post("/aggregate", summary="Получить результат аггрегации")
async def get_humo_file_n_decode(
    req: Model.Req
    ):
    try:
        aggregation_response = await Service.aggregate(req.dt_from, req.dt_upto, req.group_type)
        logger.info(f"get req: {req.dt_from}, {req.dt_upto}, {req.group_type}")
        return aggregation_response
    except Exception as e:
        logger.error(f"error: {e}")
        return {"error": str(e)}