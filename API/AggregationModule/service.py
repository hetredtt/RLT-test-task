from datebase.db import MongoDBConnection
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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
        
        if group_type == 'day':
            all_dates = [(dt_from + timedelta(days=i)).strftime("%Y-%m-%dT%H:%M:%S")  for i in range((dt_upto - dt_from).days + 1)]
        elif group_type == 'hour':
            all_dates = [(dt_from + timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M:%S") for i in range(int((dt_upto - dt_from).total_seconds() // 3600) + 1)]
        else:
            all_dates = [(dt_from + relativedelta(months=i)).strftime("%Y-%m-%dT%H:%M:%S") for i in range((dt_upto.year - dt_from.year) * 12 + dt_upto.month - dt_from.month + 1)]

        labels = [datetime.strptime(result["_id"], format).strftime("%Y-%m-%dT%H:%M:%S") for result in aggregate]
        dataset = [result["total_value"] for result in aggregate]

        index_dict = {value: index for index, value in enumerate(all_dates)}

        new_dataset = [0] * len(all_dates)

        for value, number in zip(labels, dataset):
            index = index_dict.get(value)
            if index is not None:
                new_dataset[index] = number

        output = {
            "dataset": new_dataset,
            "labels": all_dates
        }
        db.close()
        return output
    else:
        print("Failed to connect to MongoDB!")

