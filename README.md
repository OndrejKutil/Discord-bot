# Discord Bot – Modular Bot with Python & Nextcord

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Medochikita/Discord-bot?include_prereleases&style=for-the-badge) 
[![GitHub License](https://img.shields.io/github/license/Medochikita/Discord-bot?style=for-the-badge)](https://github.com/Medochikita/Discord-bot/blob/main/LICENSE.md) 
![GitHub Release Date](https://img.shields.io/github/release-date/Medochikita/Discord-bot?style=for-the-badge) 
![GitHub Last Commit](https://img.shields.io/github/last-commit/Medochikita/Discord-bot?style=for-the-badge)

![Nextcord](https://badgen.net/badge/icon/Nextcord?icon=https://nextcord.dev/icon.svg&label&scale=1.5&style=for-the-badge)
---

**Currently not maintained**

---

## Project Description

This project is a customizable Discord bot built using **Python** and the **Nextcord** framework. It features modular command architecture, dynamic prefix handling, and clean integration with Discord's modern slash commands.

---

## Goals of the Project

- Learn how to structure scalable and maintainable Python projects
- Gain experience with real-time APIs and event-driven programming
- Practice user input handling, error management, and bot security

---

## What I’ve Learned

This project helped me understand and apply the following concepts:

- **Asynchronous Programming:**  
  Learned to use Python’s `asyncio` features to handle concurrent bot events and commands.

- **Object-Oriented Design:**  
  Applied OOP principles to structure commands as classes and promote code reuse.

- **API Integration & Event Handling:**  
  Worked with Discord’s API events like `on_ready`, `on_message`, and custom user commands.

- **Version Control & Open Source Workflow:**  
  Practiced Git branching, commits, and working with open-source project structure.

---

## Project Structure

```bash
📦Bot code
 ┣ 📂modules/
 ┃ ┣ errorHandler.py  # Error handling
 ┃ ┣ music.py         # Music module
 ┃ ┣ color.py         # some API integration
 ┃ ┣ ... 
 ┣ main.py            # Entry point for the bot
 ┣ requirements.txt   # Python dependencies
 ┣ nextcord.log       # logging
 ┣ pid / prefix.json  # json files as small databases
 ┗ .env               # Environment variables (excluded from Git)
