# actions.py
from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import os
import requests
from gtts import gTTS
import random
import time


# Basic config
SECURE_API_BASE = os.getenv("SECURE_API_BASE", "http://127.0.0.1:8001")
TTS_OUTPUT_DIR = "tts_responses"
os.makedirs(TTS_OUTPUT_DIR, exist_ok=True)


# OTP settings
OTP_STORE = {}  # In-memory only; use Redis or DB in production
OTP_THRESHOLD_AMOUNT = 5000  # Ask OTP for transfers above this


def generate_otp(user_id: str) -> str:
    """Create a 6-digit OTP and store it with basic metadata."""
    otp = str(random.randint(100000, 999999))
    OTP_STORE[user_id] = {
        "otp": otp,
        "timestamp": time.time(),
        "attempts": 0,
        "max_attempts": 3
    }
    print(f"[OTP] Generated {otp} for user {user_id}")
    return otp


def verify_otp(user_id: str, provided_otp: str) -> bool:
    """Check OTP with 5-min expiry and limited attempts."""
    if user_id not in OTP_STORE:
        print(f"[OTP] No OTP found for user {user_id}")
        return False
    
    stored = OTP_STORE[user_id]
    
    # 5 minutes expiry
    if time.time() - stored["timestamp"] > 300:
        print(f"[OTP] OTP expired for user {user_id}")
        del OTP_STORE[user_id]
        return False
    
    if stored["attempts"] >= stored["max_attempts"]:
        print(f"[OTP] Max attempts exceeded for user {user_id}")
        del OTP_STORE[user_id]
        return False
    
    if stored["otp"] == provided_otp:
        print(f"[OTP] OTP verified successfully for user {user_id}")
        del OTP_STORE[user_id]
        return True
    else:
        OTP_STORE[user_id]["attempts"] += 1
        remaining = stored["max_attempts"] - OTP_STORE[user_id]["attempts"]
        print(f"[OTP] Invalid OTP for user {user_id}. {remaining} attempts remaining")
        return False


def send_otp_sms(user_id: str, otp: str):
    """Mock SMS send; plug in real SMS gateway here."""
    print(f"[SMS] Sending OTP {otp} to user {user_id}")
    return True


