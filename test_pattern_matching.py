#!/usr/bin/env python3
"""Test script for pattern matching functionality"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the intents and function from complete_ayurveda_assistant.py
from complete_ayurveda_assistant import enhanced_match_intent, intents

def test_pattern_matching():
    """Test the enhanced pattern matching function"""
    test_cases = [
        'I have acne',
        'I have a cold', 
        'acne',
        'cold',
        'I feel cold',
        'pimples on my face',
        'headache',
        'I have a headache',
        'feeling cold',
        'skin breakout',
        'runny nose',
        'sneezing'
    ]
    
    print('Testing pattern matching:')
    print('=' * 50)
    
    for test_input in test_cases:
        result = enhanced_match_intent(test_input)
        if result:
            print(f'Input: "{test_input}" -> Matched: {result["tag"]}')
        else:
            print(f'Input: "{test_input}" -> No match found')
    
    print('\n' + '=' * 50)
    print('Pattern matching test completed!')

if __name__ == "__main__":
    test_pattern_matching()
