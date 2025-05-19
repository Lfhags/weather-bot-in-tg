# weather-bot-in-tg
🌦️ Telegram Weather Bot — A Python-based Telegram bot utilizing aiogram 3 and OpenWeatherMap API to deliver real-time weather forecasts for Ukrainian regions.
# 🌦️ Telegram Weather Bot

A Python-based Telegram bot utilizing aiogram 3 and the OpenWeatherMap API to deliver real-time weather forecasts for Ukrainian regions.

---

## 📋 Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## ✅ Features

- Provides daily weather forecasts for Ukrainian regions.
- Utilizes aiogram 3 for asynchronous Telegram bot development.
- Integrates with OpenWeatherMap API for accurate weather data.
- Supports both reply and inline keyboards for user interaction.
- Designed for deployment on IPv6-only VPS environments.

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package installer)
- A Telegram account and bot token from [@BotFather](https://t.me/BotFather)
- An API key from [OpenWeatherMap](https://openweathermap.org/api)

### Installation

1. **Clone the repository:**

   git clone https://github.com/Lfhags/weather-bot-in-tg.git
   cd telegram-weather-bot
   
2. **Create a virtual environment (optional but recommended):**

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install the required packages:**

pip install -r requirements.txt


**Configuration**


1. **Create a .env file in the project root directory:**

touch .env

2. Add the following environment variables to the .env file:

BOT_TOKEN=your_telegram_bot_token
OPENWEATHER_API_KEY=your_openweathermap_api_key


📌 Usage

1. **Run the bot:**

python bot.py

2. Interact with the bot on Telegram:

Start the bot by sending /start.

Select your region using the provided keyboard.

Receive the current weather forecast for the selected region.


🛠️ Deployment
**o deploy the bot on a server:**

1. Ensure your server supports IPv6 connectivity.

2. Install necessary dependencies on the server:

sudo apt update
sudo apt install python3 python3-pip -y
pip3 install -r requirements.txt

3. Set up environment variables on the server:

Create a .env file with your BOT_TOKEN and OPENWEATHER_API_KEY.

4. Run the bot using a process manager (e.g., screen, tmux, or systemd) to ensure it stays active:
   
   screen -S weatherbot
python bot.py
# To detach: Press Ctrl+A, then D
# To resume: screen -r weatherbot

🤝 Contributing
Contributions are welcome! To contribute:

Fork the repository.

Create a new branch: git checkout -b feature/your-feature-name.

Make your changes and commit them: git commit -m 'Add your message here'.

Push to the branch: git push origin feature/your-feature-name.

Open a pull request detailing your changes.

📄 License
This project is licensed under the MIT License.

🙏 Acknowledgements
aiogram for the asynchronous Telegram bot framework.

OpenWeatherMap for providing comprehensive weather data.

Python Telegram Bot List for inspiration and resources.