# Multilingual templates
TEMPLATES = {
    "greet": {
        "hi": "नमस्ते, मैं सहाया हूं, आपकी वॉइस बैंकिंग सहायक। मैं आपकी कैसे मदद कर सकती हूं?",
        "bn": "নমস্কার, আমি সহায়া, আপনার ভয়েস ব্যাংকিং সহায়ক। আমি আপনাকে কীভাবে সাহায্য করতে পারি?",
        "mr": "नमस्कार, मी सहाया आहे, तुमची व्हॉइस बँकिंग सहाय्यक। मी तुम्हाला कशी मदत करू शकते?",
        "or": "ନମସ୍କାର, ମୁଁ ସହାୟା, ଆପଣଙ୍କର ଭଏସ୍ ବ୍ୟାଙ୍କିଙ୍ଗ ସହାୟକ। ମୁଁ ଆପଣଙ୍କୁ କିପରି ସାହାଯ୍ୟ କରିପାରିବି?",
        "ta": "வணக்கம், நான் சகாயா, உங்கள் குரல் வங்கி உதவியாளர். நான் உங்களுக்கு எப்படி உதவ முடியும்?",
        "te": "నమస్కారం, నేను సహాయ, మీ వాయిస్ బ్యాంకింగ్ సహాయకుడిని. నేను మీకు ఎలా సహాయం చేయగలను?",
        "en": "Hello, I'm SahaYaa, your voice banking assistant. How can I help you today?"
    },
    "goodbye": {
        "hi": "हमारे साथ बैंकिंग करने के लिए धन्यवाद। नमस्ते!",
        "bn": "আমাদের সাথে ব্যাংকিং করার জন্য ধন্যবাদ। বিদায়!",
        "mr": "आमच्यासोबत बँकिंग केल्याबद्दल धन्यवाद। निरोप!",
        "or": "ଆମ ସହିତ ବ୍ୟାଙ୍କିଙ୍ଗ କରିଥିବାରୁ ଧନ୍ୟବାଦ। ବିଦାୟ!",
        "ta": "எங்களுடன் வங்கிச் சேவை பயன்படுத்தியதற்கு நன்றி. பிரியாவிடை!",
        "te": "మాతో బ్యాంకింగ్ చేసినందుకు ధన్యవాదాలు. వీడ్కోలు!",
        "en": "Thanks for banking with us. Goodbye!"
    },
    "balance": {
        "hi": "आपके खाते {account_id} में वर्तमान बैलेंस {balance} रुपये है।",
        "bn": "আপনার অ্যাকাউন্ট {account_id} এর বর্তমান ব্যালেন্স {balance} টাকা।",
        "mr": "तुमच्या खात्यात {account_id} सध्याचे शिल्लक {balance} रुपये आहे।",
        "or": "ଆପଣଙ୍କର ଖାତା {account_id} ରେ ବର୍ତ୍ତମାନ ବାଲାନ୍ସ {balance} ଟଙ୍କା ଅଛି।",
        "ta": "உங்கள் கணக்கு {account_id} இல் தற்போதைய இருப்பு {balance} ரூபாய்.",
        "te": "మీ ఖాతా {account_id} లో ప్రస్తుత బ్యాలెన్స్ {balance} రూపాయలు.",
        "en": "Your current balance in account {account_id} is {balance} rupees."
    },
    # OTP request
    "otp_required": {
        "hi": "सुरक्षा के लिए, हमने आपके पंजीकृत मोबाइल पर 6 अंकों का OTP भेजा है। कृपया OTP बोलें।",
        "bn": "নিরাপত্তার জন্য, আমরা আপনার নিবন্ধিত মোবাইলে 6 সংখ্যার OTP পাঠিয়েছি। অনুগ্রহ করে OTP বলুন।",
        "mr": "सुरक्षिततेसाठी, आम्ही तुमच्या नोंदणीकृत मोबाइलवर 6 अंकी OTP पाठवला आहे। कृपया OTP सांगा।",
        "or": "ସୁରକ୍ଷା ପାଇଁ, ଆମେ ଆପଣଙ୍କର ରେଜିଷ୍ଟର ହୋଇଥିବା ମୋବାଇଲରେ 6 ସଂଖ୍ୟା OTP ପଠାଇଛୁ। ଦୟାକରି OTP କୁହନ୍ତୁ।",
        "ta": "பாதுகாப்புக்காக, உங்கள் பதிவு செய்யப்பட்ட மொபைலுக்கு 6 இலக்க OTP அனுப்பியுள்ளோம். தயவுசெய்து OTP சொல்லுங்கள்.",
        "te": "భద్రత కోసం, మేము మీ నమోదిత మొబైల్‌కు 6 అంకెల OTP పంపాము. దయచేసి OTP చెప్పండి.",
        "en": "For security, we've sent a 6-digit OTP to your registered mobile. Please say the OTP."
    },
    # OTP success
    "otp_verified": {
        "hi": "OTP सत्यापित हो गया। आपका लेन-देन जारी है।",
        "bn": "OTP যাচাই হয়েছে। আপনার লেনদেন প্রক্রিয়াধীন।",
        "mr": "OTP सत्यापित झाला। तुमचा व्यवहार सुरू आहे।",
        "or": "OTP ଯାଚାଇ ହୋଇଛି। ଆପଣଙ୍କର କାରବାର ଜାରି ଅଛି।",
        "ta": "OTP சரிபார்க்கப்பட்டது. உங்கள் பரிவர்த்தனை தொடர்கிறது.",
        "te": "OTP ధృవీకరించబడింది. మీ లావాదేవీ కొనసాగుతోంది.",
        "en": "OTP verified. Processing your transaction."
    },
    # OTP failure
    "otp_failed": {
        "hi": "गलत OTP। कृपया फिर से कोशिश करें या नया OTP के लिए कहें।",
        "bn": "ভুল OTP। অনুগ্রহ করে আবার চেষ্টা করুন বা নতুন OTP চান।",
        "mr": "चुकीचा OTP। कृपया पुन्हा प्रयत्न करा किंवा नवीन OTP मागा।",
        "or": "ଭୁଲ OTP। ଦୟାକରି ପୁନର୍ବାର ଚେଷ୍ଟା କରନ୍ତୁ କିମ୍ବା ନୂତନ OTP ମାଗନ୍ତୁ।",
        "ta": "தவறான OTP. தயவுசெய்து மீண்டும் முயற்சிக்கவும் அல்லது புதிய OTP கேளுங்கள்.",
        "te": "తప్పు OTP. దయచేసి మళ్లీ ప్రయత్నించండి లేదా కొత్త OTP కోరండి.",
        "en": "Incorrect OTP. Please try again or request a new OTP."
    },
    "transfer_success": {
        "hi": "{amount} रुपये {from_account} से {to_account} में सफलतापूर्वक भेजे गए। ट्रांजेक्शन आईडी {tx_id}।",
        "bn": "{amount} টাকা {from_account} থেকে {to_account} এ সফলভাবে পাঠানো হয়েছে। লেনদেন আইডি {tx_id}।",
        "mr": "{amount} रुपये {from_account} पासून {to_account} मध्ये यशस्वीरित्या पाठवले गेले। व्यवहार क्रमांक {tx_id}।",
        "or": "{amount} ଟଙ୍କା {from_account} ରୁ {to_account} କୁ ସଫଳତାର ସହିତ ପଠାଯାଇଛି। କାରବାର ପରିଚୟ {tx_id}।",
        "ta": "{amount} ரூபாய் {from_account} இலிருந்து {to_account} க்கு வெற்றிகரமாக அனுப்பப்பட்டது. பரிவர்த்தனை ஐடி {tx_id}.",
        "te": "{amount} రూపాయలు {from_account} నుండి {to_account} కు విజయవంతంగా పంపబడింది. లావాదేవీ ఐడి {tx_id}.",
        "en": "{amount} rupees transferred successfully from {from_account} to {to_account}. Transaction ID {tx_id}."
    },
    "transactions_header": {
        "hi": "यहाँ आपके हाल के लेन-देन हैं:",
        "bn": "এখানে আপনার সাম্প্রতিক লেনদেন রয়েছে:",
        "mr": "येथे तुमचे अलीकडील व्यवहार आहेत:",
        "or": "ଏଠାରେ ଆପଣଙ୍କର ସାମ୍ପ୍ରତିକ କାରବାର ଅଛି:",
        "ta": "இதோ உங்கள் சமீபத்திய பரிவர்த்தனைகள்:",
        "te": "ఇదిగో మీ ఇటీవలి లావాదేవీలు:",
        "en": "Here are your recent transactions:"
    },
    "transaction_item": {
        "hi": "{amount} रुपये {to_account} को {created_at} को",
        "bn": "{amount} টাকা {to_account} কে {created_at} তারিখে",
        "mr": "{amount} रुपये {to_account} ला {created_at} रोजी",
        "or": "{amount} ଟଙ୍କା {to_account} କୁ {created_at} ରେ",
        "ta": "{amount} ரூபாய் {to_account} க்கு {created_at} அன்று",
        "te": "{amount} రూపాయలు {to_account} కు {created_at} న",
        "en": "{amount} rupees to {to_account} on {created_at}"
    },
    "transactions_empty": {
        "hi": "खाते {from_account} के लिए कोई हाल का लेन-देन नहीं मिला।",
        "bn": "অ্যাকাউন্ট {from_account} এর জন্য কোনো সাম্প্রতিক লেনদেন পাওয়া যায়নি।",
        "mr": "खाते {from_account} साठी कोणतेही अलीकडील व्यवहार आढळले नाहीत।",
        "or": "ଖାତା {from_account} ପାଇଁ କୌଣସି ସାମ୍ପ୍ରତିକ କାରବାର ମିଳିଲା ନାହିଁ।",
        "ta": "கணக்கு {from_account} க்கான சமீபத்திய பரிவர்த்தனைகள் எதுவும் இல்லை.",
        "te": "ఖాతా {from_account} కోసం ఇటీవలి లావాదేవీలు ఏవీ కనుగొనబడలేదు.",
        "en": "No recent transactions found for account {from_account}."
    },
    "bill_payment_success": {
        "hi": "आपका {amount} रुपये का बिल {from_account} से भुगतान हो गया है। ट्रांजेक्शन आईडी {tx_id}।",
        "bn": "আপনার {amount} টাকার বিল {from_account} থেকে পরিশোধ করা হয়েছে। লেনদেন আইডি {tx_id}।",
        "mr": "तुमचे {amount} रुपयांचे बिल {from_account} मधून भरले गेले आहे। व्यवहार क्रमांक {tx_id}।",
        "or": "ଆପଣଙ୍କର {amount} ଟଙ୍କାର ବିଲ୍ {from_account} ରୁ ପରିଶୋଧ କରାଯାଇଛି। କାରବାର ପରିଚୟ {tx_id}।",
        "ta": "உங்கள் {amount} ரூபாய் கட்டணம் {from_account} இலிருந்து செலுத்தப்பட்டது. பரிவர்த்தனை ஐடி {tx_id}.",
        "te": "మీ {amount} రూపాయల బిల్లు {from_account} నుండి చెల్లించబడింది. లావాదేవీ ఐడి {tx_id}.",
        "en": "Your bill of {amount} rupees has been paid from {from_account}. Transaction ID {tx_id}."
    },
    "loan_info": {
        "hi": "आप वर्तमान में प्रति वर्ष 11.5% ब्याज दर पर 2,50,000 रुपये तक के पूर्व-स्वीकृत व्यक्तिगत ऋण के लिए पात्र हैं।",
        "bn": "আপনি বর্তমানে বছরে 11.5% সুদের হারে 2,50,000 টাকা পর্যন্ত পূর্ব-অনুমোদিত ব্যক্তিগত ঋণের জন্য যোগ্য।",
        "mr": "तुम्ही सध्या वार्षिक 11.5% व्याज दराने 2,50,000 रुपयांपर्यंत पूर्व-मंजूर वैयक्तिक कर्जासाठी पात्र आहात।",
        "or": "ଆପଣ ବର୍ତ୍ତମାନ ବାର୍ଷିକ 11.5% ସୁଧ ହାରରେ 2,50,000 ଟଙ୍କା ପର୍ଯ୍ୟନ୍ତ ପୂର୍ବ-ଅନୁମୋଦିତ ବ୍ୟକ୍ତିଗତ ଋଣ ପାଇଁ ଯୋଗ୍ୟ ଅଟନ୍ତି।",
        "ta": "நீங்கள் தற்போது ஆண்டுக்கு 11.5% வட்டி விகிதத்தில் 2,50,000 ரூபாய் வரை முன்-அனுமதிக்கப்பட்ட தனிப்பட்ட கடனுக்கு தகுதியானவர்.",
        "te": "మీరు ప్రస్తుతం సంవత్సరానికి 11.5% వడ్డీ రేటుతో 2,50,000 రూపాయల వరకు ముందస్తు-ఆమోదించబడిన వ్యక్తిగత రుణానికి అర్హులు.",
        "en": "You are currently eligible for a pre-approved personal loan up to 2,50,000 rupees at 11.5% per annum."
    },
    "credit_limit": {
        "hi": "आपकी वर्तमान क्रेडिट कार्ड सीमा 75,000 रुपये है। उपलब्ध सीमा 52,300 रुपये है।",
        "bn": "আপনার বর্তমান ক্রেডিট কার্ড সীমা 75,000 টাকা। উপলব্ধ সীমা 52,300 টাকা।",
        "mr": "तुमची सध्याची क्रेडिट कार्ड मर्यादा 75,000 रुपये आहे। उपलब्ध मर्यादा 52,300 रुपये आहे।",
        "or": "ଆପଣଙ୍କର ବର୍ତ୍ତମାନ କ୍ରେଡିଟ୍ କାର୍ଡ ସୀମା 75,000 ଟଙ୍କା। ଉପଲବ୍ଧ ସୀമା 52,300 ଟଙ୍କା।",
        "ta": "உங்கள் தற்போதைய கடன் அட்டை வரம்பு 75,000 ரூபாய். கிடைக்கக்கூடிய வரம்பு 52,300 ரூபாய்.",
        "te": "మీ ప్రస్తుత క్రెడిట్ కార్డ్ పరిమితి 75,000 రూపాయలు. అందుబాటులో ఉన్న పరిమితి 52,300 రూపాయలు.",
        "en": "Your current credit card limit is 75,000 rupees. Available limit is 52,300 rupees."
    },
    "reminder_set": {
        "hi": "ठीक है, मैंने आपके भुगतान के लिए एक अनुस्मारक सेट कर दिया है। मैं आपको नियत तारीख पर सूचित करूंगी।",
        "bn": "ঠিক আছে, আমি আপনার পেমেন্টের জন্য একটি রিমাইন্ডার সেট করেছি। আমি আপনাকে নির্ধারিত তারিখে জানাব।",
        "mr": "ठीक आहे, मी तुमच्या पेमेंटसाठी एक स्मरणपत्र सेट केले आहे। मी तुम्हाला नियत तारखेला सूचित करेन।",
        "or": "ଠିକ୍ ଅଛି, ମୁଁ ଆପଣଙ୍କର ପେମେଣ୍ଟ ପାଇଁ ଏକ ସ୍ମାରକ ସେଟ୍ କରିଛି। ମୁଁ ଆପଣଙ୍କୁ ନିର୍ଦ୍ଧାରିତ ତାରିଖରେ ସୂଚିତ କରିବି।",
        "ta": "சரி, உங்கள் பணம் செலுத்துவதற்கான நினைவூட்டலை அமைத்துவிட்டேன். நிர்ணயிக்கப்பட்ட தேதியில் உங்களுக்கு தெரிவிப்பேன்.",
        "te": "సరే, నేను మీ చెల్లింపు కోసం రిమైండర్‌ను సెట్ చేసాను. నిర్ణీత తేదీన మీకు తెలియజేస్తాను.",
        "en": "Okay, I've set a reminder for your payment. I'll notify you on the due date."
    },
    "error_balance": {
        "hi": "क्षमा करें, मैं अभी आपका बैलेंस नहीं दिखा सकती। कृपया फिर से प्रयास करें।",
        "bn": "দুঃখিত, আমি এখন আপনার ব্যালেন্স দেখাতে পারছি না। অনুগ্রহ করে আবার চেষ্টা করুন।",
        "mr": "क्षमस्व, मी सध्या तुमचे शिल्लक दाखवू शकत नाही। कृपया पुन्हा प्रयत्न करा।",
        "or": "କ୍ଷମା କରନ୍ତୁ, ମୁଁ ବର୍ତ୍ତମାନ ଆପଣଙ୍କର ବାଲାନ୍ସ ଦେଖାଇ ପାରୁନାହିଁ। ଦୟାକରି ପୁନର୍ବାର ଚେଷ୍ଟା କରନ୍ତୁ।",
        "ta": "மன்னிக்கவும், இப்போது உங்கள் இருப்பைக் காட்ட முடியவில்லை. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.",
        "te": "క్షమించండి, ప్రస్తుతం మీ బ్యాలెన్స్‌ను చూపించలేకపోతున్నాను. దయచేసి మళ్లీ ప్రయత్నించండి.",
        "en": "Sorry, I couldn't fetch your balance right now. Please try again."
    },
    "error_transfer": {
        "hi": "क्षमా करें, मैं अभी स्थानांतरण पूरा नहीं कर सकती।",
        "bn": "দুঃখিত, আমি এখন স্থানান্তর সম্পূর্ণ করতে পারছি না।",
        "mr": "क्षमस्व, मी सध्या हस्तांतरण पूर्ण करू शकत नाही।",
        "or": "କ୍ଷମା କରନ୍ତୁ, ମୁଁ ବର୍ତ୍ତମାନ ସ୍ଥାନାନ୍ତରଣ ସମ୍ପୂର୍ଣ୍ଣ କରିପାରୁନାହିଁ।",
        "ta": "மன்னிக்கவும், இப்போது பரிமாற்றத்தை முடிக்க முடியவில்லை.",
        "te": "క్షమించండి, ప్రస్తుతం బదిలీని పూర్తి చేయలేకపోతున్నాను.",
        "en": "Sorry, I couldn't complete the transfer right now."
    },
    "error_transactions": {
        "hi": "क्षमा करें, मैं आपके हाल के लेन-देन नहीं दिखा सकती।",
        "bn": "দুঃখিত, আমি আপনার সাম্প্রতিক লেনদেন দেখাতে পারছি না।",
        "mr": "क्षमस्व, मी तुमचे अलीकडील व्यवहार दाखवू शकत नाही।",
        "or": "କ୍ଷମା କରନ୍ତୁ, ମୁଁ ଆପଣଙ୍କର ସାମ୍ପ୍ରତିକ କାରବାର ଦେଖାଇ ପାରୁନାହିଁ।",
        "ta": "மன்னிக்கவும், உங்கள் சமீபத்திய பரிவர்த்தனைகளைக் காட்ட முடியவில்லை.",
        "te": "క్షమించండి, మీ ఇటీవలి లావాదేవీలను చూపించలేకపోతున్నాను.",
        "en": "Sorry, I couldn't fetch your recent transactions."
    },
    "error_bill_payment": {
        "hi": "क्षमा करें, मैं अभी आपका बिल भुगतान नहीं कर सकती।",
        "bn": "দুঃখিত, আমি এখন আপনার বিল পরিশোধ করতে পারছি না।",
        "mr": "क्षमस्व, मी सध्या तुमचे बिल भरू शकत नाही।",
        "or": "କ୍ଷମା କରନ୍ତୁ, ମୁଁ ବର୍ତ୍ତମାନ ଆପଣଙ୍କର ବିଲ୍ ପରିଶୋଧ କରିପାରୁନାହିଁ।",
        "ta": "மன்னிக்கவும், இப்போது உங்கள் கட்டணத்தைச் செலுத்த முடியவில்லை.",
        "te": "క్షమించండి, ప్రస్తుతం మీ బిల్లును చెల్లించలేకపోతున్నాను.",
        "en": "Sorry, I couldn't pay your bill right now."
    },
    "out_of_scope": {
        "hi": "मैं अभी इसमें मदद नहीं कर सकती। आप मुझसे बैलेंस, ट्रांसफर, बिल, लोन और रिमाइंडर के बारे में पूछ सकते हैं।",
        "bn": "আমি এখনও এতে সাহায্য করতে পারছি না। আপনি আমাকে ব্যালেন্স, ট্রান্সফার, বিল, লোন এবং রিমাইন্ডার সম্পর্কে জিজ্ঞাসা করতে পারেন।",
        "mr": "मी अद्याप यात मदत करू शकत नाही। तुम्ही मला शिल्लक, हस्तांतरण, बिल, कर्ज आणि स्मरणपत्रांबद्दल विचारू शकता।",
        "or": "ମୁଁ ଏପର୍ଯ୍ୟନ୍ତ ଏଥିରେ ସାହାଯ୍ୟ କରିପାରୁନାହିଁ। ଆପଣ ମୋତେ ବାଲାନ୍ସ, ସ୍ଥାନାନ୍ତରଣ, ବିଲ୍, ଋଣ ଏବଂ ସ୍ମାରକ ବିଷୟରେ ପଚାରିପାରିବେ।",
        "ta": "இதில் என்னால் இன்னும் உதவ முடியவில்லை. இருப்பு, பரிமாற்றம், கட்டணம், கடன் மற்றும் நினைவூட்டல் பற்றி என்னிடம் கேட்கலாம்.",
        "te": "నేను ఇంకా దీనిలో సహాయం చేయలేను. మీరు నన్ను బ్యాలెన్స్, బదిలీ, బిల్లు, రుణం మరియు రిమైండర్ల గురించి అడగవచ్చు.",
        "en": "I'm not able to help with that yet. You can ask me about balance, transfers, bills, loans, and reminders."
    },
    "ask_rephrase": {
        "hi": "मैं इसे ठीक से समझ नहीं पाई। क्या आप इसे दूसरे तरीके से कह सकते हैं?",
        "bn": "আমি এটা ঠিকমতো বুঝতে পারিনি। আপনি কি এটা অন্যভাবে বলতে পারেন?",
        "mr": "मला हे नीट समजले नाही। तुम्ही हे वेगळ्या पद्धतीने सांगू शकता का?",
        "or": "ମୁଁ ଏହାକୁ ଠିକ୍ ଭାବରେ ବୁଝିପାରିଲି ନାହିଁ। ଆପଣ ଏହାକୁ ଅନ୍ୟ ଉପାୟରେ କହିପାରିବେ କି?",
        "ta": "நான் இதை சரியாகப் புரிந்துகொள்ளவில்லை. இதை வேறு விதமாகச் சொல்ல முடியுமா?",
        "te": "నేను దీన్ని సరిగ్గా అర్థం చేసుకోలేకపోయాను. మీరు దీన్ని వేరే విధంగా చెప్పగలరా?",
        "en": "I couldn't quite catch that. Could you please say it again in a different way?"
    }
}


