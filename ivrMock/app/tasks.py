import json
import logging
import requests
import time

from celery import shared_task
from datetime import datetime
from .actions import get_actions_list
from .utils import write_to_csv


log = logging.getLogger('app')


@shared_task
def process_mocked_call(data, response_data):
    def send_webhook(action, payload):
        try:
            if action != 'input' and action != 'notify' and action != 'talk':
                webhook_url = f'http://web:8080/openmrs/ws/callflows/status/' \
                              f'{payload["uuid"]}?status={payload["status"]}'
                log.info(webhook_url)
                log.info(action)
                log.info(payload)
                response = requests.get(webhook_url, json=json.dumps(payload))
                log.info(response)
                response_json = response.text
                log.info(response_json)
                webhook_url = f'http://web:8080/openmrs/ws/callflows/' \
                              f'calls/{payload["uuid"]}.nexmo?externalIdParamName={payload["conversation_uuid"]}' \
                              f'&externalType={payload["conversation_uuid"]}'
                response = requests.get(webhook_url, json=json.dumps(payload))
                log.info(webhook_url)
                log.info(response)
                log.info(response.text)
            elif action == 'input':
                webhook_url = f'http://web:8080/openmrs/ws/callflows/' \
                              f'calls/{payload["uuid"]}.nexmo?dtmf=1111' \
                              f'&dtmf.digits=1111&digits=1111&from={payload["from"]}&to={payload["to"]}'
                response = requests.get(webhook_url, json=json.dumps(payload))
                log.info(webhook_url)
                log.info(response)
                log.info(response.text)
            elif action == 'talk':
                webhook_url = f'http://web:8080/openmrs/ws/callflows/' \
                              f'calls/{payload["uuid"]}.nexmo?text={payload["text"]}' \
                              f'&from={payload["from"]}&to={payload["to"]}'
                response = requests.get(webhook_url, json=json.dumps(payload))
                log.info(webhook_url)
                log.info(response)
                log.info(response.text)
            else:
                webhook_url = f'http://web:8080/openmrs/ws{payload["url"]}'
                response = requests.get(webhook_url, json=json.dumps(payload))
                log.info(webhook_url)
                log.info(response)
                log.info(response.text)
        except Exception as exception:
            log.error("An error occurred: %s", str(exception))

    log.info("started mocked call")
    to = data.get('to', [])
    from_number = data.get('from', {})

    start_time = f"{datetime.now()}"

    actions = get_actions_list(
        from_number=from_number["number"],
        to_number=to[0]["number"],
        call_uuid=response_data["uuid"],
        conversation_uuid=response_data["conversation_uuid"],
        start_time=start_time
    )

    for action in actions:
        time.sleep(action["time"])
        send_webhook(action["action"], action["payload"])

    call_details = {
        'call_id': response_data['uuid'],
        'phone_from': from_number['number'],
        'phone_to': to[0]['number'],
    }

    write_to_csv(call_details)
