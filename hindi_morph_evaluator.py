#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hindi Morphology Analyzer Evaluator
Tests the analyzer with sample Hindi sentences and evaluates performance
"""

import os
import json
import time
from hindi_morph_analyzer import HindiMorphAnalyzer

def load_test_sentences():
    """Load test sentences for evaluation"""
    return [
        "राम घर जाता है।",                      # Ram goes home.
        "सीता किताब पढ़ती है।",                  # Sita reads a book.
        "लड़के स्कूल में खेल रहे हैं।",           # The boys are playing in the school.
        "मैं कल दिल्ली जाऊँगा।",                 # I will go to Delhi tomorrow.
        "वह बहुत अच्छा गाना गाती है।",            # She sings very well.
        "मेरे पिता अध्यापक हैं।",                # My father is a teacher.
        "बारिश होने के कारण मैं घर पर रहा।",       # I stayed at home because of the rain.
        "क्या तुम मेरे साथ बाज़ार चलोगे?",         # Will you go to the market with me?
        "छोटे बच्चे तेज़ी से सीखते हैं।",          # Small children learn quickly.
        "यह फल बहुत मीठा है।"                   # This fruit is very sweet.
    ]

def evaluate_analyzer_on_sentences(analyzer, sentences):
    """
    Evaluate the morphology analyzer on a set of Hindi sentences
    
    Args:
        analyzer: HindiMorphAnalyzer instance
        sentences: List of Hindi sentences for testing
        
    Returns:
        dict: Performance metrics and analysis results
    """
    results = []
    total_words = 0
    total_time = 0
    
    print("\nEvaluating analyzer on test sentences...")
    
    for sentence in sentences:
        print(f"\nSentence: {sentence}")
        
        # Record start time
        start_time = time.time()
        
        # Process the sentence
        analysis = analyzer.process_text(sentence)
        
        # Record end time
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Count words (excluding punctuation)
        words = [word for word in sentence.split() if not all(c in '।,;.!?:"\'-()' for c in word)]
        word_count = len(words)
        total_words += word_count
        total_time += processing_time
        
        # Display results
        print(f"Word count: {word_count}")
        print(f"Processing time: {processing_time:.4f} seconds")
        print(f"Words per second: {word_count / processing_time:.2f}")
        
        # Display word-by-word analysis
        print("\nWord-by-word analysis:")
        for idx, word_analysis in enumerate(analysis):
            word = word_analysis['original']
            root = word_analysis['root']
            category = word_analysis['root_info'].get('category', 'unknown')
            
            # Get morphological features
            features = []
            if word_analysis['suffix_features']:
                features.extend([f"{k}: {v}" for k, v in word_analysis['suffix_features'].items()])
            
            if word_analysis['prefix_features']:
                features.extend([f"{k}: {v}" for k, v in word_analysis['prefix_features'].items()])
            
            features_str = ", ".join(features) if features else "None"
            
            print(f"  {idx+1}. Word: {word} | Root: {root} | Category: {category} | Features: {features_str}")
        
        # Store result
        results.append({
            'sentence': sentence,
            'word_count': word_count,
            'processing_time': processing_time,
            'words_per_second': word_count / processing_time,
            'analysis': analysis
        })
    
    # Calculate overall metrics
    average_time_per_word = total_time / total_words if total_words > 0 else 0
    words_per_second = total_words / total_time if total_time > 0 else 0
    
    metrics = {
        'total_sentences': len(sentences),
        'total_words': total_words,
        'total_processing_time': total_time,
        'average_time_per_word': average_time_per_word,
        'words_per_second': words_per_second
    }
    
    # Display overall metrics
    print("\nOverall Performance Metrics:")
    print(f"Total sentences: {metrics['total_sentences']}")
    print(f"Total words: {metrics['total_words']}")
    print(f"Total processing time: {metrics['total_processing_time']:.4f} seconds")
    print(f"Average time per word: {metrics['average_time_per_word']:.4f} seconds")
    print(f"Words per second: {metrics['words_per_second']:.2f}")
    
    return {
        'metrics': metrics,
        'results': results
    }

def generate_error_analysis(analyzer, test_data):
    """
    Generate error analysis for specific test cases
    
    Args:
        analyzer: HindiMorphAnalyzer instance
        test_data: List of dictionaries with ground truth
        
    Returns:
        dict: Error analysis results
    """
    error_analysis = []
    
    print("\nGenerating error analysis...")
    
    for item in test_data:
        word = item["word"]
        expected_root = item["root"]
        expected_category = item["category"]
        
        # Analyze the word
        analysis = analyzer.analyze(word)
        
        actual_root = analysis["root"]
        actual_category = analysis["root_info"].get("category", "unknown")
        
        # Check if there's an error in root or category
        if actual_root != expected_root or actual_category != expected_category:
            error = {
                'word': word,
                'expected': {
                    'root': expected_root,
                    'category': expected_category
                },
                'actual': {
                    'root': actual_root,
                    'category': actual_category
                },
                'error_type': []
            }
            
            if actual_root != expected_root:
                error['error_type'].append('root_mismatch')
            
            if actual_category != expected_category:
                error['error_type'].append('category_mismatch')
            
            error_analysis.append(error)
    
    # Display error summary
    if error_analysis:
        print(f"\nFound {len(error_analysis)} errors:")
        for idx, error in enumerate(error_analysis):
            print(f"\n{idx+1}. Word: {error['word']}")
            print(f"   Expected: Root={error['expected']['root']}, Category={error['expected']['category']}")
            print(f"   Actual  : Root={error['actual']['root']}, Category={error['actual']['category']}")
            print(f"   Error types: {', '.join(error['error_type'])}")
    else:
        print("\nNo errors found in the test data.")
    
    return error_analysis

def main():
    """Main function for the evaluator"""
    # Initialize analyzer
    rules_path = "hindi_morph_rules.json"
    dict_path = "enhanced_hindi_dictionary_v2.json"
    
    # Check if files exist, if not create them
    if not os.path.exists(rules_path):
        analyzer = HindiMorphAnalyzer()
        analyzer.save_rules(rules_path)
        print(f"Created default rules file at {rules_path}")
    
    if not os.path.exists(dict_path):
        # Create a minimal dictionary
        with open("hindi_dictionary.json", "r", encoding="utf-8") as f:
            dictionary = json.load(f)
            
        with open(dict_path, "w", encoding="utf-8") as f:
            json.dump(dictionary, f, ensure_ascii=False, indent=2)
        print(f"Created dictionary file at {dict_path}")
    
    # Initialize analyzer with files
    analyzer = HindiMorphAnalyzer(rules_path=rules_path, dictionary_path=dict_path)
    
    # Load test sentences
    sentences = load_test_sentences()
    
    # Evaluate on sentences
    evaluation = evaluate_analyzer_on_sentences(analyzer, sentences)
    
    # Create test data for error analysis
    test_data = [
        {"word": "लड़का", "root": "लड़क", "category": "noun"},
        {"word": "लड़के", "root": "लड़क", "category": "noun"},
        {"word": "पढ़ता", "root": "पढ़", "category": "verb"},
        {"word": "गाती", "root": "गा", "category": "verb"},
        {"word": "अच्छी", "root": "अच्छ", "category": "adjective"},
        {"word": "धीरे", "root": "धीरे", "category": "adverb"},
        {"word": "जाऊँगा", "root": "जा", "category": "verb"},
        {"word": "चलोगे", "root": "चल", "category": "verb"},
        {"word": "है", "root": "हो", "category": "verb"},
        {"word": "हैं", "root": "हो", "category": "verb"}
    ]
    
    # Generate error analysis
    errors = generate_error_analysis(analyzer, test_data)
    
    # Save evaluation results
    output = {
        'sentence_evaluation': evaluation,
        'error_analysis': errors
    }
    
    with open("evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("\nEvaluation complete. Results saved to evaluation_results.json")

if __name__ == "__main__":
    main()
