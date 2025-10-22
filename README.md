# 🎬 YouTube Summarization Agent

An AI-powered tool that automatically converts long YouTube videos into clear, chaptered summaries using yt-dlp, Whisper, and OpenAI GPT. Get the key insights from any video in minutes!

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com)

## ✨ Features

- **🎥 Smart Video Processing**: Downloads audio and metadata using yt-dlp
- **🎤 Multiple Transcription Options**: 
  - Auto-subtitles (fastest)
  - OpenAI Whisper API (cloud)
  - Local Whisper (offline)
- **🧠 AI-Powered Summarization**: GPT-4/4o-mini generates intelligent chapter summaries
- **📊 Intelligent Chunking**: Splits content by silence gaps and duration limits
- **📱 Dual Interface**: CLI and Streamlit web UI
- **📄 Multiple Output Formats**: JSON and Markdown
- **🔄 Retry Logic**: Robust error handling with automatic retries
- **🌍 Multi-language Support**: Works with videos in any language

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API key
- ffmpeg (for audio processing)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/meettomar07/Youtube-summarizer-.git
   cd Youtube-summarizer-
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   ```bash
   # Option 1: Environment variable
   export OPENAI_API_KEY="your-api-key-here"
   
   # Option 2: Create .env file
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

4. **Install ffmpeg** (if not already installed)
   ```bash
   # Windows (with Chocolatey)
   choco install ffmpeg
   
   # macOS (with Homebrew)
   brew install ffmpeg
   
   # Ubuntu/Debian
   sudo apt update && sudo apt install ffmpeg
   ```

## 🎯 Usage

### Web Interface (Recommended)

Launch the Streamlit app for an easy-to-use interface:

```bash
streamlit run youtube_summarizer/ui.py
```

Then open http://localhost:8501 in your browser and:
1. Enter your OpenAI API key (if not set in environment)
2. Paste a YouTube URL
3. Click "Summarize"
4. Download results as JSON or Markdown

### Command Line Interface

```bash
# Basic usage
python -m youtube_summarizer.main "https://www.youtube.com/watch?v=VIDEO_ID"

# With custom output files
python -m youtube_summarizer.main "https://www.youtube.com/watch?v=VIDEO_ID" \
  --json output.json \
  --md output.md \
  --lang en
```

### CLI Options

- `--json`: Specify JSON output file path
- `--md`: Specify Markdown output file path  
- `--lang`: Language code (e.g., en, es, fr)

## 📁 Project Structure

```
youtube_summarizer/
├── __init__.py          # Package initialization
├── config.py            # Configuration and settings
├── downloader.py        # yt-dlp video/audio downloader
├── transcriber.py       # Whisper transcription (local/API)
├── chunker.py           # Intelligent content chunking
├── summarizer.py        # GPT-powered summarization
├── main.py              # CLI entry point
├── ui.py                # Streamlit web interface
└── README.md            # This file
```

## ⚙️ Configuration

Create a `.env` file or set environment variables:

```env
# Required
OPENAI_API_KEY=your-api-key-here

# Optional
OPENAI_MODEL=gpt-4o-mini
TRANSCRIPTION_BACKEND=auto  # auto | openai | whisper_local
TRANSCRIPTION_MODEL=whisper-1
MAX_CHUNK_TOKENS=1800
CHUNK_MAX_SECONDS=480
CHUNK_GAP_SECONDS=2.0
OUTPUT_DIR=outputs
```

## 📊 Output Format

### JSON Output
```json
{
  "video_title": "The Future of AI",
  "chapters": [
    {
      "start": "0:00",
      "end": "2:14", 
      "title": "Introduction to AI Evolution",
      "summary": "The speaker introduces how AI has evolved over time...",
      "key_points": [
        "AI development timeline",
        "Key breakthrough moments",
        "Current state of technology"
      ]
    }
  ]
}
```

### Markdown Output
```markdown
# The Future of AI

## Video Summary
This video covers multiple topics and key insights.

## Chapters

### 1. Introduction to AI Evolution [0:00]
The speaker introduces how AI has evolved over time...

**Key Points:**
- AI development timeline
- Key breakthrough moments  
- Current state of technology
```

## 🔧 Advanced Usage

### Custom Transcription Backend

```python
# Force OpenAI Whisper API
export TRANSCRIPTION_BACKEND=openai

# Use local Whisper (slower but offline)
export TRANSCRIPTION_BACKEND=whisper_local
```

### Batch Processing

```bash
# Process multiple videos
for url in "https://youtube.com/watch?v=VIDEO1" "https://youtube.com/watch?v=VIDEO2"; do
  python -m youtube_summarizer.main "$url"
done
```

## 🛠️ Troubleshooting

### Common Issues

**"yt-dlp failed to download audio"**
- Update yt-dlp: `pip install --upgrade yt-dlp`
- Try a different video (some may be region-locked)
- Check your internet connection

**"OpenAI API key not found"**
- Set environment variable: `export OPENAI_API_KEY="your-key"`
- Or create `.env` file with your key

**"ffmpeg not found"**
- Install ffmpeg and ensure it's in your PATH
- See installation instructions above

**"Module not found"**
- Ensure you're in the project directory
- Install dependencies: `pip install -r requirements.txt`

### Performance Tips

- **Faster transcription**: Use auto-subtitles when available
- **Lower costs**: Use `gpt-4o-mini` instead of `gpt-4`
- **Offline mode**: Use local Whisper for privacy
- **Batch processing**: Process multiple videos in sequence

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video downloading
- [OpenAI Whisper](https://github.com/openai/whisper) for transcription
- [OpenAI GPT](https://openai.com) for summarization
- [Streamlit](https://streamlit.io) for the web interface

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#-troubleshooting)
2. Search existing [GitHub Issues](https://github.com/meettomar07/Youtube-summarizer-/issues)
3. Create a new issue with detailed information

---

**Made with ❤️ by [Meet Tomar](https://github.com/meettomar07)**
