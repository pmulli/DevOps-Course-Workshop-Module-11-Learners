import json
import logging
import uuid

import azure.functions as func


def main(msg: func.QueueMessage, translationJSON, translationResult: func.Out[str]) -> None:
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))

    language = json.loads(msg.get_body().decode('utf-8'))['languageCode']
    logging.info('Language: %s', language)

    subtitle = json.loads(translationJSON)['Name']
    logging.info('Subtitle: %s', subtitle)

    rowKey = str(uuid.uuid4())

    data = {
        "Name": subtitle.upper(),
        "PartitionKey": "translationResult",
        "RowKey": rowKey
    }

    translationResult.set(json.dumps(data))
