import utils.session
import json
import requests
from config import OPENROUTER_API_KEY, MODEL_NAME, API_URL

MEMORY_FILE = "memory.json"
MAX_CONTEXT_MESSAGES = 50  # Long-term memory: use up to 50 messages
MIN_RECENT_MESSAGES = 10   # Always include at least 10 recent messages


def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def build_messages(memory, user_input):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a long memory-based agentic AI. "
                "You have access to extensive conversation history and can recall "
                "details from past conversations to provide highly personalized and "
                "context-aware responses. Use the full conversation history to maintain "
                "continuity and build upon previous interactions."
            )
        }
    ]

    # Long-term memory strategy:
    # 1. Always include recent messages (last MIN_RECENT_MESSAGES)
    # 2. If memory is larger, include older messages up to MAX_CONTEXT_MESSAGES
    # 3. Prioritize recent context while maintaining long-term awareness
    
    total_memory = len(memory)
    
    if total_memory <= MAX_CONTEXT_MESSAGES:
        # If memory fits, use all of it
        messages.extend(memory)
    else:
        # Use recent messages + sample from older messages
        recent_messages = memory[-MIN_RECENT_MESSAGES:]
        older_messages = memory[:total_memory - MIN_RECENT_MESSAGES]
        
        # Include older messages if we have space
        remaining_slots = MAX_CONTEXT_MESSAGES - MIN_RECENT_MESSAGES
        if remaining_slots > 0 and len(older_messages) > 0:
            # Sample evenly from older messages
            step = max(1, len(older_messages) // remaining_slots)
            sampled_older = older_messages[::step][:remaining_slots]
            messages.extend(sampled_older)
        
        messages.extend(recent_messages)

    # Add current user input
    messages.append({"role": "user", "content": user_input})

    return messages


def call_openrouter(messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Long Memory-Based Agentic AI"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": messages
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


def chat():
    if not OPENROUTER_API_KEY:
        print("❌ OPENROUTER_API_KEY not set")
        return

    memory = load_memory()
    memory_size = len(memory)
    print("🧠 Long Memory-Based Agentic AI started")
    print(f"📚 Loaded {memory_size} messages from memory")
    print("Type 'exit' to stop\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("👋 Goodbye")
            break

        messages = build_messages(memory, user_input)
        context_size = len(messages) - 1  # Exclude system message
        print(f"📝 Using {context_size} messages as context...")
        
        reply = call_openrouter(messages)

        print("Agent:", reply, "\n")

        # Save conversation to memory
        memory.append({"role": "user", "content": user_input})
        memory.append({"role": "assistant", "content": reply})

        save_memory(memory)


if __name__ == "__main__":
    chat()