# Helpers
def get_template(action: Text, lang: Text) -> Text:
    """Return text template for a given action and language."""
    if action in TEMPLATES:
        return TEMPLATES[action].get(lang, TEMPLATES[action].get("en", ""))
    return ""


def _map_lang_to_tts(lang: Text) -> Text:
    """Map internal lang codes to gTTS codes."""
    mapping = {
        "hi": "hi",
        "bn": "bn",
        "mr": "mr",
        "or": "or",
        "ta": "ta",
        "te": "te",
        "en": "en"
    }
    return mapping.get(lang, "hi")


def synthesize_tts(text: Text, lang: Text, action_name: Text) -> Text:
    """Generate an mp3 file for the reply and return its path."""
    tts_lang = _map_lang_to_tts(lang)
    filename = f"{action_name}_{lang}.mp3"
    out_path = os.path.join(TTS_OUTPUT_DIR, filename)
    
    try:
        tts = gTTS(text=text, lang=tts_lang)
        tts.save(out_path)
        return out_path
    except Exception as e:
        print(f"[TTS ERROR] {e}")
        return ""


def _get_auth_from_metadata(tracker: Tracker) -> Dict[Text, Any]:
    """Read auth block from message metadata; fall back to sender_id."""
    meta = tracker.latest_message.get("metadata") or {}
    auth = meta.get("auth") or {}
    if "user_id" not in auth or not auth["user_id"]:
        auth["user_id"] = tracker.sender_id or "cust_demo"
    return auth


