"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import boto3, urllib.request, json 


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': speechlet_response 
            }
        }
        
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    should_end_session = False
    return build_response(session_attributes, "Welcome to Twitch Moderator")


def handle_session_end_request():
    card_title = "Session Ended"
    
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, "Ending Session")
    
def remove(intent, session):
    card_title = intent['slots']['Username']['value']
    session_attributes = {}
    should_end_session = False
    
    sendSQS("ban "+ card_title)

    return build_response(session_attributes, card_title + " has Been Banned")


def raffle(intent, session):
    card_title = intent['slots']['Prize']['value']
    session_attributes = {}
    should_end_session = False
    
    sendSQS('raffle ' + card_title)

    return build_response(session_attributes, "You have set up a raffle!")


def schedule(intent, session):
    session_attributes = {}
    reprompt_text = None

    
    should_end_session = False
    sendSQS('schedule')

    return build_response(session_attributes, "You have set a schedule!")

def SlowOff(intent, session):
    session_attributes = {}
    reprompt_text = None

    
    should_end_session = False
    sendSQS('slowOff')

    return build_response(session_attributes, "You have turned off slow!")
    
def Subscribers(intent, session):
    session_attributes = {}
    reprompt_text = None

    
    should_end_session = False
    sendSQS('subscribers')

    return build_response(session_attributes, "The channel has been set to subscribers only!")
    
def SubscribersOff(intent, session):
    session_attributes = {}
    reprompt_text = None

    
    should_end_session = False
    sendSQS('subscribersOff')

    return build_response(session_attributes, "You have turned off subscribers only!")
    
def TimeOut(intent, session):
    card_title = intent['slots']['Username']['value']
    seconds = intent['slots']['Seconds']['value']
    session_attributes = {}
    should_end_session = False
    
    sendSQS("timeout "+ card_title + " for " + seconds)
    
    print(seconds)
    print(len(seconds))
    
    if(len(seconds) == 5):
        sec = seconds[2]
        tsec = seconds[3]
        fsec = sec + tsec
    else:
        sec = seconds[2]
    print(fsec)
        

    return build_response(session_attributes, card_title + " is timed out for " + fsec + " seconds!" )
    
def Slow(intent, session):
    seconds = intent['slots']['Seconds']['value']
    session_attributes = {}
    reprompt_text = None

    
    should_end_session = False
   
    if(len(seconds) == 5):
        sec = seconds[2]
        tsec = seconds[3]
        fsec = sec + tsec
    else:
        sec = seconds[2]
        
    sendSQS('slow ' + fsec)

    return build_response(session_attributes, "You have slowed for " + fsec + " seconds!")
    
def post(intent, session):
    card_title = intent['slots']['Media']['value']
    session_attributes = {}
    reprompt_text = None

    
    should_end_session = False
    sendSQS("post  "+ card_title)

    return build_response(session_attributes, "You have posted an " + card_title)
    
def Host(intent, session):
    card_title = intent['slots']['Username']['value']
    session_attributes = {}
    should_end_session = False
    
    sendSQS("host "+ card_title)
    

    return build_response(session_attributes, "You are now hosting " + card_title + "!")
    
def viewer(intent, session):
    session_attributes = {}
    should_end_session = False
    
    with urllib.request.urlopen("https://tmi.twitch.tv/group/user/telorpheus/chatters") as url:
        data = json.loads(url.read().decode())

    
    return build_response(session_attributes, "You have " + str(data['chatter_count']) + " viewers.")    
    
def Unhost(intent, session):
    session_attributes = {}
    should_end_session = False
    
    sendSQS("unhost")
    
    return build_response(session_attributes, "You are unhosting!")
    

    
def sendSQS(command):
    sqs = boto3.client('sqs')
    queue_url = "url"
    
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'The Whistler'
            }
        },
        MessageBody=(
            command
        )   
    )


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers

    if intent_name == "Raffle":
        return raffle(intent, session)
    elif intent_name == "Post":
        return post(intent, session)
    elif intent_name == "Viewer":
        return viewer(intent, session)
    elif intent_name == "Schedule":
        return schedule(intent, session)
    elif intent_name == "SlowOff":
        return SlowOff(intent, session)
    elif intent_name == "Subscribers":
        return Subscribers(intent, session)
    elif intent_name == "SubscribersOff":
        return SubscribersOff(intent, session)
    elif intent_name == "TimeOut":
        return TimeOut(intent, session)
    elif intent_name == "Slow":
        return Slow(intent, session)
    elif intent_name == "Host":
        return Host(intent, session)
    elif intent_name == "Unhost":
        return Unhost(intent, session)
    elif intent_name == "Remove":
        return remove(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
