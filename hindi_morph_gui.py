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
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.minsize(600, 500)
                
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
        dict_path = "enhanced_hindi_dictionary_v2.json" if os.path.exists("enhanced_hindi_dictionary.json") else None
        
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
        input_frame = ttk.LabelFrame(self.main_frame, text="Hindi Text Input", padding="5")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Text input area
        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=8)
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                
        # Sample text button
        sample_frame = ttk.Frame(input_frame)
        sample_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(sample_frame, text="Try sample text:").pack(side=tk.LEFT, padx=5)
        
        sample_texts = [
            "राम घर जाता है।",
            "सीता किताब पढ़ती है।",
            "मैं कल दिल्ली जाऊँगा।"
        ]
        
        for sample in sample_texts:
            btn = ttk.Button(sample_frame, text=sample, command=lambda s=sample: self.load_sample(s))
            btn.pack(side=tk.LEFT, padx=2)
        
        # Button frame
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Analysis type
        ttk.Label(button_frame, text="Analysis Type:").pack(side=tk.LEFT, padx=5)
        
        self.analysis_type = tk.StringVar(value="text")
        ttk.Radiobutton(button_frame, text="Full Text", variable=self.analysis_type, value="text").pack(side=tk.LEFT)
        ttk.Radiobutton(button_frame, text="Single Word", variable=self.analysis_type, value="word").pack(side=tk.LEFT)
        
        # Analyze button
        analyze_btn = ttk.Button(button_frame, text="Analyze", command=self.analyze_text)
        analyze_btn.pack(side=tk.RIGHT, padx=5)
        
        # Clear button
        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_input)
        clear_btn.pack(side=tk.RIGHT, padx=5)
    
    def create_output_frame(self):
        """Create output frame with results area"""
        output_frame = ttk.LabelFrame(self.main_frame, text="Analysis Results", padding="5")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create notebook for different output views
        self.output_notebook = ttk.Notebook(output_frame)
        self.output_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Raw results tab
        self.raw_output_frame = ttk.Frame(self.output_notebook)
        self.output_notebook.add(self.raw_output_frame, text="Raw Analysis")
        
        self.raw_output = scrolledtext.ScrolledText(self.raw_output_frame, wrap=tk.WORD, height=10)
        self.raw_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Formatted results tab
        self.formatted_output_frame = ttk.Frame(self.output_notebook)
        self.output_notebook.add(self.formatted_output_frame, text="Formatted Analysis")
        
        # Treeview for structured output
        self.tree_columns = ("Word", "Root", "Category", "Prefix", "Prefix Features", "Suffix", "Suffix Features", "Sandhi Applied")
        self.formatted_output = ttk.Treeview(self.formatted_output_frame, columns=self.tree_columns, show="headings")
        
        # Configure columns with appropriate widths
        for col in self.tree_columns:
            self.formatted_output.heading(col, text=col)
            if col in ("Prefix Features", "Suffix Features"):
                self.formatted_output.column(col, width=250, minwidth=200)
            elif col == "Sandhi Applied":
                self.formatted_output.column(col, width=120, minwidth=100)
            else:
                self.formatted_output.column(col, width=100, minwidth=80)
        
        # Add scrollbars to treeview
        tree_scrolly = ttk.Scrollbar(self.formatted_output_frame, orient="vertical", command=self.formatted_output.yview)
        tree_scrollx = ttk.Scrollbar(self.formatted_output_frame, orient="horizontal", command=self.formatted_output.xview)
        self.formatted_output.configure(yscrollcommand=tree_scrolly.set, xscrollcommand=tree_scrollx.set)
        
        # Pack the treeview and scrollbars
        tree_scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        self.formatted_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def create_statusbar(self):
        """Create status bar at the bottom of the window"""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_sample(self, sample_text):
        """Load a sample text into the input area"""
        self.input_text.delete(1.0, tk.END)
        self.input_text.insert(tk.END, sample_text)
        self.status_var.set(f"Loaded sample text: {sample_text}")
    
    def clear_input(self):
        """Clear the input text area"""
        self.input_text.delete(1.0, tk.END)
        self.raw_output.delete(1.0, tk.END)
        self.formatted_output.delete(*self.formatted_output.get_children())
        self.status_var.set("Input cleared")
    
    def analyze_text(self):
        """Analyze the input text and display results"""
        input_text = self.input_text.get(1.0, tk.END).strip()
        if not input_text:
            messagebox.showwarning("No Input", "Please enter some Hindi text to analyze.")
            return
        
        try:
            self.status_var.set("Analyzing text...")
            self.root.update_idletasks()
            
            if self.analysis_type.get() == "word":
                # Analyze as a single word
                result = [self.analyzer.analyze(input_text)]
            else:
                # Analyze as full text
                result = self.analyzer.process_text(input_text)
            
            self.display_results(result)
            self.status_var.set(f"Analysis complete: {len(result)} word(s) analyzed")
        
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Error analyzing text: {str(e)}")
            self.status_var.set("Analysis failed")
    
    def display_results(self, results):
        """Display analysis results in the output areas"""
        # Clear previous results
        self.raw_output.delete(1.0, tk.END)
        self.formatted_output.delete(*self.formatted_output.get_children())
        
        # Display raw JSON output
        json_output = json.dumps(results, ensure_ascii=False, indent=4)
        self.raw_output.insert(tk.END, json_output)
        
        # Display formatted output in treeview
        for i, item in enumerate(results):
            word = item.get('original', '')
            root = item.get('root', '')
            category = item.get('root_info', {}).get('category', 'unknown')
            
            # Get prefix information
            prefix = item.get('prefix', '')
            prefix_features = item.get('prefix_features', {})
            prefix_features_str = ', '.join([f"{k}: {v}" for k, v in prefix_features.items()]) if prefix_features else ''
            
            # Get suffix information
            suffix = item.get('suffix', '')
            suffix_features = item.get('suffix_features', {})
            suffix_features_str = ', '.join([f"{k}: {v}" for k, v in suffix_features.items()]) if suffix_features else ''
            
            # Get sandhi information
            sandhi_applied = item.get('sandhi_applied', False)
            sandhi_info = "Yes" if sandhi_applied else "No"
            
            # Add to treeview with sandhi information
            self.formatted_output.insert('', 'end', text=f"item_{i}", 
                                         values=(word, root, category, 
                                                 prefix, prefix_features_str, 
                                                 suffix, suffix_features_str, 
                                                 sandhi_info))
            
            # If sandhi was applied, show details in raw output
            if sandhi_applied:
                self.raw_output.insert(tk.END, f"\n\nSandhi Analysis for '{word}':")
                if prefix:
                    self.raw_output.insert(tk.END, f"\nPrefix-Root Junction: {prefix}+{root}")
                if suffix:
                    self.raw_output.insert(tk.END, f"\nRoot-Suffix Junction: {root}+{suffix}")
                self.raw_output.insert(tk.END, "\n")
    
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
                
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(tk.END, text)
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
