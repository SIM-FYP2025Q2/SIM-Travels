# SIM Travels - ADK/A2A/MCP Chatbot Assistant

**Archived Project** <br/>
**This Final Year Project is no longer under active development and has been archived.
Please note that any demo or deployment links included in this repository are no longer available.**

Welcome to the official repository for the SIM Travels Chatbot Assistant! This project is designed to revolutionize the customer support experience by providing a versatile, intelligent, and easy-to-integrate chatbot solution through framework agnostic solutions such as Agent2Agent (A2A) Protocol and Model Context Protocol (MCP). Our demonstration focuses on the travel industry, but the core functionalities are designed to be universally applicable.

![SIM-Travels-Architecture.png](https://i.ibb.co/ZpM3WQCL/SIM-Travels-Architecture.png)
![SIM-Travels-Zendesk.png](https://i.ibb.co/ymjfQ1QP/SIM-Travels-Zendesk.png)

## ⭐ Demos
**💬 Chat with our Chatbot:** [https://sim-travels-deployment.onrender.com](https://sim-travels-deployment.onrender.com)

**💡 Administrative FAQ Panel:** [https://csit321-fyp-25-s2-33-php-admin-panel.onrender.com](https://csit321-fyp-25-s2-33-php-admin-panel.onrender.com)
> (Admin) Email: admin@example.com, Password: admin
> 
> (Support Agent) Email: john.doe@example.com, Password: password123

**📺 Demonstration Video:** [YouTube](https://youtu.be/ShuibtpFsFA?feature=shared&t=586)

#### 💬 Sample Prompts

* What are the available flights from Singapore to New York next week?
* Find me a hotel in London that's within walking distance to the British Museum.
* I want to travel from KLIA to Kingston Hotel Kuala Lumpur
* Tell me about the train service from Don Mueang Airport to Bangkok's Central Station
* What are some good places to visit in Thailand?
* How do I check in for my flight online?
* Can you retrieve my booking? My last name is Novak, Booking ID d2e8502e
* Can you create a support ticket?

---

### API Endpoints/Deployments

**A2A Protocol (Agent Card):**
1. [Flight Offers Agent Card](https://a2a-agents-fyp-25-s2-33.lester-liam.cc/a2a/flight_offers_agent/.well-known/agent-card.json)
2. [Hotel Offers Agent Card](https://a2a-agents-fyp-25-s2-33.lester-liam.cc/a2a/hotel_offers_agent/.well-known/agent-card.json)
3. [Transfer Offers Agent Card](https://a2a-agents-fyp-25-s2-33.lester-liam.cc/a2a/transfer_offers_agent/.well-known/agent-card.json)

**Model Context Protocol (MCP):**
1. [MCP Server](https://mcp-fyp-25-s2-33.lester-liam.cc/mcp)


Refer to `sample_api_calls.ipynb` ([Google Colab](https://colab.research.google.com/github/SIM-FYP2025Q2/SIM-Travels/blob/main/sample_api_calls.ipynb)) for more information on how to call our APIs.

---

## 👥 Members

* **Lester Liam**: Project Lead/Technical Leader
* **Nicolas Ng**: Frontend Developer
* **Nicholas Ting**: Frontend Developer
* **Lucas**: Backend/AI Logic Developer
* **Danish**:  Documentation

## 📄 Project Documentation

Documentations will be published here once completed & public access is allowed.

> 🔗 View our [Taiga Project Board](https://tree.taiga.io/project/lesterl-sim2025q2-fyp-25-s2-33/timeline)

> 📄 Documentations [Google Drive](https://drive.google.com/drive/folders/178JME2NU7hRcL9coJ_2rx1pJpNe-je6I?usp=sharing)

---

## 🚀 Introduction
In a world where 24/7 customer support is no longer a luxury but an expectation, businesses are increasingly turning to chatbots. However, many existing solutions fall short, offering rigid, rule-based interactions that frustrate users and fail to resolve complex issues.

Our project tackles this problem head-on by developing a "Universal Chatbot Assistant" that is:

🧠 **Intelligent**: Powered by Gemini to understand and respond to a wide range of queries with a human like persona.

🔌 **Plug-and-Play**: Designed with a framework-agnostic approach, allowing for seamless integration into existing systems with minimal development time.


## ✨ Key Features

✈️ **Multi-Role Capabilities**: In our travel industry demonstration, the chatbot can act as a:

- **Travel Planner**: Offers personalized trip suggestions and itineraries.
- **Offers Finder**: Searches for the best deals on flights, hotels, and airport transfers.
- **Customer Service Agent**: Handles FAQs, provides detailed policy information, and offers general support.

🎫 **Seamless Zendesk Integration**:

- **Ticket Creation**: Automatically creates support tickets for issues that require human intervention.

- **Live Agent Handover**: Smoothly transfers conversations to a human agent when necessary, providing them with the full context of the interaction.

🌐 **Universal API**: Our "plug-and-play" API is built on the principles of the Agent2Agent (A2A) Protocol and the Model Context Protocol (MCP), making it easy for any business to integrate our chatbot's capabilities into their own systems.

## 🛠️ Frameworks and Technologies
This project is built on a foundation of cutting-edge frameworks and technologies to ensure a robust, scalable, and intelligent solution:

🤖 **Agent Development Kit (ADK)**: An AI agentic framework that allows for the creation of multi-agent architectures with low code. It's model and framework-agnostic, supporting various LLMs.

🔄 **Model Context Protocol (MCP)**: An open standard that standardizes how AI applications interact with external data sources, allowing our chatbot to access real-time information from APIs.

🤝 **Agent-to-Agent (A2A) Protocol**: An open standard that enables secure and seamless communication between different AI agents, allowing for complex, collaborative workflows.

✈️ **Amadeus Travel API**: Our primary data source for real-time flight, hotel, and transfer offer prices.

🔍 **Tavily Search**: An API that grounds our chatbot with web searches, giving it access to the latest information for trip recommendations and transportation services.

🧠 **Pinecone Vector Database**: A vector embedding database that enables powerful semantic searches for our FAQ and knowledge base features.

💬**Zendesk**: A leading Customer Relationship Management (CRM) software that we've integrated for web conversations, support ticketing and live agent handover.

💻 **Frontend**: Built with React, Vite, PHP, and Bootstrap for a modern, responsive, and user-friendly interface.

⚙️ **Backend**: Powered by FastAPI and a MySQL database hosted on Azure.

## 💼 Business Model
The Universal Chatbot Assistant is an open-source project. We believe in the power of community and collaboration to drive innovation.

### 🎯 Target Market:

- **AI Developers**: Individuals and teams building AI agents.
- **Businesses**: Companies looking to deploy their own AI-powered customer service chatbot.
- **API Providers**: Individuals and companies providing data and services that can be used by AI agents.

### 🌟 Value Proposition:

- **Seamless A2A Communication**: A universal language for AI agents to interact.
- **Effortless Live Data Integration**: Simplifies connecting AI agents to real-time data.
- **Open-Source Flexibility**: Transparency, customizability, and a supportive community.

### 💰 Revenue Model
As an open-source project, there is no revenue model. We aim to create a valuable tool for the developer community.

### Prerequisites
- Node.js
- npm
- Python 3.11 or higher
- Docker
- uv 

---

## 📬 Contact

For feedback or contributions, please open an issue or reach out via our [email](mailto:FYP-25-S2-33@mail.com).

---
