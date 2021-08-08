!(https://i.imgur.com/qoJBTsJ.jpg)

This is a submission for the Warwick Hackathon 2021 - I had only 24 hours!

You can test the API using the information below, you can also run it locally however this will not work as I have removed my google credentials json which is needed to access my DialogueFlow agent.

Discord: Cal#2103

Youtube Example: https://youtu.be/aEsU-yPLXqY

## TO RUN 

Simply make sure you have Python 3.8 installed or available through a virtualenv.

Install the following packages with pip:
pip install flask flask_cors requests urllib3

Then run:
python app.py

The server will start up and you can send your requests via POST method to:
http://localhost:5000/scan
or ping my public API at
http://callydev.pythonanywhere.com/scan

## What it does

Simply query http://callydev.pythonanywhere.com/scan with a JSON object containing:

{
"sender": "Sender Name",
"sender_email": "sendersemail@gmail.com",
"email": "email body here"
}


For example if I send the body 

{
"sender": "Barclays UK",
"sender_email": "barclayssupport@gmail.com",
"email": "This is a scam email, you need to transfer us all your money!"
}

I would receive a response of:

{
    "biggest_intent": "Requesting Money",
    "company_data": {
        "domain": "barclays.co.uk",
        "logo": "https://logo.clearbit.com/barclays.co.uk",
        "name": "Barclays UK"
    },
    "domain_match": false,
    "domain_warning": "Company detected using @gmail domain, high risk",
    "intents": [{
        "confidence": 0.4614505469799042,
        "name": "Requesting Money"
    }],
    "is_gov": false,
    "is_personal": true
}

Response Breakdown:<br>
biggest_intent - this contains the most profound intent<br>
company_data - information of a company if the sender name matches a business name<br>
domain_match - is the company_datas registered website domain included in the email senders address<br>
domain_warning - displayed if a personal email domain is used and a company name used as sender name<br>
intents - contains lists of intents found and the confidence of the AI that this intent matches<br>
is_gov - is .gov domain found within the sender email<br>
is_personal - is @gmail found within the sender email<br>

## How we built it

This was built using Flask to host a local server, the Clearbit Public API for retrieving company data, and using Google DialogueFlow for the AI which determines intent. 

I have attached a screenshot of the response the API provides, and some screenshots of the phrases that I trained the DialogueFlow models with.

I gathered these phrases simply by searching up common scam phrases on Google and extracting key words/sentences from scam emails on Google Images!

## Accomplishments that we're proud of

The API can bypass DialogFlows max character count of 255 by splitting the email up, and returning a list of intents for each section, this can be useful as it provides more insight into a potential scam email.

The API can also match a senders name, to a company if registered, and if registered, it cross checks the domain the email was sent from, to the company on file. It returns an additional warning if the domain doesn't match.

## What's next for Email Fraud/Cybersecurity Detection

The original intention was for this to be submitted alongside a Google Chrome extension, however there wasn't enough time for that. It would've allowed the user to download an extension, and simply press 1 button, which would then scrape the current gmail email data off the page, query the API and display to the user any risks of whether the AI has detected scam phrases, also providing the legitimate company website if one was detected. However, this wasn't possible to complete in the timeframe so the submission stands as a public API or a service you can run locally.

This is my first project using DialogueFlow, however I have used Flask before!
