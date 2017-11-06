# alexa-worldcat-poc
A proof-of-concept service that allows you to search WorldCat using an Amazon Echo.

## Setup

1. Create or sign in to your [AWS account](https://console.aws.amazon.com/console/home).
2. Make sure you are using the either US East (N. Virginia) or EU (Ireland) region.
	1. For more information, see [Host a Custom Skill as an AWS Lambda Function](https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html).
3. Sign into AWS Lambda.
4. Create a new Lambda function.
5. Search the available Blueprints for "Alexa".
6. Select the "alexa-skills-kit-color-expert-python" Blueprint.
7. Function options
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
10. 