# ivrMock for callflow used in CfL app

This repository contains the mocked system for handling calls using IVR approach. It is based on the Vonage/Nexmo system and this 
mock simulate the behavior of callflows. It is desired to use for test purposes for example performance tests.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine 
or test server for development and testing purposes. Please run this service only for test purposes. 
IT IS NOT INTENDENT TO WORK ON PRODUCTION ENVIRONMENTS. PLEASE DO NOT USE IT ON PROD ENVIRONMENTS.

### Prerequisites

In order to use mocked IVR calls, you have to:
* create openMRS/CfL folder
* within newly created folder, clone [CfL distro](https://github.com/SolDevelo/openmrs-distro-cfl)
* verify CfL module - `callflows-1.1.12.omod` (to verify, check version within `openmrs-distro-cfl/cfl/web/cfl-modules/`)

### Installation on local environment or test server

To make a copy of this project on your local machine, please follow the next steps:
* clone [CfL distro](https://github.com/SolDevelo/openmrs-distro-cfl) (if you don't have yet cloned)
* clone the repository next to the cfl distro
```
git clone https://github.com/SolDevelo/vonage-calls-sample-mock-server
```
* within `openmrs-distro-cfl/cfl` folder add `docker-compose.nexmomockivr.yml` with content:
```
version: '2'

services:
  redis:
    image: "redis:latest"
    ports:
      - "6379:6379"

  ivrmock:
    build:
      context: ../../vonage-calls-sample-mock-server
      dockerfile: Dockerfile
    ports:
      - "7000:7000"

```
* within `openmrs-distro-cfl/cfl` folder update file `runInDevMode.sh` to update line 
with building docker images by adding `-f docker-compose.nexmomockivr.yml` for example:
```
docker-compose -f docker-compose.build.yml -f docker-compose.run.yml  -f docker-compose.debug.yml -f docker-compose.db.yml -f docker-compose.nexmock.yml -f docker-compose.nexmomockivr.yml up --build -d
```
* within `openmrs-distro-cfl/cfl` folder execute runInDevMode.sh. Alternatively if you want to attach this new 
service into already running CfL distro you can run this by executing in this folder:
```
docker-compose -f docker-compose.nexmomockivr.yml up --build -d
```
* now you should have running service with ivrMock app. Verify if app is running by executing `docker logs <container-name-or-id-container>`
or `docker ps`.

### Configuration on local app or app working in test environment
* Log into CfL as admin `http://<hostname>/openmrs/login.htm`
* Go into `http://localhost:8080/openmrs/owa/callflows/index.html#/providers` calls providers
* Add new provider
* Fill the form in the way as it is below:
```
Name: nexmo
a) Outgoing call URI template (optional): http://ivrmock:7000/v1/calls/
b) Is authentication required?: Unchecked
c) Outgoing call HTTP method: Check POST
d) POST header parameters: Content-Type: application/json
e) POST parameters: {"to": [ {"type": "phone","number": [phone]}],"from": {"type": "phone","number": 489999999876},"answer_url": 
["http://web:8080/openmrs/ws/callflows/in/nexmo/flows/MainFlow.nexmo?numbertodial=[phone]&jumpTo=[internal.jumpTo]&callId=[internal.callId]&phone=[phone]"],
"event_url":["http://web:8080/openmrs/ws/callflows/status/[internal.callId]?externalIdParamName=conversation_uuid&externalType=conversation_uuid"],
"event_method": "GET", "length_timer": 600}
f) Outbound Call Queue Configuration -> Call Limit: 0, Retry Sec: 0, Retry Attempts 0, Call after all Retry Attempts?: checked
g) Map of services that can be injected in IVR templates: 
patientService:patientService,cflPersonService:cflPersonService,messagesService:messages.messagingService,
personService:personService,personDAO:personDAO,conceptDAO:conceptDAO,locationService:locationService,
messagingGroupService:messages.messagingGroupService,openmrsContext:context,patientTemplateService:messages.patientTemplateService,
healthTipService:messages.healthTipService,callService:callflows.callService,
adherenceFeedbackService:messages.adherenceFeedbackService,conceptService:conceptService
h) 
```
* Save provider configuration
* Load the callflows by uploader in `http://localhost:8080/openmrs/module/metadatasharing/import/list.form`
* Click `import package`
* Browse the proper package in ZIP format
* click next
* in 3rd step check `Choose import mode: From Master`
* in 4th step check `4. Adjust import mode: Skip Assessing (Advanced)`. Leave the rest options as are as default
* Now you should have imported callflows. Verify this by going to `http://localhost:8080/openmrs/owa/callflows/index.html#/designer`
* In `http://localhost:8080/openmrs/owa/callflows/index.html#/designer/edit/MainFlow` `MainFlow.main.handler` please replace code by this one and save changes:
```
::::::::::::::::::::::: $internal.callDirection
#set($noInputCount = 0)
#set($invalidCount = 0)
#if($internal.callDirection == "OUTGOING")
	#set($welcomeMessage = false)
  #set($visitReminderMessage = false)

  #if($messages.size() == 0)
    |exit|
  #else
    #foreach($message in $messages)
      #if($message.name == 'Welcome Message')
        #set($welcomeMessage = true)
        #set($welcomeMessageId = $message.messageId)
      #elseif($message.name == 'Visit reminder')
        #set($visitReminderMessage = true)
        #set($visitReminderMessageId = $message.messageId)
      #end
    #end
    |play-message|
  #end
#else
	|exit|
#end
```
* In the same page with callflows design in entry-handler replace code with:
```
::::::::::::::::::::::::::::::::
::::: MainFlow params logger::::
phone:::::::::::: $phone
session.callid::: $params.get("session.callerid")
::::::::::::::::::::::::::::::::
params::::::::::: $params
messages::::::::: $messages
::::::::::::::::::::::::::::::::
personId::::::::: $personId
actorType:::::::: $actorType
actorId:::::::::: $actorId
refKey::::::::::: $refKey
internal::::::::: $internal
::::::::::::::::::::::::::::::::

#set($callId = $internal.callId)
#set($pinAttempts = 0)
#set($maxPinAttempt = 3)

#if($refKey)
	#set($sourceId = $refKey)
  #set($sourceType = "SCHEDULED_SERVICE_GROUP")
  #set($serviceGroup = $messagingGroupService.getById($Integer.parseInt($refKey)))
  #set($patientId = $serviceGroup.getPatient().personId)
patientId:::::::: $patientId
service group:::: $sourceId
#else
	#set($sourceId = $callId)
  #set($sourceType = "OTHER")
  #set($patientId = $actorId)
#end

#if(!$actorId && $personId)
	#set ($actorId = $personId)
#elseif($actorId)	
	#set ($actorId = $Integer.parseInt($actorId)) 
#end

actorId:::::::::: $actorId

#set ($person = $personDAO.getPerson($actorId))

#if($person)
	  #set($personStatus = "DEACTIVATED")
    #set($maxPinAttempt = 3)
    #set($pinAttempts = 0)
:::::::::::::::::::::::::::::::
person attributes:::::::::::::::
  	#foreach($attribute in $person.getActiveAttributes())
::::::::::::::::: $attribute.attributeType.name
::::::::::::::::: $attribute.value
::::::::::::::::: $attribute.voided
      #if($attribute.attributeType.personAttributeTypeId == 11 && !$attribute.voided)
      	#set($personStatus = $attribute.value)
personStatus::::: $personStatus
      #end
    #end
:::::::::::::::::::::::::::::::
|PinFlow.|
#else
|exit|
#end
```
* Go into `Manage Global Properties` in `System Administration`
* Add value for message.callConfig: nexmo
* Update value for `messages.statusesEndingCallflow` GP to replace with ‘ANSWERED,UNANSWERED,MACHINE,BUSY,CANCELLED,FAILED,REJECTED,NO_ANSWER,TIMEOUT,completed,UNKNOWN,DISCONNECTED’
* Update value for ‘messages.defaultFlow’ GP to add ‘MainFlow’
* (optional: for debug purposes) if you want to have more logs with DEBUG status for calls: please update log.level GP with ‘org.openmrs.api:info,org.openmrs.module.callflows:debug’. In that case you have to  either execute ‘runInDevMode.sh’ again or restart the web container.
* Now you should have configured calls based on the IVR mocked solution. You can test this by creating visit for patient.

## License

Copyright (c) SolDevelo

This project is licensed under the MIT - see the [LICENSE.md](LICENSE.md) file for details.
