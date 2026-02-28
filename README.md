# 🤖 24/7 Telegram Assistant & Lead Generator

## 📌 What is this?
Meet your new digital receptionist. This Telegram bot works 24/7 to collect client requests, answer initial inquiries, and gather contact details when human managers are sleeping, busy, or away. 

It ensures that **zero leads are lost**, turning missed chats into structured, actionable business contacts.

---

## 💼 Why does your business need it?
In today's fast world, if you don't answer a client in 5 minutes, they go to your competitor. 
This bot solves that problem:
1. **Always Online:** Greets your customers instantly, day or night.
2. **Never Misses a Lead:** Politely asks for the client's name, phone number, and their question.
3. **High Conversion Rate:** It features a smart **"⏭ Skip"** button for optional questions (like Email or Telegram username), so clients don't get annoyed and drop off.

---

## 📊 The Magic: Google Sheets as a Free CRM
You don't need to scroll through Telegram history to find who asked for what. 

**Every time a client finishes the chat, the bot instantly saves the data into a live Google Spreadsheet.** It neatly organizes:
* 📅 Date & Time of the request
* 👤 Client's Name
* 📞 Phone Number
* 📧 Email & Telegram (if provided)
* 📝 The actual message or request

*Result: Your sales team wakes up, opens one clean Google Sheet, and sees exactly who to call today.*

---

## 🎯 Perfect for:
* **🏨 Hotels & Real Estate:** "Please call me back for a booking" or "Late check-in requests".
* **🏥 Clinics & Beauty Salons:** Appointment scheduling and initial consultations.
* **🛠 Service Providers:** Plumbers, mechanics, and electricians gathering service requests.
* **🎓 Online Coaches & Mentors:** Collecting leads for courses or private sessions.

---

## 📱 How it looks to your client (User Flow)
The process takes less than 30 seconds:
1. Client presses `/start` or clicks **"Leave a message"**.
2. Bot asks for their **Name** and **Phone Number** (mandatory).
3. Bot asks for Email / Telegram username (Client can easily tap **Skip**).
4. Client types their question or message.
5. Done! The client is assured they will be contacted soon, and the business owner gets an instant Telegram notification.

---

## 🛠 For Developers (Tech Stack & Setup)
*While the bot is simple for users, it runs on a robust, modern architecture.*
* **Language:** Python 3.10+
* **Framework:** `aiogram 3.x` (Asynchronous & fast)
* **Databases:** `SQLite` (Local backup) + `Google Sheets API` (Live cloud CRM)
* **State Management:** FSM (Finite State Machine) for smooth, step-by-step conversations.

---
*Built to help businesses save time and make more money. 🚀*