from datetime import datetime


def get_actions_list(from_number, to_number, call_uuid, conversation_uuid, start_time):
    return [
        {
            "time": 10,
            "action": "answered",
            "payload": {
                "start_time": None,
                "rate": None,
                "from": from_number,
                "to": to_number,
                "uuid": call_uuid,
                "conversation_uuid": conversation_uuid,
                "status": "ANSWERED",
                "direction": "outbound",
                "network": None,
                "timestamp": f"{datetime.now()}"
            }
        },
        {
            "time": 5,
            "action": "completed",
            "payload": {
                "uuid": call_uuid,
                "conversation_uuid": conversation_uuid,
                "status": "COMPLETED",
                "timestamp": f"{datetime.now()}",
                "end_time": f"{datetime.now()}",
                "duration": 62,
                "start_time": start_time,
                "rate": 0.00000000,
                "price": 0.00000000,
                "from": from_number,
                "to": to_number,
                "direction": "outbound",
            }
        },
        {
            "time": 2,
            "action": "input",
            "payload": {
                "from": from_number,
                "to": to_number,
                "dtmf": {
                    "digits": "1111",
                    "timed_out": False
                },
                "uuid": call_uuid,
                "conversation_uuid": conversation_uuid,
                "timestamp": f"{datetime.now()}"
            }
        },
        {
            "time": 2,
            "action": "notify",
            "payload": {
                "start_time": None,
                "rate": None,
                "from": from_number,
                "to": to_number,
                "uuid": call_uuid,
                "conversation_uuid": conversation_uuid,
                "direction": "outbound",
                "network": None,
                "timestamp": f"{datetime.now()}",
                "url": f'/callflows/in/nexmo/flows/MainFlow.nexmo?callId={call_uuid}',
            }
        },
        {
            "time": 2,
            "action": "notify",
            "payload": {
                "start_time": None,
                "rate": None,
                "from": from_number,
                "to": to_number,
                "uuid": call_uuid,
                "conversation_uuid": conversation_uuid,
                "direction": "outbound",
                "network": None,
                "timestamp": f"{datetime.now()}",
                "url": f'/callflows/calls/{call_uuid}.nexmo?'
                       f'externalIdParamName={conversation_uuid}'
                       f'&externalType={conversation_uuid}'
            }
        },
        {
            "time": 2,
            "action": "input",
            "payload": {
                "from": from_number,
                "to": to_number,
                "dtmf": {
                    "digits": "1111",
                    "timed_out": False
                },
                "uuid": call_uuid,
                "conversation_uuid": conversation_uuid,
                "timestamp": f"{datetime.now()}"
            }
        },
        {
            "time": 2,
            "action": "notify",
            "payload": {
                "start_time": None,
                "rate": None,
                "from": from_number,
                "to": to_number,
                "uuid": call_uuid,
                "conversation_uuid": conversation_uuid,
                "direction": "outbound",
                "network": None,
                "timestamp": f"{datetime.now()}",
                "url": f'/callflows/calls/{call_uuid}.nexmo?'
                       f'externalIdParamName={conversation_uuid}'
                       f'&externalType={conversation_uuid}'
            }
        },
        {
            "time": 2,
            "action": "notify",
            "payload": {
                "start_time": None,
                "rate": None,
                "from": from_number,
                "to": to_number,
                "uuid": call_uuid,
                "conversation_uuid": conversation_uuid,
                "direction": "outbound",
                "network": None,
                "timestamp": f"{datetime.now()}",
                "url": f'/callflows/calls/{call_uuid}.nexmo?'
                       f'externalIdParamName={conversation_uuid}'
                       f'&externalType={conversation_uuid}'
            }
        },
        {
            "time": 2,
            "action": "notify",
            "payload": {
                "start_time": None,
                "rate": None,
                "from": from_number,
                "to": to_number,
                "uuid": call_uuid,
                "conversation_uuid": conversation_uuid,
                "direction": "outbound",
                "network": None,
                "timestamp": f"{datetime.now()}",
                "url": f'/callflows/calls/{call_uuid}.nexmo?'
                       f'externalIdParamName={conversation_uuid}'
                       f'&externalType={conversation_uuid}'
            }
        },
        {
            "time": 2,
            "action": "talk",
            "payload": {
                "from": from_number,
                "to": to_number,
                "text": "You've got a visit tomorrow.",
                "uuid": call_uuid,
                "conversation_uuid": conversation_uuid,
                "timestamp": f"{datetime.now()}"
            }
        },
        {
            "time": 2,
            "action": "input",
            "payload": {
                "from": from_number,
                "to": to_number,
                "dtmf": {
                    "digits": "1111",
                    "timed_out": False
                },
                "uuid": call_uuid,
                "conversation_uuid": conversation_uuid,
                "timestamp": f"{datetime.now()}"
            }
        },
        {
            "time": 2,
            "action": "notify",
            "payload": {
                "start_time": None,
                "rate": None,
                "from": from_number,
                "to": to_number,
                "uuid": call_uuid,
                "conversation_uuid": conversation_uuid,
                "direction": "outbound",
                "network": None,
                "timestamp": f"{datetime.now()}",
                "url": f'/callflows/calls/{call_uuid}.nexmo?'
                       f'externalIdParamName={conversation_uuid}'
                       f'&externalType={conversation_uuid}'
            }
        },
        {
            "time": 2,
            "action": "notify",
            "payload": {
                "start_time": None,
                "rate": None,
                "from": from_number,
                "to": to_number,
                "uuid": call_uuid,
                "conversation_uuid": conversation_uuid,
                "direction": "outbound",
                "network": None,
                "timestamp": f"{datetime.now()}",
                "url": f'/callflows/calls/{call_uuid}.nexmo?'
                       f'externalIdParamName={conversation_uuid}'
                       f'&externalType={conversation_uuid}'
            }
        },
        {
            "time": 2,
            "action": "disconnected",
            "payload": {
                "start_time": None,
                "rate": None,
                "from": from_number,
                "to": to_number,
                "uuid": call_uuid,
                "conversation_uuid": conversation_uuid,
                "status": "DISCONNECTED",
                "direction": "outbound",
                "network": None,
                "timestamp": f"{datetime.now()}"
            }
        },
    ]
