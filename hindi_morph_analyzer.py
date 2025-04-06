# Hindi Morphology Analyzer
# A rule-based approach for analyzing Hindi words into their morphological components

import re
import json
import os
from collections import defaultdict

class HindiMorphAnalyzer:
    def __init__(self, rules_path=None, dictionary_path=None):
        """
        Initialize the Hindi Morphology Analyzer
        
        Args:
            rules_path: Path to morphological rules file
            dictionary_path: Path to Hindi dictionary/lexicon
        """
        self.suffix_rules = {}
        self.prefix_rules = {}
        self.sandhi_rules = {}
        self.exceptions = {}
        self.dictionary = {}
        
        # Load rules and dictionary if provided
        if rules_path and os.path.exists(rules_path):
            self.load_rules(rules_path)
        else:
            self.initialize_default_rules()
            
        if dictionary_path and os.path.exists(dictionary_path):
            self.load_dictionary(dictionary_path)
        else:
            # Initialize with a minimal dictionary for testing
            self.initialize_minimal_dictionary()
    
    def load_rules(self, rules_path):
        """Load morphological rules from JSON file"""
        try:
            with open(rules_path, 'r', encoding='utf-8') as f:
                rules_data = json.load(f)
                self.suffix_rules = rules_data.get('suffix_rules', {})
                self.prefix_rules = rules_data.get('prefix_rules', {})
                self.sandhi_rules = rules_data.get('sandhi_rules', {})
                self.exceptions = rules_data.get('exceptions', {})
        except Exception as e:
            print(f"Error loading rules: {e}")
            self.initialize_default_rules()
    
    def initialize_default_rules(self):
        """Initialize with basic Hindi morphological rules"""
        # Common noun suffixes (gender, number, case)
        self.suffix_rules = {
            # Masculine singular suffixes
            'ा': {'category': 'noun', 'gender': 'masculine', 'number': 'singular', 'case': 'direct'},
            'े': {'category': 'noun', 'gender': 'masculine', 'number': 'singular/plural', 'case': 'oblique'},
            'ों': {'category': 'noun', 'gender': 'masculine', 'number': 'plural', 'case': 'oblique'},
            
            # Feminine singular suffixes
            'ी': {'category': 'noun', 'gender': 'feminine', 'number': 'singular', 'case': 'direct'},
            'ियाँ': {'category': 'noun', 'gender': 'feminine', 'number': 'plural', 'case': 'direct'},
            'ियों': {'category': 'noun', 'gender': 'feminine', 'number': 'plural', 'case': 'oblique'},
            
            # Verb suffixes
            'ना': {'category': 'verb', 'form': 'infinitive'},
            'ता': {'category': 'verb', 'tense': 'present', 'aspect': 'habitual', 'gender': 'masculine', 'number': 'singular'},
            'ती': {'category': 'verb', 'tense': 'present', 'aspect': 'habitual', 'gender': 'feminine', 'number': 'singular'},
            'ते': {'category': 'verb', 'tense': 'present', 'aspect': 'habitual', 'gender': 'masculine', 'number': 'plural'},
            'या': {'category': 'verb', 'tense': 'past', 'aspect': 'perfective', 'gender': 'masculine', 'number': 'singular'},
            'ई': {'category': 'verb', 'tense': 'past', 'aspect': 'perfective', 'gender': 'feminine', 'number': 'singular'},
            'ए': {'category': 'verb', 'tense': 'past', 'aspect': 'perfective', 'gender': 'masculine', 'number': 'plural'},
            'गा': {'category': 'verb', 'tense': 'future', 'gender': 'masculine', 'number': 'singular', 'person': 'third'},
            'गी': {'category': 'verb', 'tense': 'future', 'gender': 'feminine', 'number': 'singular', 'person': 'third'},
            'गे': {'category': 'verb', 'tense': 'future', 'gender': 'masculine', 'number': 'plural', 'person': 'third'},
        }
        
        # Common prefixes
        self.prefix_rules = {
            'अ': {'meaning': 'negation', 'type': 'negative'},
            'सु': {'meaning': 'good', 'type': 'quality'},
            'दुर्': {'meaning': 'bad', 'type': 'quality'},
            'पुनर्': {'meaning': 'again', 'type': 'repetition'},
        }
        
        # Basic sandhi rules (sound changes)
        self.sandhi_rules = {
            'ा' + 'अ': 'ा',
            'ि' + 'आ': 'ी',
            'ु' + 'आ': 'ू',
        }
    
    def load_dictionary(self, dictionary_path):
        """Load Hindi dictionary/lexicon"""
        try:
            with open(dictionary_path, 'r', encoding='utf-8') as f:
                self.dictionary = json.load(f)
        except Exception as e:
            print(f"Error loading dictionary: {e}")
            self.initialize_minimal_dictionary()
    
    def initialize_minimal_dictionary(self):
        """Initialize with a minimal test dictionary"""
        self.dictionary = {
            # Nouns
            'लड़क': {'category': 'noun', 'meaning': 'boy', 'gender': 'masculine'},
            'लड़की': {'category': 'noun', 'meaning': 'girl', 'gender': 'feminine'},
            'किताब': {'category': 'noun', 'meaning': 'book', 'gender': 'feminine'},
            'घर': {'category': 'noun', 'meaning': 'house', 'gender': 'masculine'},
            
            # Verbs
            'पढ़': {'category': 'verb', 'meaning': 'read'},
            'लिख': {'category': 'verb', 'meaning': 'write'},
            'खा': {'category': 'verb', 'meaning': 'eat'},
            'जा': {'category': 'verb', 'meaning': 'go'},
            'कर': {'category': 'verb', 'meaning': 'do'},
            
            # Adjectives
            'अच्छ': {'category': 'adjective', 'meaning': 'good'},
            'बड़': {'category': 'adjective', 'meaning': 'big'},
            'छोट': {'category': 'adjective', 'meaning': 'small'},
        }
    
    def normalize(self, word):
        """Normalize Hindi text by handling Unicode variations"""
        # Implement Hindi-specific normalization as needed
        # For example, handling half-forms, Nukta, etc.
        return word
    
    def extract_suffix(self, word):
        """
        Extract suffix from a Hindi word
        
        Returns:
            tuple: (root, suffix, features)
        """
        # Sort suffixes by length (longest first) to avoid substring matches
        sorted_suffixes = sorted(self.suffix_rules.keys(), key=len, reverse=True)
        
        for suffix in sorted_suffixes:
            if word.endswith(suffix):
                potential_root = word[:-len(suffix)]
                # Check if root exists in dictionary or is valid
                if potential_root in self.dictionary or len(potential_root) >= 2:
                    return potential_root, suffix, self.suffix_rules[suffix]
        
        # No suffix found
        return word, "", {}
    
    def extract_prefix(self, word):
        """
        Extract prefix from a Hindi word
        
        Returns:
            tuple: (root, prefix, features)
        """
        # Sort prefixes by length (longest first) to avoid substring matches
        sorted_prefixes = sorted(self.prefix_rules.keys(), key=len, reverse=True)
        
        for prefix in sorted_prefixes:
            if word.startswith(prefix):
                potential_root = word[len(prefix):]
                # Check if root exists in dictionary or is valid
                if potential_root in self.dictionary or len(potential_root) >= 2:
                    return potential_root, prefix, self.prefix_rules[prefix]
        
        # No prefix found
        return word, "", {}
    
    def apply_sandhi_rules(self, parts):
        """Apply sandhi rules to handle morphophonemic changes"""
        if not parts or len(parts) < 2:
            return parts
            
        result = parts[0]
        for i in range(1, len(parts)):
            junction = result[-1] + parts[i][0]  # Get the junction point
            
            # Check if this junction has a sandhi rule
            if junction in self.sandhi_rules:
                # Apply the sandhi rule
                combined = result[:-1] + self.sandhi_rules[junction] + parts[i][1:]
                result = combined
            else:
                result += parts[i]
        
        return result
    
    def analyze(self, word):
        """
        Analyze a Hindi word into its morphological components
        
        Args:
            word: Hindi word to analyze
        
        Returns:
            dict: Morphological analysis result
        """
        # Handle exception words
        if word in self.exceptions:
            return self.exceptions[word]
        
        # Normalize the word
        normalized = self.normalize(word)
        
        # Extract suffix
        root_after_suffix, suffix, suffix_features = self.extract_suffix(normalized)
        
        # Extract prefix from the remaining root
        final_root, prefix, prefix_features = self.extract_prefix(root_after_suffix)
        
        # Apply sandhi rules if needed
        if prefix and final_root:
            # Apply sandhi rules at prefix-root junction
            parts = [prefix, final_root]
            combined = self.apply_sandhi_rules(parts)
            final_root = combined[len(prefix):]  # Remove prefix from the combined result
        
        if final_root and suffix:
            # Apply sandhi rules at root-suffix junction
            parts = [final_root, suffix]
            combined = self.apply_sandhi_rules(parts)
            if combined != final_root + suffix:
                # If sandhi rules were applied, update the root
                final_root = combined[:-len(suffix)]
        
        # Lookup root word in dictionary if available
        root_info = self.dictionary.get(final_root, {'category': 'unknown', 'meaning': 'unknown'})
        
        # Combine all morphological information
        analysis = {
            'original': word,
            'normalized': normalized,
            'root': final_root,
            'root_info': root_info,
            'suffix': suffix,
            'suffix_features': suffix_features,
            'prefix': prefix,
            'prefix_features': prefix_features,
            'sandhi_applied': True if prefix or suffix else False
        }
        
        return analysis
    
    def save_rules(self, file_path):
        """Save the current rules to a JSON file"""
        rules_data = {
            'suffix_rules': self.suffix_rules,
            'prefix_rules': self.prefix_rules,
            'sandhi_rules': self.sandhi_rules,
            'exceptions': self.exceptions
        }
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(rules_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving rules: {e}")
            return False

    def process_text(self, text):
        """
        Process a Hindi text and analyze each word
        
        Args:
            text: Hindi text to analyze
        
        Returns:
            list: List of analyzed words
        """
        # Simple tokenization by splitting on whitespace
        # In a full implementation, use a proper Hindi tokenizer
        words = text.split()
        
        results = []
        for word in words:
            # Remove punctuation
            clean_word = re.sub(r'[।,;.!?()[\]{}:"\'-]', '', word)
            if clean_word:
                analysis = self.analyze(clean_word)
                results.append(analysis)
        
        return results

# Utility functions for dataset creation and handling

def create_test_dataset(size=100):
    """Create a simple test dataset for the morphology analyzer"""
    test_data = []
    
    # Nouns with different suffixes
    nouns = [
        {"word": "लड़का", "root": "लड़क", "category": "noun", "gender": "masculine", "number": "singular", "case": "direct"},
        {"word": "लड़के", "root": "लड़क", "category": "noun", "gender": "masculine", "number": "plural", "case": "direct"},
        {"word": "लड़की", "root": "लड़क", "category": "noun", "gender": "feminine", "number": "singular", "case": "direct"},
        {"word": "लड़कियां", "root": "लड़क", "category": "noun", "gender": "feminine", "number": "plural", "case": "direct"},
        {"word": "किताब", "root": "किताब", "category": "noun", "gender": "feminine", "number": "singular", "case": "direct"},
        {"word": "किताबें", "root": "किताब", "category": "noun", "gender": "feminine", "number": "plural", "case": "direct"},
    ]
    
    # Verbs with different forms
    verbs = [
        {"word": "पढ़ना", "root": "पढ़", "category": "verb", "form": "infinitive"},
        {"word": "पढ़ता", "root": "पढ़", "category": "verb", "tense": "present", "aspect": "habitual", "gender": "masculine", "number": "singular"},
        {"word": "पढ़ती", "root": "पढ़", "category": "verb", "tense": "present", "aspect": "habitual", "gender": "feminine", "number": "singular"},
        {"word": "पढ़ा", "root": "पढ़", "category": "verb", "tense": "past", "aspect": "perfective", "gender": "masculine", "number": "singular"},
        {"word": "पढ़ेगा", "root": "पढ़", "category": "verb", "tense": "future", "gender": "masculine", "number": "singular"},
    ]
    
    # Adjectives with different forms
    adjectives = [
        {"word": "अच्छा", "root": "अच्छ", "category": "adjective", "gender": "masculine", "number": "singular"},
        {"word": "अच्छी", "root": "अच्छ", "category": "adjective", "gender": "feminine", "number": "singular"},
        {"word": "अच्छे", "root": "अच्छ", "category": "adjective", "gender": "masculine", "number": "plural"},
    ]
    
    # Combine all categories
    test_data.extend(nouns)
    test_data.extend(verbs)
    test_data.extend(adjectives)
    
    # Limit to requested size
    return test_data[:min(size, len(test_data))]

def evaluate_analyzer(analyzer, test_data):
    """
    Evaluate the morphology analyzer against test data
    
    Args:
        analyzer: HindiMorphAnalyzer instance
        test_data: List of dictionaries with ground truth
    
    Returns:
        dict: Evaluation metrics
    """
    total = len(test_data)
    correct_root = 0
    correct_category = 0
    correct_features = 0
    
    for item in test_data:
        word = item["word"]
        result = analyzer.analyze(word)
        
        # Check root identification
        if result["root"] == item["root"]:
            correct_root += 1
        
        # Check category identification
        if result["root_info"].get("category") == item["category"]:
            correct_category += 1
        
        # Check if key features are identified correctly
        # This is a simplistic approach - in a real implementation, 
        # we'd need more sophisticated feature comparison
        features_match = True
        for key, value in item.items():
            if key not in ["word", "root", "category"]:
                if key not in result["suffix_features"] or result["suffix_features"][key] != value:
                    features_match = False
                    break
        
        if features_match:
            correct_features += 1
    
    return {
        "total": total,
        "root_accuracy": (correct_root / total) * 100 if total > 0 else 0,
        "category_accuracy": (correct_category / total) * 100 if total > 0 else 0,
        "feature_accuracy": (correct_features / total) * 100 if total > 0 else 0,
        "overall_accuracy": ((correct_root + correct_category + correct_features) / (total * 3)) * 100 if total > 0 else 0
    }

# Example usage

def main():
    # Initialize analyzer
    analyzer = HindiMorphAnalyzer("hindi_morph_rules.json", "hindi_dictionary.json")
    
    # Test with sample words
    test_words = [
        "लड़का",    # boy
        "लड़के",    # boys
        "लड़की",    # girl
        "लड़कियां", # girls
        "पढ़ना",    # to read
        "पढ़ता",    # reads (masculine)
        "पढ़ती",    # reads (feminine)
        "पढ़ा",     # read (past, masculine)
        "अच्छा",    # good (masculine)
        "अच्छी"     # good (feminine)
    ]
    
    print("Hindi Morphology Analyzer - Test Results\n")
    print("=" * 50)
    
    for word in test_words:
        analysis = analyzer.analyze(word)
        print(f"\nWord: {word}")
        print(f"Root: {analysis['root']}")
        print(f"Category: {analysis['root_info'].get('category', 'unknown')}")
        
        if analysis['suffix']:
            print(f"Suffix: {analysis['suffix']}")
            features = ", ".join([f"{k}: {v}" for k, v in analysis['suffix_features'].items()])
            print(f"Features: {features}")
        
        if analysis['prefix']:
            print(f"Prefix: {analysis['prefix']}")
            prefix_info = ", ".join([f"{k}: {v}" for k, v in analysis['prefix_features'].items()])
            print(f"Prefix Info: {prefix_info}")
    
    # Create and evaluate on test dataset
    test_data = create_test_dataset()
    metrics = evaluate_analyzer(analyzer, test_data)
    
    print("\n" + "=" * 50)
    print("\nEvaluation Results:")
    print(f"Total test items: {metrics['total']}")
    print(f"Root identification accuracy: {metrics['root_accuracy']:.2f}%")
    print(f"Category identification accuracy: {metrics['category_accuracy']:.2f}%")
    print(f"Feature identification accuracy: {metrics['feature_accuracy']:.2f}%")
    print(f"Overall accuracy: {metrics['overall_accuracy']:.2f}%")

if __name__ == "__main__":
    main()
