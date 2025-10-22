# Hugging Face API Configuration

## Setup Instructions

1. **Get your Hugging Face API key**:
   - Go to https://huggingface.co/settings/tokens
   - Create a new token with read access

2. **Set up your API key**:
   ```bash
   # Option 1: Environment variable
   export HUGGINGFACE_API_KEY="your-api-key-here"
   
   # Option 2: Create .env file
   echo "HUGGINGFACE_API_KEY=your-api-key-here" > .env
   
   # Option 3: Streamlit secrets (for web interface)
   mkdir -p .streamlit
   echo "HUGGINGFACE_API_KEY = \"your-api-key-here\"" > .streamlit/secrets.toml
   ```

3. **Run the application**:
   ```bash
   # Web interface
   streamlit run ui.py
   
   # Command line
   python -m main "https://www.youtube.com/watch?v=VIDEO_ID"
   ```

## Configuration Options

You can customize the models and settings by setting environment variables:

```bash
# Model selection
export HUGGINGFACE_MODEL="facebook/bart-large-cnn"  # Summarization model
export TRANSCRIPTION_MODEL="openai/whisper-base"    # Transcription model

# Processing settings
export MAX_CHUNK_TOKENS="1800"
export CHUNK_MAX_SECONDS="480"
export CHUNK_GAP_SECONDS="2.0"
export OUTPUT_DIR="outputs"
```

## Available Models

### Summarization Models:
- `facebook/bart-large-cnn` (default, recommended)
- `google/pegasus-cnn_dailymail`
- `facebook/bart-large-cnn`

### Transcription Models:
- `openai/whisper-base` (default, fast)
- `openai/whisper-small`
- `openai/whisper-medium`
- `openai/whisper-large-v2`
