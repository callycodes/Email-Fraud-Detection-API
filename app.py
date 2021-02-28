
import os
from flask import Flask, request
from flask_cors import CORS, cross_origin
import requests
import urllib
import json
from collections import Counter

# I have removed this credentials file for safety!
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="googlecredentials.json"

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def hello_world():
    return 'Hello from Flask!!!'

# Returns intents of the email body sent to it using dialogue flow.
def detect_intent_texts(text):
    
    project_id = 'esoteric-virtue-306011'
    session_id = '123456789'
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code='en-US')

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result

# Send request to clearbit api to get company data if any is found.
def getSenderInfo(sender):
    if len(sender) > 1:
        search_result = requests.get('http://autocomplete.clearbit.com/v1/companies/suggest?query=' + urllib.parse.quote(sender))
        if search_result.text != '[]':
            search_json = json.loads(search_result.text)
            return {
                "name": search_json[0]['name'],
                "domain": search_json[0]['domain'],
                "logo": search_json[0]['logo']
                }
        else:
            return None

# Sort through intents list, return most common intent.
def biggest_intent(lst):
    intents = [item['name'] for item in lst]
    most_common = [intent for intent, intent_count in Counter(intents).most_common(1)]
    return most_common

# Scan endpoint, takes 3 email parameters and returns JSON object response 
# with in-depth fraud/risk analysis
@app.route('/scan', methods=['POST'])
@cross_origin()
def scan():
    if request.is_json:
        data = request.get_json()
        output = {
            "intents": [],
            "company_data": None,
            "domain_match": None
            }
        company_domain = getSenderInfo(data['sender'])

        # Splits the body of email into 255 character chunks so it doesn't
        # exceed dialogue flows limit.
        email_body_list = [(data['email'][i:i+255]) for i in range(0, len(data['email']), 255)]
        for email_body in email_body_list:
            intent_result = detect_intent_texts(email_body)
            output['intents'].append({
                "name": intent_result.intent.display_name,
                "confidence": intent_result.intent_detection_confidence
                })

        output['is_personal'] = '@gmail' in data['sender_email']
        output['is_gov'] = '.gov' in data['sender_email']


        if company_domain != None:
            output['company_data'] = company_domain
            output['domain_match'] = company_domain['domain'] in data['sender_email']
            if output['company_data'] != None and output['is_personal'] == True:
                output['domain_warning'] = 'Company detected using @gmail domain, high risk'

        output['biggest_intent'] = biggest_intent(output['intents'])[0]

        return output
    else:
        return "Incorrect formatting"
