#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for the MP4 to MP3 converter.
"""

import os
import unittest
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from mp4_to_mp3 import convert_mp4_to_mp3


class TestMP4ToMP3Converter(unittest.TestCase):
    """Test cases for the MP4 to MP3 converter."""

    def setUp(self):
        """Set up test environment."""
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary directory
        shutil.rmtree(self.temp_dir)
    
    @patch('mp4_to_mp3.VideoFileClip')
    def test_convert_mp4_to_mp3_success(self, mock_video_file_clip):
        """Test successful conversion."""
        # Set up mock
        mock_video = MagicMock()
        mock_video.audio = MagicMock()
        mock_video_file_clip.return_value = mock_video
        
        # Create a test file
        test_file = os.path.join(self.temp_dir, 'test.mp4')
        with open(test_file, 'w') as f:
            f.write('dummy data')
        
        # Create mock input file
        mock_input = MagicMock()
        mock_input.name = test_file
        
        # Call the function
        result = convert_mp4_to_mp3(mock_input)
        
        # Verify the result
        expected_output = os.path.join(self.temp_dir, 'test.mp3')
        self.assertEqual(result, expected_output)
        
        # Verify the function called the right methods
        mock_video_file_clip.assert_called_once_with(test_file)
        mock_video.audio.write_audiofile.assert_called_once()
        mock_video.close.assert_called_once()
    
    def test_convert_mp4_to_mp3_none_input(self):
        """Test with None input."""
        result = convert_mp4_to_mp3(None)
        self.assertEqual(result, "Please upload a file")
    
    def test_convert_mp4_to_mp3_invalid_extension(self):
        """Test with invalid file extension."""
        # Create mock input file with wrong extension
        mock_input = MagicMock()
        mock_input.name = 'test.avi'
        
        # Call the function
        result = convert_mp4_to_mp3(mock_input)
        
        # Verify the result
        self.assertEqual(result, "Please upload a valid MP4 file")
    
    @patch('mp4_to_mp3.VideoFileClip')
    def test_convert_mp4_to_mp3_no_audio(self, mock_video_file_clip):
        """Test with video that has no audio."""
        # Set up mock with no audio
        mock_video = MagicMock()
        mock_video.audio = None
        mock_video_file_clip.return_value = mock_video
        
        # Create mock input file
        mock_input = MagicMock()
        mock_input.name = 'test.mp4'
        
        # Call the function
        result = convert_mp4_to_mp3(mock_input)
        
        # Verify the result
        self.assertEqual(result, "The uploaded MP4 file does not contain audio")
        mock_video.close.assert_called_once()
    
    @patch('mp4_to_mp3.VideoFileClip')
    def test_convert_mp4_to_mp3_exception(self, mock_video_file_clip):
        """Test exception handling."""
        # Set up mock to raise an exception
        mock_video_file_clip.side_effect = Exception("Test error")
        
        # Create mock input file
        mock_input = MagicMock()
        mock_input.name = 'test.mp4'
        
        # Call the function
        result = convert_mp4_to_mp3(mock_input)
        
        # Verify the result
        self.assertEqual(result, "Error: Test error")


if __name__ == '__main__':
    unittest.main() 