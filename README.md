# File Processor and RegexApp Documentation

## Table of Contents
- [Overview](#overview)
- [Classes](#classes)
  - [FileProcessorApp](#fileprocessorapp)
  - [RegexApp](#regexapp)
- [GUI Components](#gui-components)
- [Workflow](#workflow)
- [Screenshots](#screenshots)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [How to Run](#how-to-run)
- [Notes](#notes)

## Overview

This Python script implements a graphical user interface (GUI) application using the Tkinter library. The application allows users to process Word/PDF files, view the processed content, and perform regular expression pattern matching.

## Classes

### 1. FileProcessorApp

#### Description
The `FileProcessorApp` class manages the file processing functionality. It provides a GUI for users to drag and drop or select Word/PDF files. The processed content is displayed, and users can switch to the `RegexApp` for further pattern matching.

#### Methods
- `__init__(self, root)`: Initializes the FileProcessorApp with the main Tkinter root window.
- `hide(self)`: Hides the current window.
- `show(self)`: Shows the current window.
- `switch_to_file_processor(self)`: Switches to the FileProcessorApp window.
- `switch_to_regex_app(self)`: Switches to the RegexApp window.
- `handle_drop(self, event)`: Handles the drop event when files are dragged and dropped.
- `open_file_dialog(self)`: Opens a file dialog for users to select a file.
- `enable_switch_button(self)`: Enables the switch button to the RegexApp after processing is complete.
- `update_status(self, message)`: Updates the status bar with the given message.
- `process_file(self, file_path)`: Processes the selected file, extracting text content and saving it to 'output.txt'.

### 2. RegexApp

#### Description
The `RegexApp` class manages the regular expression pattern matching functionality. It displays metacharacters, special sequences, and sets. Users can enter a regex pattern to search for matches in the processed text.

#### Methods
- `__init__(self, root)`: Initializes the RegexApp with the main Tkinter root window.
- `hide(self)`: Hides the current window.
- `show(self)`: Shows the current window.
- `switch_to_file_processor(self)`: Switches to the FileProcessorApp window.
- `toggle_edit_mode(self)`: Toggles between view and edit modes for the search results.
- `find_matches(self)`: Finds and displays matches for the entered regex pattern.
- `display_dictionary(self, heading, desc, dictionary)`: Displays dictionaries of metacharacters, special sequences, and sets.

## GUI Components

### 1. FileProcessorApp GUI Components
- Label for instructions
- Drag and drop functionality
- Button to select files
- Status bar
- Switch button to RegexApp

### 2. RegexApp GUI Components
- Text widget for metacharacters, special sequences, and sets
- Entry widget for entering regex patterns
- Button to trigger search
- Labels for displaying total words, matched words, and most frequent words
- Edit button to toggle between view and edit modes
- Text widget for displaying search results


## Workflow

1. User opens the application.
2. In the FileProcessorApp:
   - User drags and drops or selects Word/PDF files.
   - The processed content is displayed.
   - User can switch to the RegexApp for pattern matching.
3. In the RegexApp:
   - User views metacharacters, special sequences, and sets.
   - User enters a regex pattern and clicks the search button.
   - Search results, total words, matched words, and most frequent words are displayed.
   - User can toggle between view and edit modes.
4. User can switch back and forth between FileProcessorApp and RegexApp as needed.

## Screenshots

### 1. FileProcessorApp - Drag and Drop

![Drag and Drop](images/DragAndDrop.png)

### 2. RegexApp - Initial Screen

![Initial Screen](images/InitialScreen.png)

### 3. RegexApp - Used Regex in Action

![Used Regex](images/UsedRegex.png)

## Usage

1. Run the script.
2. Drag and drop or select Word/PDF files in the FileProcessorApp.
3. View processed content and switch to the RegexApp for pattern matching.
4. Enter regex patterns in the RegexApp to search for matches.


## Dependencies

- Tkinter: Python's standard GUI library.
- tkinterdnd2: A Tkinter extension for drag-and-drop functionality.
- pdfplumber: A library for extracting text content from PDF files.


## How to Run

Follow these steps to run the File Processor and RegexApp:

1. Install dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the main script:

    ```bash
    python main.py
    ```

Ensure that you have Python installed on your machine.

## Notes

- The processed content is saved to 'output.txt'.
- The application supports Word (.docx) and PDF (.pdf) file formats.
- Users can explore and understand regex patterns using the RegexApp.
