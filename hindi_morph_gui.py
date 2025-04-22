#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hindi Morphology Analyzer GUI
A graphical user interface for the Hindi Morphology Analyzer
"""

import os
import sys
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from hindi_morph_analyzer import HindiMorphAnalyzer

# Add DPI awareness
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

class HindiMorphGUI:
    def __init__(self, root):
        self.root = root
        # Enable high DPI scaling
        self.root.tk.call('tk', 'scaling', 2.0)
        
        self.root.title("Hindi Morphology Analyzer")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        self.root.minsize(600, 700)
                
        # Initialize analyzer
        self.initialize_analyzer()
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create UI elements
        self.create_menu()
        self.create_input_frame()
        self.create_output_frame()
        self.create_statusbar()
    

    def initialize_analyzer(self):
        """Initialize the morphology analyzer"""
        rules_path = "hindi_morph_rules.json" if os.path.exists("hindi_morph_rules.json") else None
        dict_path = "enhanced_hindi_dictionary_v2.json" if os.path.exists("enhanced_hindi_dictionary_v2.json") else None
        
        self.analyzer = HindiMorphAnalyzer(rules_path=rules_path, dictionary_path=dict_path)
        self.rules_path = rules_path
        self.dict_path = dict_path
    
    def create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Text", command=self.open_text_file)
        file_menu.add_command(label="Save Results", command=self.save_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Configure menu
        config_menu = tk.Menu(menubar, tearoff=0)
        config_menu.add_command(label="Load Rules", command=self.load_rules)
        config_menu.add_command(label="Load Dictionary", command=self.load_dictionary)
        menubar.add_cascade(label="Configure", menu=config_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Help", command=self.show_help)
        menubar.add_cascade(label="Help", menu=help_menu)
                
        self.root.config(menu=menubar)
    
    def create_input_frame(self):
        """Create input frame with text area and buttons"""
        input_frame = ttk.LabelFrame(self.main_frame, text="Enter Hindi Word", padding="5")
        input_frame.pack(fill=tk.BOTH, pady=5)
        
        # Text input area - single line
        self.input_text = ttk.Entry(input_frame)
        self.input_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Sample words frame
        sample_frame = ttk.LabelFrame(input_frame, text="Sample Words", padding="5")
        sample_frame.pack(fill=tk.X, padx=5, pady=5)
        
        sample_words = [
            "लड़का",
            "पढ़ता",
            "अशुभ",
            "सुरक्षा",
            "अप्रसन्नता"
        ]
        
        # Create sample word buttons in a grid
        for i, word in enumerate(sample_words):
            btn = ttk.Button(sample_frame, text=word, 
                            command=lambda w=word: self.load_sample(w))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2, sticky='ew')
        
        # Button frame
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Analyze and Clear buttons
        analyze_btn = ttk.Button(button_frame, text="Analyze", command=self.analyze_text)
        analyze_btn.pack(side=tk.RIGHT, padx=5)
        
        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_input)
        clear_btn.pack(side=tk.RIGHT, padx=5)
    
    def create_output_frame(self):
        """Create output frame with results area"""
        output_frame = ttk.LabelFrame(self.main_frame, text="Analysis Results", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Main results frame with centered content
        result_frame = ttk.Frame(output_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create frames for each result row with distinctive styling
        self.result_word_var = tk.StringVar()
        self.result_root_var = tk.StringVar()
        self.result_prefix_var = tk.StringVar()
        self.result_suffix_var = tk.StringVar()
        
        # Word frame
        word_frame = ttk.Frame(result_frame, padding="5")
        word_frame.pack(fill=tk.X, pady=5)
        ttk.Label(word_frame, text="Word:", width=15, anchor=tk.E).pack(side=tk.LEFT, padx=5)
        ttk.Label(word_frame, textvariable=self.result_word_var, font=('Nirmala UI', 14, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Root frame with highlight
        root_frame = ttk.Frame(result_frame, padding="5")
        root_frame.pack(fill=tk.X, pady=5)
        ttk.Label(root_frame, text="Root:", width=15, anchor=tk.E).pack(side=tk.LEFT, padx=5)
        self.root_label = ttk.Label(root_frame, textvariable=self.result_root_var, font=('Nirmala UI', 13))
        self.root_label.pack(side=tk.LEFT, padx=5)
        
        # Prefix frame
        prefix_frame = ttk.Frame(result_frame, padding="5")
        prefix_frame.pack(fill=tk.X, pady=5)
        ttk.Label(prefix_frame, text="Prefix:", width=15, anchor=tk.E).pack(side=tk.LEFT, padx=5)
        self.prefix_label = ttk.Label(prefix_frame, textvariable=self.result_prefix_var, font=('Nirmala UI', 12))
        self.prefix_label.pack(side=tk.LEFT, padx=5)
        
        # Suffix frame
        suffix_frame = ttk.Frame(result_frame, padding="5")
        suffix_frame.pack(fill=tk.X, pady=5)
        ttk.Label(suffix_frame, text="Suffix:", width=15, anchor=tk.E).pack(side=tk.LEFT, padx=5)
        self.suffix_label = ttk.Label(suffix_frame, textvariable=self.result_suffix_var, font=('Nirmala UI', 12))
        self.suffix_label.pack(side=tk.LEFT, padx=5)
        
        # Add Detail View button centered at bottom
        button_frame = ttk.Frame(output_frame)
        button_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)
        detail_btn = ttk.Button(button_frame, text="Show Details", command=self.show_details)
        detail_btn.pack(side=tk.BOTTOM, anchor=tk.CENTER)

    def show_details(self):
        """Show detailed information about the analyzed word"""
        if not hasattr(self, 'last_result') or not self.last_result:
            messagebox.showinfo("Info", "No analysis results available")
            return
            
        # Get the full analysis from stored results
        analysis = self.last_result[0]  # Since we're only analyzing one word
        word = analysis['original']
        
        details = f"Detailed Analysis for '{word}'\n\n"
        details += f"Root Word: {analysis['root']}\n"
        
        if 'root_info' in analysis and analysis['root_info']:
            if analysis['root_info'].get('meaning'):
                details += f"Meaning: {analysis['root_info']['meaning']}\n"
            if analysis['root_info'].get('category'):
                details += f"Category: {analysis['root_info']['category']}\n"
        
        if analysis.get('prefix', ''):
            details += f"\nPrefix Information:\n"
            details += "\n".join([f"{k}: {v}" for k, v in analysis['prefix_features'].items()])
        
        if analysis.get('suffix', ''):
            details += f"\n\nSuffix Information:\n"
            details += "\n".join([f"{k}: {v}" for k, v in analysis['suffix_features'].items()])
        
        # Enhanced sandhi information
        if analysis.get('sandhi_applied'):
            details += f"\n\nSandhi Applied: Yes"
            # Get sandhi rules from the analyzer
            sandhi_rules = self.analyzer.sandhi_rules if hasattr(self.analyzer, 'sandhi_rules') else {}
            
            # Display information about prefix-root junction if applicable
            if analysis.get('prefix') and analysis.get('root'):
                junction = f"{analysis['prefix'][-1]}+{analysis['root'][0]}"
                # Check if the junction is in the sandhi rules
                if junction in sandhi_rules:
                    details += f"\n\nPrefix-Root Junction: {analysis['prefix']} + {analysis['root']}"
                    details += f"\nSandhi Rule Applied: {junction} → {sandhi_rules[junction]}"
                    # details += f"\nExample: {analysis['prefix'][:-1]}{sandhi_rules[junction]}{analysis['root'][1:]}"
                
            # Display information about root-suffix junction if applicable
            if analysis.get('root') and analysis.get('suffix'):
                junction = f"{analysis['root'][-1]}+{analysis['suffix'][0]}"
                if junction in sandhi_rules:
                    details += f"\n\nRoot-Suffix Junction: {analysis['root']} + {analysis['suffix']}"
                    details += f"\nSandhi Rule Applied: {junction} → {sandhi_rules[junction]}"
                    # details += f"\nExample: {analysis['root'][:-1]}{sandhi_rules[junction]}{analysis['suffix'][1:]}"
        
        messagebox.showinfo("Detailed Analysis", details)

    def create_statusbar(self):
        """Create status bar at the bottom of the window"""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_sample(self, sample_text):
        """Load a sample text into the input area"""
        self.input_text.delete(0, tk.END)
        self.input_text.insert(0, sample_text)
        self.status_var.set(f"Loaded sample text: {sample_text}")
    
    def clear_input(self):
        """Clear the input text area"""
        self.input_text.delete(0, tk.END)
        self.result_word_var.set("")
        self.result_root_var.set("")
        self.result_prefix_var.set("")
        self.result_suffix_var.set("")
        self.status_var.set("Input cleared")
    
    def analyze_text(self):
        """Analyze the input word and display results"""
        input_word = self.input_text.get().strip()
        if not input_word:
            messagebox.showwarning("No Input", "Please enter a Hindi word to analyze.")
            return
        
        try:
            self.status_var.set("Analyzing word...")
            self.root.update_idletasks()
            
            # Analyze single word
            result = [self.analyzer.analyze(input_word)]
            self.last_result = result  # Store for details view
            
            # Display results
            self.display_results(result)
            self.status_var.set("Analysis complete")
        
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Error analyzing word: {str(e)}")
            self.status_var.set("Analysis failed")

    def display_results(self, results):
        """Display analysis results using StringVar variables"""
        if not results or len(results) == 0:
            return
            
        # Get the first result (we're only analyzing one word at a time)
        item = results[0]
        
        # Update the StringVar values
        self.result_word_var.set(item['original'])
        self.result_root_var.set(item['root'])
        self.result_prefix_var.set(item.get('prefix', '-'))
        self.result_suffix_var.set(item.get('suffix', '-'))
        
        # Store the result for details view
        self.last_result = results

    def open_text_file(self):
        """Open a text file for analysis"""
        file_path = filedialog.askopenfilename(
            title="Open Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                
                self.input_text.delete(0, tk.END)
                self.input_text.insert(0, text)
                self.status_var.set(f"Loaded file: {os.path.basename(file_path)}")
            
            except Exception as e:
                messagebox.showerror("File Error", f"Error opening file: {str(e)}")
    
    def save_results(self):
        """Save analysis results to a file"""
        file_path = filedialog.asksaveasfilename(
            title="Save Results",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                raw_output = self.raw_output.get(1.0, tk.END).strip()
                
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(raw_output)
                
                self.status_var.set(f"Results saved to: {os.path.basename(file_path)}")
            
            except Exception as e:
                messagebox.showerror("Save Error", f"Error saving results: {str(e)}")
    
    def load_rules(self):
        """Load morphological rules from a JSON file"""
        file_path = filedialog.askopenfilename(
            title="Load Rules File",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.analyzer.load_rules(file_path)
                self.rules_path = file_path
                self.status_var.set(f"Rules loaded from: {os.path.basename(file_path)}")
            
            except Exception as e:
                messagebox.showerror("Rules Error", f"Error loading rules: {str(e)}")
    
    def load_dictionary(self):
        """Load dictionary from a JSON file"""
        file_path = filedialog.askopenfilename(
            title="Load Dictionary File",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.analyzer.load_dictionary(file_path)
                self.dict_path = file_path
                self.status_var.set(f"Dictionary loaded from: {os.path.basename(file_path)}")
            
            except Exception as e:
                messagebox.showerror("Dictionary Error", f"Error loading dictionary: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Hindi Morphology Analyzer
Version 1.0

A tool for analyzing the morphological structure of Hindi words.
This application demonstrates a rule-based approach to Hindi morphology.

© 2025 Hindi Morphology NLP Project"""
        
        messagebox.showinfo("About", about_text)
    
    def show_help(self):
        """Show help dialog"""
        help_text = """Hindi Morphology Analyzer Help

Input:
- Enter Hindi text in the input box
- Choose "Full Text" to analyze entire text or "Single Word" for a single word
- Click "Analyze" to process

Results:
- Raw Analysis: Shows complete JSON output
- Formatted Analysis: Shows structured results in table format

Configuration:
- Load custom rules and dictionary files from the Configure menu

For more information, visit the documentation."""
        
        messagebox.showinfo("Help", help_text)

def main():
    root = tk.Tk()
    # Set DPI-aware font sizes
    default_font = ('Nirmala UI', 11)  # Use a better font for Hindi text
    heading_font = ('Nirmala UI', 12)

    # Configure fonts for different widget types
    root.option_add('*Font', default_font)
    root.option_add('*TButton*Font', default_font)
    root.option_add('*TLabel*Font', default_font)
    root.option_add('*TLabelframe*Font', heading_font)
    root.option_add('*Treeview*Font', default_font)

    # Adjust Treeview row height by setting a larger font
    style = ttk.Style()
    style.configure('Treeview', rowheight=30)  # Increase row height for better visibility

    app = HindiMorphGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
