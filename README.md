# alexa-worldcat-poc
A proof-of-concept service that allows you to search WorldCat using an Amazon Echo.

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