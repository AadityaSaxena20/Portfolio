from flask import Flask, render_template, request, jsonify, session
from fuzzywuzzy import fuzz
import spacy
import random
from spacy.matcher import PhraseMatcher
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecret'  # Session handling
nlp = spacy.load("en_core_web_sm")

# Links
BASE_URL = "https://chennai.vit.ac.in/"
ADMISSION_LINK = f"{BASE_URL}admissions/"
COURSES_LINK = f"{BASE_URL}academics/programmes-offered/"
FEE_LINK = f"{BASE_URL}fee-structure/"
PLACEMENT_LINK = f"{BASE_URL}placement/"
CAMPUS_LINK = f"{BASE_URL}campus-life/"
HOSTEL_LINK = f"{BASE_URL}hostels/"
CONTACT_LINK = f"{BASE_URL}contact-us/"

# Responses
responses = {
    "greeting": [
        "Hey there! Welcome to VIT Chennai. How can I help you today?",
        "Hello! Ask me anything about VIT Chennai 😊",
    ],
    "farewell": [
        "Goodbye! Feel free to ping me anytime.",
        "Take care! See you soon 👋"
    ],
    "admission": [
        "Admissions are through VITEEE or direct application depending on the program.",
        f"You can apply or get more info here: <a href='{ADMISSION_LINK}' target='_blank' rel='noopener noreferrer'>Apply Here</a>"
    ],
    "courses": [
        "We offer BTech, MTech, MBA, Law, and Science programs.",
        f"Check the complete course list here: <a href='{COURSES_LINK}' target='_blank' rel='noopener noreferrer'>Course List</a>"
    ],
    "fees": [
        "Fees vary by program. BTech is around ₹2.5–3 lakhs/year.",
        f"For full fee details, visit: <a href='{FEE_LINK}' target='_blank' rel='noopener noreferrer'>Fee Structure</a>"
    ],
    "placements": [
        "Top companies like Amazon, Microsoft, and TCS hire from VIT Chennai.",
        f"Placement stats are available here: <a href='{PLACEMENT_LINK}' target='_blank' rel='noopener noreferrer'>Placement Info</a>"
    ],
    "campus": [
        "The campus has modern labs, libraries, hostels, cafes, and sports areas.",
        f"Here's a glimpse: <a href='{CAMPUS_LINK}' target='_blank' rel='noopener noreferrer'>Campus Life</a>"
    ],
    "hostel": [
        f"Separate hostels for boys and girls with AC and non-AC options.There are 4 types of rooms available 2-bed,3-bed,4-bed and 6-bed.For more details you can visit our website: <a href='{HOSTEL_LINK}' target='_blank' rel='noopener noreferrer'>Hostel Info</a>",
        f"More details here:  <a href='{HOSTEL_LINK}' target='_blank' rel='noopener noreferrer'>Hostel Info</a>"
    ],
    "contact": [
        f"You can reach VIT Chennai here: <a href='{CONTACT_LINK}' target='_blank' rel='noopener noreferrer'>Contact Us</a>",
        "Check out the contact page for phone numbers and emails."
    ],
    "vit_info": [
        "VIT is a top-ranked private university with campuses in Chennai, Vellore, and more.",
        "Known for academics, placements, and student-friendly campus life."
    ],
    "vit_quality": [
        "Yes! VIT Chennai is NAAC A++ accredited with great faculty and placements.",
        "Students love the learning environment and infrastructure here!"
    ],
    "casual_how_are_you": [
        "I'm doing great, thanks for asking! How about you?",
        "Running perfectly fine 😁 Ask me anything!"
    ],
    "casual_age": [
        "I was created recently to help students like you!",
        "I'm as old as my last software update ❤️"
    ],
    "casual_creator": [
        "I was developed by a student at VIT Chennai!",
        "A fellow VITian made me with love and code 💻"
    ],
    "casual_name": [
        "You can call me V-Bot 😊",
        "I'm V-Bot, your virtual buddy for VIT Chennai!"
    ],
    "casual_greeting": [
        "I'm just a bot, but I'm feeling helpful today 😊",
        "Doing great! Ready to assist you with anything about VIT.",
        "I’m always up and running for your questions!"
    ],
    "age": [
        "Age is just a number, and I’m timeless 😁",
        "I'm as old as my code – constantly evolving!",
        "Bots don't age, we just update!"
    ],
    "bot_name": [
        "I'm V-Bot, your assistant for everything VIT Chennai!",
        "Call me V-Bot – I help students like you every day.",
        "I'm the virtual guide for VIT Chennai 😊"
    ],
    "bot_identity": [
        "I'm an AI-powered bot, not human – but I try to be friendly!",
        "Not human, but designed to help you like one!",
        "Just a smart assistant here to help you explore VIT Chennai!"
    ],
    "default": [
        "I'm not sure how to answer that. Try asking about courses, fees, or campus life!",
        "Sorry, I didn’t understand that. You can ask about admissions, placements, or say hello!"
    ]
}

# Intent patterns
patterns = {
    "greeting": ["hi", "hello", "hey", "good morning", "good evening", "what's up"],
    "farewell": ["bye", "goodbye", "see you", "take care", "thanks", "thank you", "exit"],
    "admission": ["admission", "how to join", "apply for vit", "enroll", "entrance", "admission process"],
    "courses": ["courses", "programs", "degrees", "branches", "subjects", "departments", "btech"],
    "fees": ["fees", "tuition", "cost", "price", "payment", "structure"],
    "placements": ["placements", "jobs", "recruiters", "salary", "companies", "placement stats"],
    "campus": ["campus", "facilities", "library", "canteen", "sports", "labs", "wifi"],
    "hostel": ["hostel", "rooms", "ac room", "hostel fees", "mess", "laundry"],
    "contact": ["contact", "phone", "email", "helpdesk", "reach", "address"],
    "vit_info": ["what is vit", "about vit", "vit university", "vit chennai", "tell me about vit"],
    "vit_quality": ["is vit good", "how is vit", "vit worth it", "vit ranking", "vit quality"],
    "casual_how_are_you": ["how are you", "how's it going", "you good"],
    "casual_age": ["how old are you", "your age", "when were you made"],
    "casual_creator": ["who made you", "your creator", "who built you", "who developed you"],
    "casual_name": ["what's your name", "your name", "who are you"]
}

matcher = PhraseMatcher(nlp.vocab)
for intent, phrases in patterns.items():
    matcher.add(intent, [nlp(text) for text in phrases])

def understand_intent(user_input):
    doc = nlp(user_input.lower())

    question_map = {
        "how are you": "casual_greeting",
        "how old are you": "age",
        "what is your name": "bot_name",
        "who are you": "bot_name",
        "are you human": "bot_identity"
    }
    for q in question_map:
        if q in user_input.lower():
            return question_map[q]

    matches = matcher(doc)
    if matches:
        return nlp.vocab.strings[matches[0][0]]

    best_score = 0
    best_intent = None
    for intent, phrases in patterns.items():
        for phrase in phrases:
            score = fuzz.partial_ratio(user_input.lower(), phrase)
            if score > best_score:
                best_score = score
                best_intent = intent

    return best_intent if best_score > 75 else None

def generate_response(intent):
    if intent in responses:
        return random.choice(responses[intent])
    return random.choice(responses["default"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_message = request.json.get("message")

    if "chat_history" not in session:
        session["chat_history"] = []

    session["chat_history"].append({"sender": "user", "message": user_message})

    intent = understand_intent(user_message)
    response = generate_response(intent)

    session["chat_history"].append({"sender": "bot", "message": response})
    session["chat_history"] = session["chat_history"][-10:]

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
