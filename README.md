# MP4 to MP3 Tool

A simple yet powerful web-based tool to convert MP4 video files to MP3 audio format. This project provides a clean user interface built with Gradio and uses FFmpeg for efficient media conversion.

![GitHub license](https://img.shields.io/github/license/sawyer-shi/mp4-to-mp3-tool)

## Features

- Easy-to-use web interface
- Fast conversion from MP4 to MP3
- Error handling and validation
- Informative logging
- Cross-platform compatibility
- Automatic FFmpeg installation on Windows

## Screenshots

(Add screenshots of your application here)

## Installation

Choose one of the following installation methods:

### 1. Source Code Installation

```bash
# Clone the repository
git clone https://github.com/sawyer-shi/mp4-to-mp3-tool.git
cd mp4-to-mp3-tool

# Install dependencies
pip install -r requirements.txt

# Run the application
python run_gradio.py
```

### 2. Virtual Environment Installation

```bash
# Clone the repository
git clone https://github.com/sawyer-shi/mp4-to-mp3-tool.git
cd mp4-to-mp3-tool

# Create and activate virtual environment
python -m venv env

# On Windows
env\Scripts\activate

# On macOS/Linux
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run_gradio.py
```

### 3. Conda Environment Installation

```bash
# Clone the repository
git clone https://github.com/sawyer-shi/mp4-to-mp3-tool.git
cd mp4-to-mp3-tool

# Create and activate conda environment
conda create -n mp4_to_mp3 python=3.9
conda activate mp4_to_mp3

# Install dependencies
pip install -r requirements.txt

# Run the application
python run_gradio.py
```

Once the application is running, open your browser and navigate to:
```
http://localhost:7860
```

## Usage

1. Open the web interface in your browser
2. Click the upload button to select an MP4 file
3. Wait for the conversion to complete
4. Download the converted MP3 file

## Prerequisites

- Python 3.8 or higher
- FFmpeg (automatically installed on Windows, manual installation required on other platforms)

### FFmpeg Installation (if automatic installation fails)

- **Windows**: Download from [FFmpeg.org](https://ffmpeg.org/download.html#build-windows) and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo dnf install ffmpeg` (Fedora)

