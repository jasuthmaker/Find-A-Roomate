# Hugging Face API Setup Guide

## Getting Your API Token

1. Go to [Hugging Face](https://huggingface.co/)
2. Create an account or log in
3. Go to your profile settings
4. Navigate to "Access Tokens" section
5. Create a new token with "Read" permissions
6. Copy the token (starts with `hf_`)

## Setting Up the Environment Variable

### Option 1: Environment Variable (Recommended)
Set the environment variable before running the app:

**Windows (Command Prompt):**
```cmd
set HUGGINGFACE_API_TOKEN=your_token_here
python main.py
```

**Windows (PowerShell):**
```powershell
$env:HUGGINGFACE_API_TOKEN="your_token_here"
python main.py
```

**Linux/Mac:**
```bash
export HUGGINGFACE_API_TOKEN="your_token_here"
python main.py
```

### Option 2: Direct Code Modification
If you prefer not to use environment variables, you can directly modify the token in `main.py`:

```python
HF_API_TOKEN = 'your_actual_token_here'  # Replace with your token
```

## Testing the Integration

1. Start the Flask application
2. Navigate to the Chat Assistant page
3. Send a message about housing/roommate issues
4. The AI should respond with contextual advice

## Fallback System

If the Hugging Face API is unavailable or fails, the system will automatically fall back to predefined responses to ensure the chatbot continues working.

## Troubleshooting

- **401 Unauthorized**: Check that your API token is correct
- **429 Too Many Requests**: You've hit the rate limit, wait a moment and try again
- **Timeout errors**: The API might be slow, the system will use fallback responses
- **No response**: Check your internet connection and API token

## API Model Used

The system uses `microsoft/DialoGPT-medium` which is optimized for conversational AI and works well for housing-related questions.
