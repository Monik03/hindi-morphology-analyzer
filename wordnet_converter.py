import json
import re

def parse_wordnet_line(line):
    # Split by | to separate definition and example
    parts = line.split('|')
    if len(parts) < 2:
        return None
        
    # Parse the first part to get synset info
    synset_part = parts[0].strip().split()
    if len(synset_part) < 4:
        return None
        
    # Get synonyms
    synonyms = synset_part[3].split(':')
    
    # Get definition
    definition = parts[1].split(':')[0].strip()
    
    # Get examples if present
    examples = []
    if ':' in parts[1]:
        example = parts[1].split(':')[1].strip().strip('"')
        if example:
            examples.append(example)
            
    # Get category info from codes
    category = 'noun'
    if synset_part[1] == '02':
        category = 'adjective'
    elif synset_part[1] == '03':
        category = 'verb'
    elif synset_part[1] == '04':
        category = 'adverb'
        
    return {
        'word': synonyms[0],
        'synonyms': synonyms[1:],
        'category': category,
        'meaning': definition,
        'example': examples[0] if examples else None,
    }

def get_root_word(word):
    """Extract root word by removing both prefixes and suffixes"""
    # Common Hindi prefixes to remove
    prefixes = [
        'अ', 'अन', 'अधि', 'अनु', 'अभि', 'अव', 'आ', 'उप', 'उत्', 
        'दुर्', 'दु', 'निर्', 'नि', 'पर', 'परि', 'प्र', 'प्रति', 
        'सु', 'स', 'सम्', 'सह'
    ]
    
    # Sort prefixes by length (longest first)
    prefixes.sort(key=len, reverse=True)
    
    # Remove prefix if present
    root = word
    original_root = root  # Store original word
    
    for prefix in prefixes:
        if word.startswith(prefix):
            root = word[len(prefix):]
            # If removing prefix results in empty string, keep original
            if not root.strip():
                root = original_root
            break
    
    # Remove suffix inflections
    stripped_root = root.rstrip('ाीेैोौंः')
    
    # If stripping everything results in empty string, return original root
    return stripped_root if stripped_root.strip() else root

def convert_to_dictionary_format():
    dictionary = {}
    
    with open('HindiWN_1_5/database/data_txt', 'r', encoding='utf-8') as f:
        for line in f:
            entry = parse_wordnet_line(line)
            if entry and entry['word'].strip():  # Check for non-empty words
                # Get root word by removing both prefix and suffix
                root = get_root_word(entry['word'])
                
                # Skip entries where root extraction failed
                if not root.strip():
                    continue
                    
                if root not in dictionary:
                    dictionary[root] = {
                        'category': entry['category'],
                        'meaning': entry['meaning'],
                        'gender': 'masculine' if entry['word'].endswith('ा') else 'feminine',
                        'example': entry['example'],
                        'base_forms': [entry['word']],
                        'synonyms': entry['synonyms']
                        # 'original_word': entry['word']  # Store original word for reference
                    }
                else:
                    # If root exists, add the word to base forms if not already present
                    if entry['word'] not in dictionary[root]['base_forms']:
                        dictionary[root]['base_forms'].append(entry['word'])
                    # Add new synonyms if not already present
                    dictionary[root]['synonyms'].extend(
                        [syn for syn in entry['synonyms'] 
                         if syn not in dictionary[root]['synonyms']]
                    )
                    
    return dictionary

# Generate enhanced dictionary
dictionary = convert_to_dictionary_format()

# Save to JSON file
with open('enhanced_hindi_dictionary_v2.json', 'w', encoding='utf-8') as f:
    json.dump(dictionary, f, ensure_ascii=False, indent=2)