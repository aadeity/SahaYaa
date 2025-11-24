

***

<div align="center">

# 🏦 SahaYaa
### AI-Powered Multilingual Voice Banking Assistant

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white(httpsa](https://img.shields.io/badge/Rasa-3.6-5A17EE?style=for-the-badge&logo=rasa&logoColor=white(httpstAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi&logoColor=white(httpsorch](https://img.shields.io/badge/PyTorch-2.1-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white(httpsense: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge(httpsHub stars](https://img.shields.io/github/stars/yourusername/sahayaa?style=for-the-badge(https://github.com/yourusername/sahayaa/stargazers
[![GitHub issues](https://img.shields.io/github/issues/yourusername/sahayaa?style=for-the-badge(https://github.com/yourusername/sahayaa/issues
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge(http Live Demo](#-demo-video) -  [📖 Documentation](#-getting-started) -  [🎯 Features](#-features) -  [🤝 Contribute](#-contributing)**

<img src="https://your-demo-gif-url.gif" alt="SahaYaa Demo" width="600px"/>

***

### *Breaking language barriers in digital banking with voice-first AI*
</div>

***

## 📋 Table of Contents

- [🌟 Project Overview](#-project-overview)
- [💡 Why SahaYaa?](#-why-sahayaa)
- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Getting Started](#-getting-started)
- [💻 Usage](#-usage)
- [🎥 Demo Video](#-demo-video)
- [🏗️ Architecture](#️-architecture)
- [🗺️ Roadmap](#️-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [🙏 Acknowledgements](#-acknowledgements)

***

## 🌟 Project Overview

**SahaYaa** (सहाया - *meaning "help" in Hindi*) is an intelligent voice-first banking assistant designed to democratize digital banking across India's linguistic diversity. Built with state-of-the-art NLP and speech technologies, SahaYaa enables seamless banking operations through natural voice conversations in **8 languages**.

### 🎯 What Problem Does It Solve?

- **Digital Divide**: 🇮🇳 Only 22% of Indians speak English, yet most banking apps require it
- **Accessibility**: 👨‍🦯 Voice-first design helps visually impaired and elderly users
- **Complexity**: 🔢 Eliminates complex UIs - just speak naturally
- **Trust**: 🔐 Multi-layer authentication builds user confidence

### 👥 Who It's For

- 🏘️ **Rural Banking Customers** - Limited digital literacy
- 👴 **Senior Citizens** - Prefer voice over typing
- ♿ **Differently-abled Users** - Screen-reader friendly
- 🚀 **Tech-savvy Users** - Faster than traditional banking apps

***

## 💡 Why SahaYaa?

### 🎨 What Sets Us Apart

| Feature             | Traditional Apps | SahaYaa                       |
|---------------------|-----------------|-------------------------------|
| **Language Support**| 2-3 languages   | **8 languages** (7 Indian + English) |
| **Interaction**     | Touch/Type      | **Voice-first**               |
| **Learning Curve**  | Complex UI      | **Zero learning curve**       |
| **Accessibility**   | Limited         | **Fully accessible**          |
| **Security**        | OTP only        | **Biometric + OTP**           |
| **Offline Support** | Needs internet  | **Hybrid mode** (planned)     |

### 🔥 Unique Features

1. **🎤 Indic ASR Excellence** - Powered by AI4Bharat's IndicConformer (600M parameters)
2. **🧠 Context-Aware NLU** - Understands code-mixed speech (Hinglish, Tanglish, etc.)
3. **🔐 Smart Security** - Conditional OTP for high-value transactions (>₹5000)
4. **🎭 Natural Conversations** - Handles follow-ups, corrections, and clarifications
5. **📊 Real-time Feedback** - Voice + visual confirmation for critical operations

***

## ✨ Features

<table>
<tr>
<td width="50%">
### 🏦 Banking Operations
- ✅ **Balance Inquiry**
- ✅ **Money Transfer**
- ✅ **Bill Payments**
- ✅ **Transaction History**
- ✅ **Loan Inquiries**
- ✅ **Credit Limit**
</td>
<td width="50%">
### 🔒 Security Features
- 🔐 **Multi-Factor Auth**
- 👤 **Liveness Detection**
- 🚨 **Risk-based OTP**
- 🔑 **Session Management**
- 📝 **Audit Logging**
- 🛡️ **CORS Protection**
</td>
</tr>
<tr>
<td width="50%">
### 🌐 Multilingual Support
- 🇮🇳 **Hindi** (हिंदी)
- 🇮🇳 **Bengali** (বাংলা)
- 🇮🇳 **Marathi** (मराठी)
- 🇮🇳 **Odia** (ଓଡ଼ିଆ)
- 🇮🇳 **Tamil** (தமிழ்)
- 🇮🇳 **Telugu** (తెలుగు)
- 🇬🇧 **English**
</td>
<td width="50%">
### 🤖 AI/ML Features
- 🎙️ **Automatic Speech Recognition**
- 🔊 **Text-to-Speech** (Multilingual)
- 🧠 **Intent Classification** (13+ intents)
- 🏷️ **Entity Extraction**
- 📈 **Context Tracking**
- 🔄 **Fallback Handling**
</td>
</tr>
</table>

***

## 🛠️ Tech Stack

### **Core Technologies**

<div align="center">

| **Category**        | **Technology**                                         | **Version** | **Purpose**                       |
|:-------------------:|:------------------------------------------------------:|:-----------:|:----------------------------------:|
| **🤖 NLU Engine**   | ![Rasa](https://img.shields.io/badge/Rasa-5A17EE?logo=rasa&logoColor=white     | 3.6.13      | Intent classification & dialogue   |
| **🎙️ ASR**         | ![AI4Bharat](https://img.shields.io/badge/IndicConformer-FF6B35?logo=python&logoColor=white  | 600M      | Speech-to-text (8 languages)       |
| **🔊 TTS**          | ![gTTS](https://img.shields.io/badge/Google_TTS-4285F4?logo=google&logoColor=white          | 2.4.0      | Text-to-speech synthesis           |
| **🌐 API Framework**| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white         | 0.104      | Voice API gateway                  |
| **🧠 ML Framework** | ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white         | 2.1.0      | ASR model inference                |
| **💾 ML Ops**       | ![Transformers](https://img.shields.io/badge/🤗_Transformers-FFD21E?logoColor=black        | 4.35.0     | Model loading & inference          |
| **🎨 Frontend**     | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white              | -          | Web interface                      |
| **🔧 Audio**        | ![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?logo=ffmpeg&logoColor=white           | Latest     | Audio processing                   |

</div>

### Development Stack

Language: Python 3.10  
NLU Pipeline: RegexFeaturizer → DIETClassifier → TEDPolicy  
ASR Model: ai4bharat/indic-conformer-600m-multilingual  
Dialogue: Rasa 3.6 (Rule + ML policies)  
Server: Uvicorn (ASGI)  
Audio Format: WebM → WAV (16kHz mono)  

***

## 🚀 Getting Started

### 📋 Prerequisites

- Python 3.10 or higher
- 8GB+ RAM
- ffmpeg installed ([Guide](https://ffmpeg.org/download.html))
- Git for version control

### ⚡ Quick Installation

```sh
git clone https://github.com/yourusername/sahayaa.git
cd sahayaa
python -m venv venv310
source venv310/bin/activate # Windows: venv310\Scripts\activate
pip install -r requirements.txt
rasa train  # First time only
```

### 🎬 Running SahaYaa

Open **3 terminals** for:

**Terminal 1: Action Server**  
```
rasa run actions
```

**Terminal 2: Rasa Server**  
```
rasa run --enable-api --cors "*" -p 5005
```

**Terminal 3: Voice API**  
```
python voice_api.py
```

### 🌐 Access the App

[http://127.0.0.1:3000/#chat](http://127.0.0.1:3000/#chat)

***

## 💻 Usage

### 📱 Example Conversations

<details>
<summary><b>🔍 Check Balance (Hindi)</b></summary>
🗣️ You: "मेरे अकाउंट का बैलेंस क्या है?"  
🤖 Bot: "आपके खाते acct_savings_1 में वर्तमान बैलेंस 48500.5 रुपये है।"
</details>

<details>
<summary><b>💸 Money Transfer - Small Amount (No OTP)</b></summary>
🗣️ You: "रिया को तीन सौ रुपये भेजो"  
🤖 Bot: "300 रुपये acct_savings_1 से acct_friend_riya में सफलतापूर्वक भेजे गए।"
"ट्रांजेक्शन आईडी TX00003।"
</details>

<details>
<summary><b>🔐 Money Transfer - Large Amount (OTP Required)</b></summary>
🗣️ You: "छः हज़ार रुपये भेजो"  
🤖 Bot: "सुरक्षा के लिए, हमने आपके पंजीकृत मोबाइल पर 6 अंकों का OTP भेजा है।"
"कृपया OTP बोलें।"
🗣️ You: "एक दो तीन चार पांच छह"
🤖 Bot: "OTP सत्यापित। 6000 रुपये सफलतापूर्वक भेजे गए।"
</details>

### 🎥 Demo GIF/Video Embedding

**Markdown GIF:**  
``

**Embed MP4:**
```html
<video width="600" controls>
  <source src="https://your-server.com/sahayaa-demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
```

**YouTube Embed:**  
```html
<iframe width="560" height="315" src="https://www.youtube.com/embed/YOUR_VIDEO_ID" frameborder="0" allowfullscreen></iframe>
```

***

## 🎥 Demo Video
<div align="center">
🎬 Watch SahaYaa in Action  
[📹 Full Demo (5 min)](https://your-demo-link.com/) | [⚡ Quick Start (1 min)](https://your-quick-demo.com/)
</div>

***

## 🏗️ Architecture

```
USER INTERFACE (Web UI)
         |
    WebM Audio
         ▼
VOICE API (FastAPI)
    | ASR | Hindi→Digits | Audio Processing |
         ▼
RASA NLU + Dialogue
    | Intent | Entity | Dialogue |
         ▼
ACTION SERVER (Banking/OTP/TTS)
         ▼
SECURE BANKING API (Balance, Transfer)
```

***

## 🗺️ Roadmap

✅ Multilingual ASR  
✅ Voice-first web interface  
✅ OTP-based security for high-value transactions  
✅ Real-time TTS responses  
🚧 Session-based OTP flow  
📱 Mobile app (React Native)  
🌙 Offline mode support  
📊 Analytics dashboard  
🔗 Integration with UPI  
🎯 Personalized banking recommendations  
🌍 Support for 22 Indian languages  

***

## 🤝 Contributing

We love contributions! 💙

- 🐛 [Report Bugs](https://github.com/yourusername/sahayaa/issues/new?template=bug_report.md)
- 💡 [Request Features](https://github.com/yourusername/sahayaa/issues/new?template=feature_request.md)
- 🔧 Submit Pull Requests
  - Fork the repository
  - `git checkout -b feature/AmazingFeature`
  - Commit changes
  - Push and Open Pull Request
- 📖 Contribution Guidelines
  - Use PEP 8 for Python code
  - Add tests for new features
  - Update documentation

***

## 📄 License

Distributed under the MIT License.  
See LICENSE for more info.

***

## 🙏 Acknowledgements

🌟 Open Source Projects  
- [AI4Bharat](https://ai4bharat.org/)
- [Rasa](https://rasa.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PyTorch](https://pytorch.org/)
- [Hugging Face](https://huggingface.co/)

👥 Contributors  
<a href="https://github.com/yourusername/sahayaa/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yourusername/sahayaa" />
</a>

📬 Contact & Support  
<div align="center">
Let's Connect! 🤝  
[GitHub](https://github.com/yourusername) | [LinkedIn](https://linkedin.com/in/yourprofile) | [Twitter](https://twitter.com/yourhandle) | [Email](mailto:your.email@example.com)  
[💡 Join our Discord](https://discord.gg/your-invite) | [📧 Email Us](mailto:support@sahayaa.dev) | [📖 Read the Docs](https://docs.sahayaa.dev/)
</div>

***

<sub>Made with ❤️ by [Your Name](https://github.com/yourusername) — Empowering India's digital banking revolution</sub>  
If SahaYaa helped you, please ⭐ this repository!

***

**Customization tips:**  
- Replace `yourusername`/links/ids with your info  
- Adjust badges, demo image/video URLs  
- Visit [Shields.io](https://shields.io/) for more badges!  
- You can add screenshots by placing images in a `screenshots/` folder

***

