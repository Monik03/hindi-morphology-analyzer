# Hindi Morphology Analyzer

A graphical tool for analyzing the morphological structure of Hindi words and text. This application demonstrates a rule-based approach to Hindi morphology, enabling the analysis of word structure, roots, prefixes, suffixes, and sandhi formations in Hindi text.

## Project Overview

The Hindi Morphology Analyzer is designed to break down Hindi words into their constituent morphological components:
- Root word identification
- Prefix and suffix detection
- Part of speech recognition
- Grammatical feature extraction (gender, number, case, tense, etc.)
- Sandhi (sound change) analysis at morpheme boundaries

## Features

- **Text Analysis**: Analyze full text or individual words
- **Dual Output Views**: Raw JSON data and formatted tabular results
- **Sample Text**: Includes built-in sample texts to demonstrate functionality
- **File Operations**: Open text files and save analysis results
- **Configurable**: Load custom morphological rules and dictionaries

## Requirements

- Python 3.6 or higher
- Tkinter (usually included with Python installation)
- Hindi Unicode font support

## Dependencies

- No external Python packages required beyond the standard library

## Project Structure

- `hindi_morph_gui.py`: The main GUI application
- `hindi_morph_analyzer.py`: Core analyzer engine
- `hindi_morph_rules.json`: Rules for Hindi morphology analysis
- `enhanced_hindi_dictionary_v2.json`: Dictionary of Hindi root words
- `wordnet_converter.py`: Utility to convert WordNet data to the dictionary format

## Installation

1. Clone the repository or download all project files
2. Ensure you have Python 3.6+ installed
3. Make sure you have a Hindi Unicode font installed on your system (e.g., Nirmala UI)

## Usage

### Running the Application

```bash
python hindi_morph_gui.py
```

### Basic Usage Steps

1. Enter Hindi text in the input box or use one of the sample texts
2. Select analysis type:
   - **Full Text**: Analyzes the entire text and processes each word
   - **Single Word**: Treats input as a single word for detailed analysis
3. Click "Analyze" to perform the morphological analysis
4. View results in either Raw Analysis (JSON) or Formatted Analysis (table) tabs

### Configuration

- **Load Rules**: Import custom morphological rule sets via Configure → Load Rules
- **Load Dictionary**: Import custom word dictionaries via Configure → Load Dictionary

## Creating a Custom Dictionary

The project includes `wordnet_converter.py` which can convert Hindi WordNet data into the required dictionary format. To use:

1. Obtain Hindi WordNet data in the expected format
2. Run the converter:
   ```bash
   python wordnet_converter.py
   ```
3. The output will be saved as `enhanced_hindi_dictionary_v2.json`

## Technical Details

### Morphological Analysis Approach

The analyzer uses a rule-based approach with the following steps:
1. Word normalization
2. Root extraction using prefix and suffix identification
3. Morphological feature extraction based on affixes
4. Dictionary lookup for root word verification
5. Sandhi (phonological change) detection at morpheme boundaries

### Rule Structure

The rules are stored in `hindi_morph_rules.json` and include:
- Suffix rules with associated grammatical features
- Prefix rules with semantic meanings
- Derivational rules for word formation
- Sandhi rules for handling phonological changes
- Exception handling for irregular forms

## License

This project is provided for educational and research purposes.

## Acknowledgments

- Based on Hindi WordNet data for dictionary creation
- Implements linguistic principles of Hindi morphology
