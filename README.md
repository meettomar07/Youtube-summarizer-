# YouTube Summarizer

A powerful tool that automatically downloads, transcribes, and summarizes YouTube videos using Hugging Face models.

## Features

- 🎬 **YouTube Video Processing**: Download and process any YouTube video
- 🎤 **Multiple Transcription Options**: Support for Hugging Face Whisper, OpenAI Whisper, or local Whisper
- 📝 **AI-Powered Summarization**: Uses Hugging Face BART model for intelligent summarization
- 📊 **Structured Output**: Generates both JSON and Markdown summaries
- 🌐 **Web Interface**: User-friendly Streamlit web interface
- ⚡ **Configurable**: Customizable chunk sizes and processing parameters

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Hugging Face API Key

Create a `.env` file in the project root:

```bash
HUGGINGFACE_API_KEY=your_hugging_face_api_key_here
HUGGINGFACE_MODEL=facebook/bart-large-cnn
TRANSCRIPTION_BACKEND=huggingface
TRANSCRIPTION_MODEL=openai/whisper-large
MAX_CHUNK_TOKENS=800
CHUNK_MAX_SECONDS=480
CHUNK_GAP_SECONDS=2.0
OUTPUT_DIR=outputs
```

Or set the environment variable directly:

```bash
export HUGGINGFACE_API_KEY=your_hugging_face_api_key_here
```

### 3. Get Your Hugging Face API Key

1. Go to [Hugging Face](https://huggingface.co/)
2. Create an account or log in
3. Go to Settings → Access Tokens
4. Create a new token with read permissions
5. Copy the token and add it to your `.env` file

## Usage

### Web Interface (Recommended)

```bash
streamlit run ui.py
```

Then open your browser to `http://localhost:8501` and:
1. Enter a YouTube URL
2. Optionally specify a language code
3. Click "Summarize"
4. Download the results as JSON or Markdown

### Command Line Interface

```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --lang en
```

## Configuration

The application can be configured through environment variables:

- `HUGGINGFACE_API_KEY`: Your Hugging Face API key (required)
- `HUGGINGFACE_MODEL`: Summarization model (default: facebook/bart-large-cnn)
- `TRANSCRIPTION_BACKEND`: Transcription method (huggingface, whisper_local, auto)
- `TRANSCRIPTION_MODEL`: Transcription model (default: openai/whisper-large)
- `MAX_CHUNK_TOKENS`: Maximum tokens per chunk (default: 800)
- `CHUNK_MAX_SECONDS`: Maximum seconds per chunk (default: 480)
- `CHUNK_GAP_SECONDS`: Gap between chunks (default: 2.0)
- `OUTPUT_DIR`: Output directory (default: outputs)

## Output

The tool generates:

1. **JSON Summary**: Structured data with chapters, timestamps, and summaries
2. **Markdown Summary**: Human-readable format with overview and chapters

## Requirements

- Python 3.8+
- Hugging Face API key
- Internet connection for downloading videos and accessing models

## Troubleshooting

### Common Issues

1. **Missing API Key**: Make sure `HUGGINGFACE_API_KEY` is set in your environment
2. **Model Loading Errors**: Ensure you have sufficient disk space and memory
3. **Video Download Issues**: Check your internet connection and video URL validity

### Performance Tips

- Use smaller `MAX_CHUNK_TOKENS` for faster processing
- Increase `CHUNK_GAP_SECONDS` for better chunk boundaries
- Use local Whisper for offline transcription

## License

This project is open source and available under the MIT License.