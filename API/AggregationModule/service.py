from datebase.db import MongoDBConnection
from datetime import datetime

async def aggregate(dt_from, dt_upto, group_type):
    print(dt_from)
    db = MongoDBConnection(host='localhost', port=27017, db_name='mydatabase')
    dt_from = datetime.fromisoformat(dt_from)
    dt_upto = datetime.fromisoformat(dt_upto)
    if group_type == 'day':
        format = "%Y-%m-%d"
    elif group_type == 'month':
        format = "%Y-%m"
    else:
        format = "%Y-%m-%dT%H"
    if db.connect():
        pipeline = [
            {
                "$match": {
                    "dt": {"$gte": dt_from, "$lte": dt_upto}
                }
            },
            {
                "$group": {
                    "_id": {"$dateToString": {"format": f"{format}", "date": "$dt"}},
                    "total_value": {"$sum": "$value"}
                }
            },
            {
                "$sort": {"_id": 1}
            }
        ]
        aggregate = db.find_documents('mycollection', pipeline)
        output = {
            "dataset": [result["total_value"] for result in aggregate],
            "labels": [result["_id"] for result in aggregate]
        }
        db.close()
        return output
    else:
        print("Failed to connect to MongoDB!")