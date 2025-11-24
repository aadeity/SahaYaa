<div align="center">

# 🏦 SahaYaa
### AI-Powered Multilingual Voice Banking Assistant

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Rasa](https://img.shields.io/badge/Rasa-3.6-5A17EE?style=for-the-badge&logo=rasa&logoColor=white)](https://rasa.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/sahayaa?style=for-the-badge)](https://github.com/yourusername/sahayaa/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/sahayaa?style=for-the-badge)](https://github.com/yourusername/sahayaa/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)

**[🚀 Live Demo](#-demo-video) • [📖 Documentation](#-getting-started) • [🎯 Features](#-features) • [🤝 Contribute](#-contributing)**

<img src="https://your-demo-gif-url.gif" alt="SahaYaa Demo" width="600px"/>

---

### *Breaking language barriers in digital banking with voice-first AI*

</div>

---

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

---

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

---

## 💡 Why SahaYaa?

### 🎨 What Sets Us Apart

| Feature | Traditional Apps | SahaYaa |
|---------|-----------------|---------|
| **Language Support** | 2-3 languages | **8 languages** (7 Indian + English) |
| **Interaction** | Touch/Type | **Voice-first** |
| **Learning Curve** | Complex UI | **Zero learning curve** |
| **Accessibility** | Limited | **Fully accessible** |
| **Security** | OTP only | **Biometric + OTP** |
| **Offline Support** | Requires internet | **Hybrid mode** (planned) |

### 🔥 Unique Features

1. **🎤 Indic ASR Excellence** - Powered by AI4Bharat's IndicConformer (600M parameters)
2. **🧠 Context-Aware NLU** - Understands code-mixed speech (Hinglish, Tanglish, etc.)
3. **🔐 Smart Security** - Conditional OTP for high-value transactions (>₹5000)
4. **🎭 Natural Conversations** - Handles follow-ups, corrections, and clarifications
5. **📊 Real-time Feedback** - Voice + visual confirmation for critical operations

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🏦 Banking Operations
- ✅ **Balance Inquiry** - Check account balance
- ✅ **Money Transfer** - UPI-style transfers
- ✅ **Bill Payments** - Electricity, mobile, gas
- ✅ **Transaction History** - Last N transactions
- ✅ **Loan Inquiries** - Check eligibility & rates
- ✅ **Credit Limit** - View available credit

</td>
<td width="50%">

### 🔒 Security Features
- 🔐 **Multi-Factor Auth** - Biometric + OTP
- 👤 **Liveness Detection** - Anti-spoofing
- 🚨 **Risk-based OTP** - Smart threshold (₹5000)
- 🔑 **Session Management** - 60-min timeout
- 📝 **Audit Logging** - Complete transaction trail
- 🛡️ **CORS Protection** - Secure API endpoints

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
- 🏷️ **Entity Extraction** (Amounts, accounts)
- 📈 **Context Tracking** (Multi-turn dialogues)
- 🔄 **Fallback Handling** (Graceful degradation)

</td>
</tr>
</table>

---

## 🛠️ Tech Stack

### **Core Technologies**

<div align="center">

| **Category** | **Technology** | **Version** | **Purpose** |
|:------------:|:-------------:|:-----------:|:-----------:|
| **🤖 NLU Engine** | ![Rasa](https://img.shields.io/badge/Rasa-5A17EE?logo=rasa&logoColor=white) | 3.6.13 | Intent classification & dialogue |
| **🎙️ ASR** | ![AI4Bharat](https://img.shields.io/badge/IndicConformer-FF6B35?logo=python&logoColor=white) | 600M | Speech-to-text (8 languages) |
| **🔊 TTS** | ![gTTS](https://img.shields.io/badge/Google_TTS-4285F4?logo=google&logoColor=white) | 2.4.0 | Text-to-speech synthesis |
| **🌐 API Framework** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) | 0.104 | Voice API gateway |
| **🧠 ML Framework** | ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white) | 2.1.0 | ASR model inference |
| **💾 ML Ops** | ![Transformers](https://img.shields.io/badge/🤗_Transformers-FFD21E?logoColor=black) | 4.35.0 | Model loading & inference |
| **🎨 Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white) | - | Web interface |
| **🔧 Audio** | ![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?logo=ffmpeg&logoColor=white) | Latest | Audio processing |

</div>

### **Development Stack**

