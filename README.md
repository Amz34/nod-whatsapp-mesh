# nod-whatsapp-mesh 🤖📱

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Baileys%20Socket-25D366.svg?logo=whatsapp&logoColor=white)](https://github.com/whiskeysockets/baileys)
[![n8n Nod](https://img.shields.io/badge/n8n-Nod%20Labs-EA4B71.svg?logo=n8n&logoColor=white)](https://github.com/n8n-io/nod)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](https://docker.com)

**Enterprise WhatsApp Baileys Transport & Native Poll Approval Mesh for n8n Nod (AI Chief of Staff).**

Transform [n8n Nod](https://github.com/n8n-io/nod) into a 24/7 mobile executive assistant on WhatsApp with **deterministic "No Nod, No Action" native interactive poll button approvals**, automated SaaS subscription leak audits, and zero-API Computer Use browser automation.

---

## 🌟 Why nod-whatsapp-mesh?

While n8n Nod ships out-of-the-box with Telegram and Desktop Electron channels, **WhatsApp** is the primary operational communication medium for global founders, executives, and enterprise teams across EMEA, LATAM, and APAC.

`nod-whatsapp-mesh` provides the bridge:

- 📱 **1-Tap Thumb Approvals (Native WhatsApp Polls)**: When the agent plans an irreversible action (sending emails, canceling subscriptions, executing payments), it halts and dispatches a native clickable WhatsApp poll button to your chat.
- 💸 **Autonomous SaaS & Financial Leak Auditor**: Scans Gmail receipts via IMAP, detects silent price hikes, double billings, and abandoned subscriptions, compiling an executive ledger.
- 🖥️ **Zero-API Visual Computer Use**: Seamlessly integrates with [browser-use](https://github.com/browser-use/browser-use) to navigate gated vendor portals and tender dashboards that have no public APIs.
- 🧠 **BYO LLM Inference Router**: Routes model inference across Google Gemini 2.5 Flash, Anthropic Claude 3.5 Sonnet, OpenAI, DeepSeek V3, or local Ollama instances.
- 🗄️ **Centralized PostgreSQL 16 State**: Fully auditable SQL event log with zero state loss.

---

## 🏗️ Architecture

```
📱 You on WhatsApp (+966 / Global Phone)
   │
   │  (Native Clickable Poll Buttons & Text Commands)
   ▼
⚡ Baileys WhatsApp Bridge (:3003)
   │
   ▼
🤖 Nod Autonomous Engine (Host Daemon / Docker)
   ├── 🧠 LLM Gateway (:8000) [Gemini 2.5 Flash / Claude 3.5 Sonnet]
   ├── 🖥️ Headless Chromium [browser-use Computer Use]
   ├── ⚙️ Workflow Mesh [n8n Automation Engine :5678]
   └── 🗄️ PostgreSQL 16 Storage [agent_memory.nod_ledger :5435]
```

---

## 🚀 Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/Amz34/nod-whatsapp-mesh.git
cd nod-whatsapp-mesh
```

### 2. Configure Environment (`.env`)
```bash
cp .env.example .env
```
Populate your credentials:
```env
WHATSAPP_PHONE=966574268856
GEMINI_API_KEY=your_gemini_api_key_here
GMAIL_APP_PASSWORD=your_gmail_app_password_here
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5435
POSTGRES_DB=agent_memory
POSTGRES_USER=agent_admin
POSTGRES_PASSWORD=central_secret
```

### 3. Start WhatsApp Bridge
```bash
npm install
npm run bridge
# Scan the QR code in your terminal with WhatsApp (Linked Devices)
```

### 4. Run Nod Agent Daemon
```bash
pip install -r requirements.txt
python3 src/nod_engine.py --daemon
```

---

## 💬 Interactive Commands

Text your WhatsApp agent number at any time:

| Command | Action |
| :--- | :--- |
| `audit` | Runs real-time SaaS & invoice audit across connected mailboxes and cloud accounts. |
| `leads` | Triages recent candidate profiles or enterprise RFP briefs with staged proposals. |
| `monitor` | Executes a headless browser check on target URLs to detect layout or pricing changes. |
| `help` | Lists available operational commands and status. |

---

## 🛡️ "No Nod, No Action" Trust Tripwire

The safety engine enforces a physical approval gate before execution:

1. Agent detects an actionable task (e.g. *Found 3 unused SaaS subscriptions costing $180/mo*).
2. Agent **pauses execution** and sends a **Native Clickable Poll Button Card** directly to your WhatsApp.
3. You tap **"✅ Cancel Unused"** on your phone.
4. Bridge intercepts the poll vote event, verifies author JID, and logs the authorization receipt to PostgreSQL before performing the action.

---

## 📄 License

Licensed under the **Apache License 2.0**. See [LICENSE](LICENSE) for details.

Developed with ❤️ by **[Engr. Aamir Zameer](https://github.com/Amz34)**.
