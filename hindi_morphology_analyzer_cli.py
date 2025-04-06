#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hindi Morphology Analyzer CLI
A command-line interface for the Hindi Morphology Analyzer
"""

import os
import argparse
import json
from hindi_morph_analyzer import HindiMorphAnalyzer, create_test_dataset, evaluate_analyzer

def setup_argument_parser():
    """Set up command line argument parser"""
    parser = argparse.ArgumentParser(description='Hindi Morphology Analyzer CLI')
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze Hindi words or text')
    analyze_parser.add_argument('input', help='Hindi word or text to analyze')
    analyze_parser.add_argument('--rules', help='Path to rules file (JSON)')
    analyze_parser.add_argument('--dict', help='Path to dictionary file (JSON)')
    analyze_parser.add_argument('--out', help='Output file path (JSON)')
    analyze_parser.add_argument('--format', choices=['json', 'text'], default='text',
                              help='Output format (default: text)')
    
    # Evaluate command
    eval_parser = subparsers.add_parser('evaluate', help='Evaluate analyzer against test data')
    eval_parser.add_argument('--rules', help='Path to rules file (JSON)')
    eval_parser.add_argument('--dict', help='Path to dictionary file (JSON)')
    eval_parser.add_argument('--test-data', help='Path to test data file (JSON)')
    eval_parser.add_argument('--out', help='Output file path for evaluation results (JSON)')
    
    # Create test data command
    testdata_parser = subparsers.add_parser('create-test-data', help='Create sample test data')
    testdata_parser.add_argument('--size', type=int, default=100, help='Number of test items to create')
    testdata_parser.add_argument('--out', required=True, help='Output file path (JSON)')
    
    return parser

def analyze_input(args):
    """Analyze Hindi input text"""
    # Initialize analyzer
    analyzer = HindiMorphAnalyzer(
        rules_path=args.rules,
        dictionary_path=args.dict
    )
    
    # Check if input is a single word or text
    if ' ' in args.input:
        results = analyzer.process_text(args.input)
    else:
        results = [analyzer.analyze(args.input)]
    
    # Output results
    if args.format == 'json':
        output = json.dumps(results, ensure_ascii=False, indent=2)
        if args.out:
            with open(args.out, 'w', encoding='utf-8') as f:
                f.write(output)
        else:
            print(output)
    else:  # text format
        output_text = ""
        for idx, result in enumerate(results):
            output_text += f"Analysis {idx+1}: {result['original']}\n"
            output_text += f"  Root: {result['root']}\n"
            output_text += f"  Category: {result['root_info'].get('category', 'unknown')}\n"
            
            if result['suffix']:
                output_text += f"  Suffix: {result['suffix']}\n"
                features = ", ".join([f"{k}: {v}" for k, v in result['suffix_features'].items()])
                output_text += f"  Features: {features}\n"
            
            if result['prefix']:
                output_text += f"  Prefix: {result['prefix']}\n"
                prefix_info = ", ".join([f"{k}: {v}" for k, v in result['prefix_features'].items()])
                output_text += f"  Prefix Info: {prefix_info}\n"
            
            output_text += "\n"
        
        if args.out:
            with open(args.out, 'w', encoding='utf-8') as f:
                f.write(output_text)
        else:
            print(output_text)

def evaluate_analyzer_cli(args):
    """Evaluate analyzer against test data"""
    # Initialize analyzer
    analyzer = HindiMorphAnalyzer(
        rules_path=args.rules,
        dictionary_path=args.dict
    )
    
    # Load test data or create default
    if args.test_data and os.path.exists(args.test_data):
        with open(args.test_data, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
    else:
        test_data = create_test_dataset()
    
    # Run evaluation
    metrics = evaluate_analyzer(analyzer, test_data)
    
    # Output results
    output = json.dumps(metrics, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(output)
    else:
        print("\nEvaluation Results:")
        print(f"Total test items: {metrics['total']}")
        print(f"Root identification accuracy: {metrics['root_accuracy']:.2f}%")
        print(f"Category identification accuracy: {metrics['category_accuracy']:.2f}%")
        print(f"Feature identification accuracy: {metrics['feature_accuracy']:.2f}%")
        print(f"Overall accuracy: {metrics['overall_accuracy']:.2f}%")

def create_test_data_cli(args):
    """Create sample test data"""
    test_data = create_test_dataset(args.size)
    
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print(f"Created test dataset with {len(test_data)} items at {args.out}")

def main():
    """Main entry point for CLI"""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    if args.command == 'analyze':
        analyze_input(args)
    elif args.command == 'evaluate':
        evaluate_analyzer_cli(args)
    elif args.command == 'create-test-data':
        create_test_data_cli(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
