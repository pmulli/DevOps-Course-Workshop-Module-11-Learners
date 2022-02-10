import logging
import time
import typing
import uuid
import json
import azure.functions as func


def main(request: func.HttpRequest, translation: func.Out[str], msg: func.Out[typing.List[str]]) -> func.HttpResponse:
    logging.info('HTTP trigger function received a request.')
    start = time.time()

    req_body = request.get_json()
    subtitle = req_body.get("subtitle")
    languages = req_body.get("languages")

    rowKey = str(uuid.uuid4())

    data = {
        "Name": subtitle,
        "PartitionKey": "translation",
        "RowKey": rowKey
    }

    translation.set(json.dumps(data))

    queue_msg = []
    for language in languages:
        queue_data = {
            "rowKey": rowKey,
            "languageCode": language
        }
        queue_msg.append(json.dumps(queue_data))
    msg.set(queue_msg)

    end = time.time()
    processingTime = end - start

    return func.HttpResponse(
        f"Processing took {str(processingTime)} seconds. Translation is: {subtitle}",
        status_code=200
    )