# Long Memory-Based Agentic AI

A conversational AI agent that maintains extensive conversation history using persistent long-term memory, enabling deep context-aware and highly personalized interactions across sessions.

## Features

- 🧠 **Long-Term Memory**: Stores and utilizes up to 50 messages from conversation history
- 💬 **Deep Context Awareness**: Uses extensive conversation history to provide highly personalized responses
- 🔄 **Session Continuity**: Remembers past conversations even after restarting the application
- ⚙️ **Smart Memory Management**: Intelligently balances recent context with long-term memory
- 🌐 **OpenRouter Integration**: Uses OpenRouter API to access various AI models
- 🔒 **Secure Configuration**: API keys stored in environment variables

## Key Differences from Single Memory Version

- **Memory Capacity**: Uses up to 50 messages (vs 6 in single memory version)
- **Memory Strategy**: Prioritizes recent messages while sampling from older conversations
- **Context Awareness**: Maintains awareness of much longer conversation history
- **Better Continuity**: Can recall and reference information from many turns ago

## Prerequisites

- Python 3.7 or higher
- OpenRouter API key ([Get one here](https://openrouter.ai/))

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd Long-memory-based-agentic-ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in the project root:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

## Configuration

The project uses the following configuration (defined in `config.py`):

- **Model**: `xiaomi/mimo-v2-flash:free` (free tier model via OpenRouter)
- **API URL**: `https://openrouter.ai/api/v1/chat/completions`
- **Max Context Messages**: 50 messages (configurable via `MAX_CONTEXT_MESSAGES` in `agent.py`)
- **Min Recent Messages**: 10 messages always included (configurable via `MIN_RECENT_MESSAGES` in `agent.py`)

To change the model, edit `MODEL_NAME` in `config.py`.

## Usage

Run the agent:
```bash
python agent.py
```

Once started, you can:
- Type messages to interact with the AI
- Type `exit` to stop the conversation and save memory

Example conversation:
```
🧠 Long Memory-Based Agentic AI started
📚 Loaded 25 messages from memory
Type 'exit' to stop

You: What did we talk about last week?
Agent: Last week we discussed your favorite programming languages, 
       specifically how you prefer Python for data science and JavaScript 
       for web development. We also talked about your upcoming project 
       involving machine learning.

You: Remind me about that project
Agent: You mentioned you're working on a machine learning project to 
       predict customer churn using historical data. You were planning 
       to use Python with scikit-learn and were looking for advice on 
       feature engineering.
```

## Project Structure

```
Long-memory-based-agentic-ai/
├── agent.py          # Main agent logic with long-term memory management
├── config.py         # Configuration and environment variables
├── memory.json       # Persistent conversation memory (auto-generated)
├── requirements.txt  # Python dependencies
├── .env             # Environment variables (create this)
└── README.md        # This file
```

## How It Works

1. **Memory Loading**: On startup, the agent loads all previous conversations from `memory.json`
2. **Smart Context Building**: 
   - Always includes the last 10 messages (recent context)
   - Samples from older messages to fill up to 50 total messages
   - Ensures continuity while managing token usage
3. **API Interaction**: Messages are sent to OpenRouter API with proper headers
4. **Memory Persistence**: Each conversation turn is saved to `memory.json`
5. **Response Generation**: The AI generates responses based on extensive context

## Memory Management Strategy

- **Recent Priority**: Last 10 messages are always included for immediate context
- **Long-Term Sampling**: Older messages are sampled evenly to fill remaining slots
- **Total Capacity**: Up to 50 messages sent to API per request
- **Full History**: All conversation history is preserved in `memory.json`
- **Adaptive**: Automatically adjusts based on total memory size

## Customization

### Change Memory Capacity

Edit `MAX_CONTEXT_MESSAGES` in `agent.py`:
```python
MAX_CONTEXT_MESSAGES = 100  # Use up to 100 messages
```

### Adjust Recent Message Window

Edit `MIN_RECENT_MESSAGES` in `agent.py`:
```python
MIN_RECENT_MESSAGES = 20  # Always include last 20 messages
```

### Change AI Model

Edit `MODEL_NAME` in `config.py`:
```python
MODEL_NAME = "openai/gpt-4"  # Use GPT-4 instead
```

### Customize System Prompt

Edit the system message in the `build_messages()` function in `agent.py`:
```python
"content": (
    "You are a helpful assistant specialized in..."
)
```

## Troubleshooting

**Issue**: `OPENROUTER_API_KEY not set`
- **Solution**: Ensure you've created a `.env` file with your API key

**Issue**: API request fails
- **Solution**: Verify your API key is valid and you have sufficient credits on OpenRouter

**Issue**: Memory file not found
- **Solution**: This is normal on first run. The file will be created automatically.

**Issue**: Token limit exceeded
- **Solution**: Reduce `MAX_CONTEXT_MESSAGES` if your model has token limits

## Dependencies

- `requests` - HTTP library for API calls
- `python-dotenv` - Load environment variables from `.env` file

## License

This project is open source and available for personal and educational use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