def _get_lang_from_metadata(tracker: Tracker) -> Text:
    """Pick language code from metadata, default to Hindi."""
    meta = tracker.latest_message.get("metadata") or {}
    return meta.get("lang", "hi")


# Rasa actions
class ActionCheckBalance(Action):
    def name(self) -> Text:
        return "action_check_balance"


    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        auth = _get_auth_from_metadata(tracker)
        user_id = auth.get("user_id", tracker.sender_id or "cust_demo")
        lang = _get_lang_from_metadata(tracker)
        account_id = tracker.get_slot("account_id") or "acct_savings_1"

        payload = {
            "user_id": user_id,
            "account_id": account_id,
            "auth": auth,
        }

        try:
            resp = requests.post(f"{SECURE_API_BASE}/balance/", json=payload, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            balance = data.get("balance")
            currency = data.get("currency", "INR")

            template = get_template("balance", lang)
            bot_text = template.format(account_id=account_id, balance=balance, currency=currency)
            
            audio_path = synthesize_tts(bot_text, lang, "balance_reply")
            
            if audio_path:
                dispatcher.utter_message(
                    text=bot_text,
                    json_message={
                        "type": "audio_reply",
                        "audio_file": audio_path,
                        "lang": lang
                    }
                )
            else:
                dispatcher.utter_message(text=bot_text)

            return [
                SlotSet("user_id", user_id),
                SlotSet("account_id", account_id),
            ]
        except Exception as e:
            error_text = get_template("error_balance", lang)
            dispatcher.utter_message(text=error_text)
            
            audio_path = synthesize_tts(error_text, lang, "balance_error")
            if audio_path:
                dispatcher.utter_message(
                    json_message={
                        "type": "audio_reply",
                        "audio_file": audio_path,
                        "lang": lang
                    }
                )
            print("[ACTION] action_check_balance error:", repr(e))
            return []


class ActionMakeTransfer(Action):
    def name(self) -> Text:
        return "action_make_transfer"


    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        auth = _get_auth_from_metadata(tracker)
        user_id = auth.get("user_id", tracker.sender_id or "cust_demo")
        lang = _get_lang_from_metadata(tracker)

        from_account = tracker.get_slot("from_account") or "acct_savings_1"
        to_account = tracker.get_slot("to_account") or "acct_friend_riya"

        # Amount handling
        amount = tracker.get_slot("amount")

        if not amount or amount == 0:
            user_message = tracker.latest_message.get('text', '')
            print(f"[DEBUG] Slot empty, extracting from text: {user_message}")

            numbers = re.findall(r'\d+', user_message)
            if numbers:
                amount = numbers[0]
                print(f"[DEBUG] Extracted amount from text: {amount}")
            else:
                amount = 500
                print(f"[DEBUG] No amount found, using default: {amount}")

        if isinstance(amount, str):
            try:
                amount = float(amount.replace(',', '').strip())
                print(f"[DEBUG] Converted string to float: {amount}")
            except (ValueError, TypeError):
                print(f"[DEBUG] Conversion failed, using default 500")
                amount = 500.0
        elif isinstance(amount, int):
            amount = float(amount)
            print(f"[DEBUG] Converted int to float: {amount}")
        elif not isinstance(amount, float):
            print(f"[DEBUG] Unknown type {type(amount)}, using default 500")
            amount = 500.0

        print(f"[DEBUG] Final amount: {amount} (type: {type(amount).__name__})")

        currency = tracker.get_slot("currency") or "INR"
        
        # Check if OTP is needed
        if amount > OTP_THRESHOLD_AMOUNT:
            otp_verified = tracker.get_slot("otp_verified")
            
            if not otp_verified:
                print(f"[OTP] Amount {amount} > {OTP_THRESHOLD_AMOUNT}, requesting OTP")
                
                otp = generate_otp(user_id)
                send_otp_sms(user_id, otp)
                
                bot_text = get_template("otp_required", lang)
                dispatcher.utter_message(text=bot_text)
                
                audio_path = synthesize_tts(bot_text, lang, "otp_request")
                if audio_path:
                    dispatcher.utter_message(
                        json_message={
                            "type": "audio_reply",
                            "audio_file": audio_path,
                            "lang": lang
                        }
                    )
                
                return [
                    SlotSet("pending_transfer_amount", amount),
                    SlotSet("pending_transfer_from", from_account),
                    SlotSet("pending_transfer_to", to_account),
                    SlotSet("pending_transfer_currency", currency),
                    SlotSet("awaiting_otp", True),
                ]
        else:
            print(f"[TRANSFER] Amount {amount} <= {OTP_THRESHOLD_AMOUNT}, no OTP needed")
        
        payload = {
            "user_id": user_id,
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount,
            "currency": currency,
            "auth": auth,
            "note": "voice_upi_transfer",
        }

        try:
            print(f"[TRANSFER] Initiating transfer: {amount} {currency} from {from_account} to {to_account}")
            resp = requests.post(f"{SECURE_API_BASE}/transfer/", json=payload, timeout=8)
            resp.raise_for_status()
            data = resp.json()
            tx_id = data.get("tx_id", "N/A")

            template = get_template("transfer_success", lang)
            bot_text = template.format(
                amount=int(amount),
                from_account=from_account,
                to_account=to_account,
                tx_id=tx_id
            )
            
            dispatcher.utter_message(text=bot_text)
            
            audio_path = synthesize_tts(bot_text, lang, "transfer_reply")
            if audio_path:
                dispatcher.utter_message(
                    json_message={
                        "type": "audio_reply",
                        "audio_file": audio_path,
                        "lang": lang
                    }
                )

            print(f"[TRANSFER] Success! TX ID: {tx_id}")

            return [
                SlotSet("user_id", user_id),
                SlotSet("from_account", from_account),
                SlotSet("to_account", to_account),
                SlotSet("amount", amount),
                SlotSet("currency", currency),
                SlotSet("last_tx_id", tx_id),
                SlotSet("last_tx_token", data.get("signed_token")),
                SlotSet("otp_verified", False),
                SlotSet("awaiting_otp", False),
                SlotSet("pending_transfer_amount", None),
                SlotSet("pending_transfer_from", None),
                SlotSet("pending_transfer_to", None),
            ]
        except Exception as e:
            print(f"[ACTION] action_make_transfer error: {repr(e)}")
            error_text = get_template("error_transfer", lang)
            dispatcher.utter_message(text=error_text)
            
            audio_path = synthesize_tts(error_text, lang, "transfer_error")
            if audio_path:
                dispatcher.utter_message(
                    json_message={
                        "type": "audio_reply",
                        "audio_file": audio_path,
                        "lang": lang
                    }
                )
            return []


class ActionVerifyOTP(Action):
    def name(self) -> Text:
        return "action_verify_otp"


    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        auth = _get_auth_from_metadata(tracker)
        user_id = auth.get("user_id", tracker.sender_id or "cust_demo")
        lang = _get_lang_from_metadata(tracker)
        
        user_message = tracker.latest_message.get("text", "")
        provided_otp = ''.join(filter(str.isdigit, user_message))
        
        print(f"[OTP] User {user_id} provided OTP: {provided_otp}")
        
        if verify_otp(user_id, provided_otp):
            bot_text = get_template("otp_verified", lang)
            dispatcher.utter_message(text=bot_text)
            
            audio_path = synthesize_tts(bot_text, lang, "otp_success")
            if audio_path:
                dispatcher.utter_message(
                    json_message={
                        "type": "audio_reply",
                        "audio_file": audio_path,
                        "lang": lang
                    }
                )
            
            amount = tracker.get_slot("pending_transfer_amount")
            from_account = tracker.get_slot("pending_transfer_from")
            to_account = tracker.get_slot("pending_transfer_to")
            currency = tracker.get_slot("pending_transfer_currency") or "INR"
            
            return [
                SlotSet("otp_verified", True),
                SlotSet("awaiting_otp", False),
                SlotSet("amount", amount),
                SlotSet("from_account", from_account),
                SlotSet("to_account", to_account),
                SlotSet("currency", currency),
            ]
        else:
            bot_text = get_template("otp_failed", lang)
            dispatcher.utter_message(text=bot_text)
            
            audio_path = synthesize_tts(bot_text, lang, "otp_failed")
            if audio_path:
                dispatcher.utter_message(
                    json_message={
                        "type": "audio_reply",
                        "audio_file": audio_path,
                        "lang": lang
                    }
                )
            
            return [
                SlotSet("otp_verified", False),
            ]


class ActionGetTransactions(Action):
    def name(self) -> Text:
        return "action_get_transactions"


    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        auth = _get_auth_from_metadata(tracker)
        user_id = auth.get("user_id", tracker.sender_id or "cust_demo")
        lang = _get_lang_from_metadata(tracker)
        from_account = tracker.get_slot("from_account") or "acct_savings_1"

        payload = {
            "user_id": user_id,
            "from_account": from_account,
            "auth": auth,
        }

        try:
            resp = requests.post(f"{SECURE_API_BASE}/transactions/", json=payload, timeout=8)
            resp.raise_for_status()
            data = resp.json()
            items = data.get("items", [])

            if not items:
                template = get_template("transactions_empty", lang)
                bot_text = template.format(from_account=from_account)
                dispatcher.utter_message(text=bot_text)
                
                audio_path = synthesize_tts(bot_text, lang, "transactions_empty")
                if audio_path:
                    dispatcher.utter_message(
                        json_message={
                            "type": "audio_reply",
                            "audio_file": audio_path,
                            "lang": lang
                        }
                    )
                return []

            header = get_template("transactions_header", lang)
            item_template = get_template("transaction_item", lang)
            
            lines = [header]
            for tx in items[:3]:
                line = item_template.format(
                    amount=tx.get("amount"),
                    to_account=tx.get("to_account"),
                    created_at=tx.get("created_at")
                )
                lines.append(line)
            
            bot_text = " ".join(lines)
            dispatcher.utter_message(text=bot_text)
            
            audio_path = synthesize_tts(bot_text, lang, "transactions_reply")
            if audio_path:
                dispatcher.utter_message(
                    json_message={
                        "type": "audio_reply",
                        "audio_file": audio_path,
                        "lang": lang
                    }
                )

            return [
                SlotSet("user_id", user_id),
                SlotSet("from_account", from_account),
            ]
        except Exception as e:
            error_text = get_template("error_transactions", lang)
            dispatcher.utter_message(text=error_text)
            
            audio_path = synthesize_tts(error_text, lang, "transactions_error")
            if audio_path:
                dispatcher.utter_message(
                    json_message={
                        "type": "audio_reply",
                        "audio_file": audio_path,
                        "lang": lang
                    }
                )
            print("[ACTION] action_get_transactions error:", repr(e))
            return []


class ActionPayBill(Action):
    def name(self) -> Text:
        return "action_pay_bill"


    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        auth = _get_auth_from_metadata(tracker)
        user_id = auth.get("user_id", tracker.sender_id or "cust_demo")
        lang = _get_lang_from_metadata(tracker)

        from_account = tracker.get_slot("from_account") or "acct_savings_1"
        amount = tracker.get_slot("amount") or 500
        currency = tracker.get_slot("currency") or "INR"

        payload = {
            "user_id": user_id,
            "from_account": from_account,
            "amount": amount,
            "currency": currency,
            "auth": auth,
            "biller_id": "demo_electricity_board",
        }

        try:
            resp = requests.post(f"{SECURE_API_BASE}/paybill/", json=payload, timeout=8)
            resp.raise_for_status()
            data = resp.json()
            tx_id = data.get("tx_id", "N/A")

            template = get_template("bill_payment_success", lang)
            bot_text = template.format(
                amount=amount,
                from_account=from_account,
                tx_id=tx_id
            )
            
            dispatcher.utter_message(text=bot_text)
            
            audio_path = synthesize_tts(bot_text, lang, "paybill_reply")
            if audio_path:
                dispatcher.utter_message(
                    json_message={
                        "type": "audio_reply",
                        "audio_file": audio_path,
                        "lang": lang
                    }
                )

            return [
                SlotSet("user_id", user_id),
                SlotSet("from_account", from_account),
                SlotSet("amount", amount),
                SlotSet("currency", currency),
                SlotSet("last_tx_id", tx_id),
            ]
        except Exception as e:
            error_text = get_template("error_bill_payment", lang)
            dispatcher.utter_message(text=error_text)
            
            audio_path = synthesize_tts(error_text, lang, "paybill_error")
            if audio_path:
                dispatcher.utter_message(
                    json_message={
                        "type": "audio_reply",
                        "audio_file": audio_path,
                        "lang": lang
                    }
                )
            print("[ACTION] action_pay_bill error:", repr(e))
            return []


class ActionLoanInfo(Action):
    def name(self) -> Text:
        return "action_loan_info"


    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        lang = _get_lang_from_metadata(tracker)
        bot_text = get_template("loan_info", lang)
        
        dispatcher.utter_message(text=bot_text)
        
        audio_path = synthesize_tts(bot_text, lang, "loan_info_reply")
        if audio_path:
            dispatcher.utter_message(
                json_message={
                    "type": "audio_reply",
                    "audio_file": audio_path,
                    "lang": lang
                }
            )
        
        return []


class ActionCreditLimit(Action):
    def name(self) -> Text:
        return "action_credit_limit"


    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        lang = _get_lang_from_metadata(tracker)
        bot_text = get_template("credit_limit", lang)
        
        dispatcher.utter_message(text=bot_text)
        
        audio_path = synthesize_tts(bot_text, lang, "credit_limit_reply")
        if audio_path:
            dispatcher.utter_message(
                json_message={
                    "type": "audio_reply",
                    "audio_file": audio_path,
                    "lang": lang
                }
            )
        
        return []


class ActionSetReminder(Action):
    def name(self) -> Text:
        return "action_set_reminder"


    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        lang = _get_lang_from_metadata(tracker)
        bot_text = get_template("reminder_set", lang)
        
        dispatcher.utter_message(text=bot_text)
        
        audio_path = synthesize_tts(bot_text, lang, "reminder_reply")
        if audio_path:
            dispatcher.utter_message(
                json_message={
                    "type": "audio_reply",
                    "audio_file": audio_path,
                    "lang": lang
                }
            )
        
        return []
