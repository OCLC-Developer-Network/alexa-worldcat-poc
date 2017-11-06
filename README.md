# alexa-worldcat-poc
A proof-of-concept service that allows you to search WorldCat using an Amazon Echo.

Demo: [https://youtu.be/6Byuih0vfs4](https://youtu.be/6Byuih0vfs4)

Sample voice interaction:

* User: Alexa, launch WorldCat.
* Alexa: Ask me to find a book for you. For example, you can say, "Where can I find 'On the Road'?"
* User: Where can I find "On the Road"?
* Alexa: The closest library where you can find "On the Road" by Kerouac, Jack is Worthington Libraries. Do you need the library's address?
* User: Yes.
* Alexa: I've sent the address to your device.
* Card displays on Amazon Alexa app and/or Echo device
	* Worthington Libraries / 820 High Street, Worthington, OH, 43085, United States

## Setup Part 1 - AWS Lambda

1. Create or sign in to your [AWS account](https://console.aws.amazon.com/console/home).
2. Make sure you are using the either US East (N. Virginia) or EU (Ireland) region.
	1. For more information, see [Host a Custom Skill as an AWS Lambda Function](https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html).
3. Select AWS Lambda.
4. Create a new Lambda function.
5. Search the available Blueprints for "Alexa".
6. Select the "alexa-skills-kit-color-expert-python" Blueprint.
7. Function options:
	1. Give your function a name (such as `askWorldCat`).
	2. Choose the existing role `lambda_basic_execution`.
	3. Leave all the other default options.
	4. Create the function.
8. Copy and paste the contents of [lambda_function.py](lambda_function.py) into the code editor.
9. Fill in your [WorldCat Search API](https://www.oclc.org/developer/develop/web-services/worldcat-search-api.en.html) WSKey and your zipcode.
```python
# fill in the variables below
wskey = ""
zip_code = ""
```
10. Save all changes.
11. Note the ARN value in the top right of the screen.

## Setup Part 2 - Amazon Developer Console

1. Create or sign in to your [Amazon Developer Console](https://developer.amazon.com/).
2. Select Your Alexa Dashboards.
3. Select Alexa Skills Kit.
4. Add a New Skill.
5. Skill Information:
	1. Name = "Ask WorldCat"
	2. Invocation Name = "world cat"
	3. Leave all the other default options.
	4. Save > Next
6. Interaction Model:
	1. Intent Schema: copy and paste the contents of [intent_schema.json](speech_assets/intent_schema.json).
	2. Sample Utterances: copy and paste the contents of [utterances](speech_assets/utterances).
	3. Leave all the other default options.
	4. Save > Next
7. Configuration:
	1. Service Endpoint Type:
		1. Select "AWS Lambda ARN"
		2. Copy and paste your AWS Lambda ARN (Step 11, above) into the text box.
	2. Leave all the other default options.
	3. Save > Next

## Test

1. Test your Skill using the Voice Simulator or the Service Simulator in the Developer Console.
2. For example, entering the text "Where can I find Hillbilly Elegy?" in the Service Simulator will produce a request and response like the following:

Request:
```json
{
  "session": {
    "new": true,
    "sessionId": "SessionId.d85d7912...",
    "application": {
      "applicationId": "amzn1.ask.skill.59520a35..."
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.ask.account.AGHBSX2S..."
    }
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.d5048246-...",
    "intent": {
      "name": "SearchIntent",
      "slots": {
        "Search": {
          "name": "Search",
          "value": "hillbilly elegy"
        }
      }
    },
    "locale": "en-US",
    "timestamp": "2017-11-06T21:00:12Z"
  },
  "context": {
    "AudioPlayer": {
      "playerActivity": "IDLE"
    },
    "System": {
      "application": {
        "applicationId": "amzn1.ask.skill..."
      },
      "user": {
        "userId": "amzn1.ask.account.AGHBSX2SX..."
      },
      "device": {
        "supportedInterfaces": {}
      }
    }
  },
  "version": "1.0"
}
```

Response:
```json
{
  "version": "1.0",
  "response": {
    "outputSpeech": {
      "text": "The closest library where you can find Hillbilly elegy by Vance, J. D., author. is Worthington Libraries.\n\nDo you need the library's address?",
      "type": "PlainText"
    },
    "card": {
      "content": "The closest library where you can find Hillbilly elegy by Vance, J. D., author. is Worthington Libraries.\n\nDo you need the library's address?",
      "title": "Ask WorldCat"
    },
    "reprompt": {
      "outputSpeech": {
        "text": "",
        "type": "PlainText"
      }
    },
    "speechletResponse": {
      "outputSpeech": {
        "text": "The closest library where you can find Hillbilly elegy by Vance, J. D., author. is Worthington Libraries.\n\nDo you need the library's address?"
      },
      "card": {
        "content": "The closest library where you can find Hillbilly elegy by Vance, J. D., author. is Worthington Libraries.\n\nDo you need the library's address?",
        "title": "Ask WorldCat"
      },
      "reprompt": {
        "outputSpeech": {
          "text": ""
        }
      },
      "shouldEndSession": false
    }
  },
  "sessionAttributes": {
    "author": "Vance, J. D., author.",
    "closest_library_address": "820 High Street, Worthington, OH, 43085, United States",
    "closest_library_name": "Worthington Libraries",
    "title": "Hillbilly elegy"
  }
}
```

You can also copy and paste any requests from the Service Simulator into AWS Lambda as test events. This allows you to quickly run the tests against your code as you make changes.

If you have an Echo device associated with your Amazon account, you can use it to test your Skill too.
