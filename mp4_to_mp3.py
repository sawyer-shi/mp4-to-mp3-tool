#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MP4 to MP3 Tool
A simple tool to convert MP4 videos to MP3 audio files with a clean user interface.
"""

import os
import subprocess
import sys
import tempfile
import shutil
import gradio as gr
import logging
import time
import json
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_ffmpeg():
    """
    Check if FFmpeg is installed, and install it if not (on Windows).
    """
    try:
        # Try to run ffmpeg to check if it's installed
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE, 
                      check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.warning("FFmpeg not found in PATH")
        
        if sys.platform == 'win32':
            logger.info("Attempting to download FFmpeg...")
            try:
                # Create temp directory
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Download FFmpeg binary for Windows
                    subprocess.run([
                        'powershell', 
                        '-Command', 
                        f"Invoke-WebRequest -Uri 'https://github.com/GyanD/codexffmpeg/releases/download/5.1.2/ffmpeg-5.1.2-essentials_build.zip' -OutFile '{temp_dir}\\ffmpeg.zip'"
                    ], check=True)
                    
                    # Extract the zip file
                    subprocess.run([
                        'powershell',
                        '-Command',
                        f"Expand-Archive -Path '{temp_dir}\\ffmpeg.zip' -DestinationPath '{temp_dir}\\ffmpeg' -Force"
                    ], check=True)
                    
                    # Find ffmpeg.exe
                    ffmpeg_exe = None
                    for root, dirs, files in os.walk(f"{temp_dir}\\ffmpeg"):
                        if "ffmpeg.exe" in files:
                            ffmpeg_exe = os.path.join(root, "ffmpeg.exe")
                            break
                    
                    if ffmpeg_exe:
                        # Copy to a location in PATH
                        bin_dir = os.path.join(os.path.dirname(sys.executable), "Scripts")
                        os.makedirs(bin_dir, exist_ok=True)
                        shutil.copy(ffmpeg_exe, os.path.join(bin_dir, "ffmpeg.exe"))
                        logger.info(f"FFmpeg installed to {bin_dir}")
                        return True
                    else:
                        logger.error("Could not find ffmpeg.exe in the downloaded package")
                        return False
            
            except Exception as e:
                logger.error(f"Failed to install FFmpeg: {str(e)}")
                return False
        else:
            logger.error("FFmpeg not found. Please install FFmpeg manually:")
            logger.error("- Linux: sudo apt-get install ffmpeg")
            logger.error("- macOS: brew install ffmpeg")
            logger.error("- Windows: Download from https://ffmpeg.org/download.html#build-windows")
            return False

def check_audio_stream(file_path):
    """
    Check if a video file contains an audio stream.
    
    Args:
        file_path: Path to the video file
        
    Returns:
        bool: True if the file contains an audio stream, False otherwise
    """
    try:
        # Use FFprobe to get stream information
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'a',  # Select audio streams
            '-show_entries', 'stream=codec_type',
            '-of', 'json',
            file_path
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Check if there's any audio stream
        if result.returncode == 0:
            output = json.loads(result.stdout)
            return 'streams' in output and len(output['streams']) > 0
        
        # Alternative method if ffprobe json output fails
        cmd = [
            'ffmpeg',
            '-i', file_path,
            '-hide_banner'
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Look for audio stream in the output
        output = result.stderr
        return "Stream #" in output and "Audio:" in output
    
    except Exception as e:
        logger.error(f"Error checking audio stream: {str(e)}")
        # Default to attempt conversion if check fails
        return True

def convert_mp4_to_mp3(input_file, progress=gr.Progress()):
    """
    Convert MP4 file to MP3 format using FFmpeg.
    
    Args:
        input_file: The uploaded MP4 file object
        progress: Gradio progress indicator
        
    Returns:
        tuple: (output_file path or None, status message)
    """
    if input_file is None:
        return None, "Please upload a file"
    
    # Update progress
    progress(0, desc="Checking FFmpeg installation...")
    
    # Check if ffmpeg is installed
    if not check_ffmpeg():
        error_msg = "Error: FFmpeg is not installed and could not be automatically installed. Please install FFmpeg manually. Download from ffmpeg.org."
        return None, error_msg
    
    # Generate output filename
    filename = os.path.basename(input_file.name)
    basename, ext = os.path.splitext(filename)
    
    if ext.lower() != '.mp4':
        error_msg = f"Error: Please upload a valid MP4 file. The file you uploaded has extension '{ext}'."
        return None, error_msg
    
    output_file = os.path.join(os.path.dirname(input_file.name), f"{basename}.mp3")
    
    try:
        logger.info(f"Processing file: {input_file.name}")
        progress(0.1, desc="Checking audio streams...")
        
        # Check if the MP4 file has audio streams
        if not check_audio_stream(input_file.name):
            error_msg = "Error: The MP4 file does not contain any audio streams. Cannot convert to MP3. Please choose a video with audio."
            logger.error(error_msg)
            return None, error_msg
        
        progress(0.2, desc="Preparing conversion...")
        
        # Use FFmpeg to convert MP4 to MP3
        cmd = [
            'ffmpeg',
            '-i', input_file.name,  # Input file
            '-vn',                  # Disable video
            '-acodec', 'libmp3lame', # MP3 codec
            '-q:a', '2',            # Quality (0-9, lower is better)
            '-y',                   # Overwrite output file
            output_file             # Output file
        ]
        
        logger.info(f"Running command: {' '.join(cmd)}")
        progress(0.3, desc="Starting conversion...")
        
        # Run the FFmpeg command
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            universal_newlines=True
        )
        
        # Monitor the conversion process
        while process.poll() is None:
            progress(0.5, desc="Converting...")
            time.sleep(0.5)
        
        progress(0.8, desc="Finalizing...")
        
        # Get the process output
        _, stderr = process.communicate()
        
        # Check if the conversion was successful
        if process.returncode != 0:
            logger.error(f"FFmpeg error: {stderr}")
            
            # Check for no streams error specifically
            if "Output file #0 does not contain any stream" in stderr:
                error_msg = "Error: The MP4 file does not contain any audio streams. Cannot convert to MP3. Please choose a different file with audio."
                return None, error_msg
            else:
                error_msg = "Error: FFmpeg conversion failed. The file may be corrupted or use an unsupported codec."
                return None, error_msg
        
        # Check if the output file exists and has content
        if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
            logger.error("Output file was not created or is empty")
            error_msg = "Error: MP3 file could not be created. The MP4 may not contain valid audio."
            return None, error_msg
        
        progress(1.0, desc="Conversion complete!")
        logger.info(f"Conversion successful: {output_file}")
        return output_file, "Conversion successful!"
    
    except Exception as e:
        logger.error(f"Conversion failed: {str(e)}")
        error_msg = f"Error: Conversion failed - {str(e)}"
        return None, error_msg

def create_ui():
    """Create and configure the Gradio interface."""
    
    # Custom CSS for a cleaner look
    css = """
    .gradio-container {
        font-family: 'Arial', sans-serif;
    }
    .footer {
        margin-top: 20px;
        text-align: center;
        font-size: 0.8em;
        color: #666;
    }
    /* Added styles for the processing state */
    .processing {
        opacity: 0.5;
        pointer-events: none;
    }
    .status-message {
        margin-top: 10px;
        padding: 10px;
        border-radius: 4px;
        background-color: #f8f9fa;
        color: #666;
    }
    .error-message {
        color: #dc3545;
        font-weight: bold;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
    """
    
    # Create the interface with progress tracking
    with gr.Blocks(css=css) as interface:
        gr.Markdown("# MP4 to MP3 Tool")
        gr.Markdown("Upload an MP4 video file to convert it to MP3 audio format.")
        
        with gr.Row():
            input_file = gr.File(label="Upload MP4 File")
        
        with gr.Row():
            status = gr.Textbox(
                label="Status", 
                value="Ready", 
                interactive=False
            )
            
        with gr.Row():
            convert_btn = gr.Button("Convert to MP3", variant="primary")
        
        output_file = gr.File(label="Download MP3 File")
        
        # Handle button click event
        convert_btn.click(
            fn=convert_mp4_to_mp3,
            inputs=[input_file],
            outputs=[output_file, status],
            show_progress=True,  # Show progress bar
        )
        
        # Add footer
        gr.Markdown("<div class='footer'>Created with ❤️ using Gradio and FFmpeg | MIT License</div>")
    
    return interface

if __name__ == "__main__":
    # Create and launch the UI
    ui = create_ui()
    ui.launch(share=False, server_port=7860) 