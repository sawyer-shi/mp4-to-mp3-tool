#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MP4 to MP3 Converter Application
Main entry point for running the converter application.
"""

from mp4_to_mp3 import create_ui


def main():
    """Main entry point for the application."""
    ui = create_ui()
    ui.launch(share=False, server_port=7860)
    return 0


if __name__ == "__main__":
    main() 