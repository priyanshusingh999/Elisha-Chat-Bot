# Elisha Chat Bot

Elisha Chat Bot is an intelligent and interactive Telegram chatbot powered by Google Generative AI (Gemini). It responds to user messages with a friendly, mature, and sometimes playful tone, simulating a human-like conversation. The bot supports basic commands and can broadcast messages to users. It stores user data in MongoDB and is designed to run continuously, either directly or via Docker.

## Features

- Responds to Telegram messages using Google Gemini AI.
- Supports commands:
  - `/start` - Welcome message.
  - `/help` - List available commands.
  - `/broadcast` - Broadcast a message to all users (owner only).
  - `/users` - Show total number of users (owner only).
- Stores user information in MongoDB.
- Easy to deploy with Docker or run directly.
- Keeps the bot alive for continuous operation.

## Requirements

- Python 3.11+
- MongoDB instance (connection URI required)
- Telegram Bot Token
- Google Gemini API Key

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Elisha-Chat-Bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables:
   - `BOT_TOKEN` - Your Telegram bot token.
   - `OWNER_ID` - Telegram user ID of the bot owner.
   - `GEMINI_API_KEY` - API key for Google Generative AI.
   - `MONGODB_URI` - MongoDB connection string.

   You can set these in your environment or store them in the MongoDB `variables` collection.

## Usage

### Running directly

Start the bot by running:

```bash
python main.py
```

Or use the provided shell script:

```bash
./start.sh
```

### Running with Docker

Build the Docker image:

```bash
docker build -t elisha-chat-bot .
```

Run the container (exposing port 8002 for keep-alive server):

```bash
docker run -d -p 8002:8002 --env BOT_TOKEN=your_bot_token --env OWNER_ID=your_owner_id --env GEMINI_API_KEY=your_gemini_api_key --env MONGODB_URI=your_mongodb_uri elisha-chat-bot
```

## Commands

- `/start` - Receive a welcome message.
- `/help` - Get a list of available commands.
- `/broadcast <message>` - Broadcast a message to all users (owner only).
- `/users` - Get the total number of users (owner only).

## License

This project is open source and free to use.
