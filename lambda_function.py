import json
import urllib2
from xml.dom import minidom

# fill in the variables below
wskey = ""
zip_code = ""

# OCLC WorldCat Search API base URLs
base_url_search = "http://www.worldcat.org/webservices/catalog/search/worldcat/opensearch?q="
base_url_location = "http://www.worldcat.org/webservices/catalog/content/libraries/"

# the AWS Lambda handler function
def lambda_handler(event, context):
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

# function to log start of new session
def on_session_started(session_started_request, session):
    print "Starting new session."

# return welcome message when LaunchRequest is received
def on_launch(launch_request, session):
    return get_welcome_response()

# specify functions to return appropriate response for each event type
def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "SearchIntent":
        return get_book_info(intent)
    elif intent_name == "AMAZON.YesIntent":
        return get_address(intent_request, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent" or intent_name == "AMAZON.NoIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

# function to log end of session
def on_session_ended(session_ended_request, session):
    print "Ending session."

# return goodbye message when SessionEndedRequest is received
def handle_session_end_request():
    card_title = "Ask WorldCat"
    speech_output = "Thank you for using Ask WorldCat."
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, speech_output, None, should_end_session))

# function to build welcome message
def get_welcome_response():
    session_attributes = {}
    card_title = "Ask WorldCat"
    speech_output = "Welcome to the Alexa Ask WorldCat service. " \
                    "Ask me to find a book for you. For example, you can say, \'Where can I find \'On the Road.\'\'"
    reprompt_text = "Ask me to find a book for you. For example, you can say, \'Where can I find \'On the Road.\'\'"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, speech_output, reprompt_text, should_end_session))

# upon SearchIntent, call WorldCat Search API to build speech response
# sample query: Alexa, where can I find Hillbilly Elegy?
# sample response: The closest library where you can find Hillbilly elegy by Vance, J. D., author. is Worthington Libraries.\n\nDo you need the library's address?
def get_book_info(intent):
    session_attributes = {}
    card_title = "Ask WorldCat"
    reprompt_text = "Ask me to find a book for you. For example, you can say, \'Where can I find \'On the Road.\'\'"
    should_end_session = False

    if "Search" in intent["slots"]:
        search = intent["slots"]["Search"]["value"]
        search_url = base_url_search + urllib2.quote(search) + "%22&wskey=" + wskey

        # call the Search API
        dom = minidom.parse(urllib2.urlopen(search_url))
        entries = dom.getElementsByTagName('entry')
        
        # check for empty result set
        if len(entries) == 0:
            speech_output = "I'm sorry, I couldn't find anything matching your search."
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, speech_output, reprompt_text, should_end_session))
        
        # store pertinent metadata
        entry = entries[0]
        title = entry.getElementsByTagName('title')[0].firstChild.data
        authorName = entry.getElementsByTagName('author')[0]
        author = authorName.getElementsByTagName('name')[0].firstChild.data
        oclcNum = entry.getElementsByTagName('oclcterms:recordIdentifier')[0].firstChild.data
        
        # get library location info from Search API
        location_url = base_url_location + oclcNum + "?location=" + zip_code + "&wskey=" + wskey + "&format=json"
        location_response = urllib2.urlopen(location_url)
        location_data = json.loads(location_response.read())
        closest_library = location_data['library'][0]
        closest_library_name = closest_library['institutionName']
        closest_library_address = closest_library['streetAddress1'] + closest_library['streetAddress2'] + ", " + closest_library['city'] + ", " + closest_library['state'] + ", " + closest_library['postalCode'] + ", " + closest_library['country']
        
        # build speech output and store session attributes
        speech_output = "The closest library where you can find " + title + " by " + author + " is " + closest_library_name + ".\n\nDo you need the library's address?"
        reprompt_text = ""
        session_attributes = {
            "title" : title,
            "author" : author,
            "closest_library_name" : closest_library_name,
            "closest_library_address" : closest_library_address,
        }
    
    # return response
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, speech_output, reprompt_text, should_end_session))

# function called upon AMAZON.YesIntent
# i.e. when user response "Yes" to "Do you need the library's address?"
# speech output: I've sent the address to your device."
# sample card output: Worthington Libraries\n\n820 High Street, Worthington, OH, 43085, United States
def get_address(intent_request, session):
    session_attributes = {}
    card_title = "Ask WorldCat"
    reprompt_text = "Ask me to find a book for you. For example, you can say, \'Where can I find \'On the Road.\'\'"
    should_end_session = True
    
    # pull needed metadata from session attributes
    title = session["attributes"]["title"]
    author = session["attributes"]["author"]
    closest_library_name = session["attributes"]["closest_library_name"]
    closest_library_address = session["attributes"]["closest_library_address"]
    
    speech_output = "I've sent the address to your device."
    
    # build card text
    card_text = closest_library_name + "\n\n" + closest_library_address
    
    # return response
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_text, reprompt_text, should_end_session))

# helper function to build speechlet for Alexa response    
def build_speechlet_response(title, output, card_text, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": card_text
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

# helper function to build Alexa response
def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }