import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog
import pdfplumber
import re
from tkinter import filedialog
from tkinter import ttk  # For themed widgets
from collections import Counter


class FileProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Regex App")
        self.root.geometry("800x600")
        self.root.configure(bg='#f5f5f5')  # Set background color

        # Create a label for instructions
        self.label = ttk.Label(root, text="Drag and drop Word/PDF files here or click the button to select a file", font=('Roboto', 16))
        self.label.pack(pady=10)

        # Enable drop functionality
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)

        # Create a button with a plus sign
        self.plus_button = tk.Button(root, text='+', font=('Roboto', 30), width=3, height=1, command=self.open_file_dialog)
        self.plus_button.pack(pady=10)

        # Create a status bar
        self.status = ttk.Label(root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def hide(self):
        # Hide the current window
        self.root.withdraw()

    def show(self):
        # Show the current window
        self.root.deiconify()

    def switch_to_file_processor(self):
        # Switch to the FileProcessorApp
        self.hide()
        file_processor_app.show()

    # Modify the switch_to_regex_app method in FileProcessorApp
    def switch_to_regex_app(self):
        # Hide the FileProcessorApp
        self.hide()

        # Create and run the RegexApp window
        regex_root = tk.Tk()
        global regex_app  # Make regex_app a global variable to access it later
        regex_app = RegexApp(regex_root)
        regex_root.protocol("WM_DELETE_WINDOW", self.switch_to_file_processor)  # Handle window close event
        regex_root.mainloop()

    def handle_drop(self, event):
        file_path = event.data
        file_path = file_path.strip('{}')  # Remove the curly braces if they are present
        self.process_file(file_path)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()  # filetypes=[("Word Documents", "*.docx"), ("PDF Documents", "*.pdf")]
        if file_path:
            self.process_file(file_path)

    def enable_switch_button(self):
        self.switch_button = tk.Button(root, text="Go to Regex APP", command=self.switch_to_regex_app)
        self.switch_button.pack(pady=10)
        # Enable the switch button
        self.switch_button.config(state=tk.NORMAL)
        
    def update_status(self, message):
        # Update the status bar with the given message
        self.status.config(text=message)
        self.root.update_idletasks()

    def process_file(self, file_path):
        processed = False
        if file_path.lower().endswith(('.docx', '.pdf')):
            if file_path.lower().endswith('.docx'):
                # Handle Word document
                try:
                    with open(file_path, 'r') as doc_file:
                        content = doc_file.read()
                                            # Write the content to a text file
                    with open('output.txt', 'w') as output_file:
                        output_file.write(content)
                    processed=True
                except:
                    self.update_status("Unsupported file format. Encoding Error")

            elif file_path.lower().endswith('.pdf'):
                # Handle PDF document
                with pdfplumber.open(file_path) as pdf:
                    content = ''
                    for page in pdf.pages:
                        try:
                            for line in page.extract_text(x_tolerance=1).split('\n'):
                                content += line + '\n'
                                                # Write the content to a text file
                            with open('output.txt', 'w') as output_file:
                                output_file.write(content)
                            processed=True
                        except:
                            self.update_status("Unsupported file format. Encoding Error")

            # Enable the switch button after processing is complete
        if processed == True:
            self.root.after(0, self.enable_switch_button)  # Adjust the delay (in milliseconds) as needed
            self.update_status(f"Successfully processed {file_path}")
        else:
            self.update_status("Unsupported file format. Please select a Word (.docx) or PDF (.pdf) file.")



class RegexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RegEx(Regular Expression) for Pattern Matching")

        # Create a frame for the left half of the window
        self.left_frame = tk.Frame(root, bd=5, relief='sunken')
        self.left_frame.grid(row=0, column=0, rowspan=2, sticky='nswe')

        # Create a scrollbar in the left frame
        self.scrollbar = tk.Scrollbar(self.left_frame, width=30, bg='blue')
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a text widget in the left frame
        self.text_widget = tk.Text(self.left_frame, wrap=tk.WORD, font=("Roboto", 14), yscrollcommand=self.scrollbar.set)
        self.text_widget.pack(fill='both', expand=True, padx=10, pady=10)

        # Attach the scrollbar to the text widget
        self.scrollbar.config(command=self.text_widget.yview)

        # Define a tag for bold text
        self.text_widget.tag_configure("bold", font=("Helvetica", 12, "bold"))

                # Metacharacters and their descriptions
        self.metacharacters = {
            '[]': 'A set of characters',
            '\\': 'Signals a special sequence (can also be used to escape special characters)',
            '.': 'Any character (except newline character)',
            '^': 'String Starts with',
            '$': 'String Ends with',
            '*': 'Zero or more occurrences',
            '+': 'One or more occurrences',
            '?': 'Zero or one occurrences',
            '{}': 'Exactly the specified number of occurrences',
            '|': 'Either or',
            '()': 'Capture and group'
        }

        # Special sequences and their descriptions
        self.special_sequences = {
            '\\A': 'Returns a match if the specified characters are at the beginning of the string',
            '\\b': 'Returns a match where the specified characters are at the beginning or at the end of a word',
            '\\B': 'Returns a match where the specified characters are present, but NOT at the beginning (or at the end) of a word',
            '\\d': 'Returns a match where the string contains digits (numbers from 0-9)',
            '\\D': 'Returns a match where the string DOES NOT contain digits',
            '\\s': 'Returns a match where the string contains a white space character',
            '\\S': 'Returns a match where the string DOES NOT contain a white space character',
            '\\w': 'Returns a match where the string contains any word characters (characters from a to Z, digits from 0-9, and the underscore _ character)',
            '\\W': 'Returns a match where the string DOES NOT contain any word characters',
            '\\Z': 'Returns a match if the specified characters are at the end of the string'
        }

        # Sets and their descriptions
        self.sets = {
            '[arn]': 'Returns a match where one of the specified characters (a, r, or n) is present',
            '[a-n]': 'Returns a match for any lower case character, alphabetically between a and n',
            '[^arn]': 'Returns a match for any character EXCEPT a, r, and n',
            '[0123]': 'Returns a match where any of the specified digits (0, 1, 2, or 3) are present',
            '[0-9]': 'Returns a match for any digit between 0 and 9',
            '[0-5][0-9]': 'Returns a match for any two-digit numbers from 00 and 59',
            '[a-zA-Z]': 'Returns a match for any character alphabetically between a and z, lower case OR upper case',
            '[+]': 'In sets, +, *, ., |, (), $,{} has no special meaning, so [+] means: return a match for any + character in the string'
        }

        # Display dictionary in the text widget
        self.display_dictionary("\n   Metacharacters", "   Metacharacters are characters with a special meaning:\n\n", self.metacharacters)
        self.display_dictionary("\n    Special Sequences", "    A special sequence is a \\ followed by one of the characters in the list below, and has a special meaning:\n\n", self.special_sequences)
        self.display_dictionary("\n Sets", "     A set is a set of characters inside a pair of square brackets [] with a special meaning:\n\n", self.sets)

        # Create a frame for the top half of the right side of the window
        self.top_right_frame = tk.Frame(root, bd=5, relief='sunken')
        self.top_right_frame.grid(row=0, column=1, sticky='nswe')

        # Create a Label widget in the top right frame for the regex instruction
        self.regex_label = tk.Label(self.top_right_frame, text="You can click on the regex to insert it in search", font=("Ariel", 14), bg = 'yellow',fg='blue')
        self.regex_label.place(relx=0.5, rely=0.1, anchor='center')  # Place it at the top corner

        # Create a Label widget in the top right frame
        self.label = tk.Label(self.top_right_frame, text="Enter The Search Expression", font=("Arial", 22))
        self.label.place(relx=0.5, rely=0.4, anchor='center')  # Place it above the Entry widget
        # Create an Entry widget in the top right frame
        self.user_input = tk.Entry(self.top_right_frame, font=("Ariel", 15))
        # Create a button that triggers the search_match function
        self.search_button = tk.Button(self.top_right_frame, text="Search", command=self.find_matches)
        self.search_button.place(relx=0.5, rely=0.6, anchor='center')

        # Place the Entry widget in the center of the frame
        self.user_input.place(relx=0.5, rely=0.5, anchor='center')

        self.bottom_right_frame = tk.Frame(root, bd=5, relief='sunken')
        self.bottom_right_frame.grid(row=1, column=1, sticky='nswe')

        # Create a frame to hold the labels vertically
        most_frequent_words_frame = tk.Frame(self.bottom_right_frame)
        most_frequent_words_frame.pack(side=tk.LEFT, anchor='sw')  # Pack the frame in the bottom left corner

        # Create labels within the frame and pack vertically
        self.most_frequent_label1 = tk.Label(most_frequent_words_frame, text="1st Frequent: Words", font=("Arial", 12))
        self.most_frequent_label1.pack(fill=tk.X)  # Expand horizontally

        self.most_frequent_label2 = tk.Label(most_frequent_words_frame, text="2nd Frequent: Word", font=("Roboto", 12))
        self.most_frequent_label2.pack(fill=tk.X)

        self.most_frequent_label3 = tk.Label(most_frequent_words_frame, text="3rd Frequent: Word", font=("Roboto", 12))
        self.most_frequent_label3.pack(fill=tk.X)



        # Create labels for total words and matched words
        self.total_words_label = tk.Label(self.bottom_right_frame, text="Total Words: 0", font=("Arial", 12))
        self.total_words_label.pack(side=tk.BOTTOM, anchor='se')  # Place it above the Edit button
        self.matched_words_label = tk.Label(self.bottom_right_frame, text="Matched Words: 0", font=("Arial", 12))
        self.matched_words_label.pack(side=tk.BOTTOM, anchor='se')  # Place it above the Edit button

        # Create an Edit button for toggling edit mode
        self.edit_button = tk.Button(self.bottom_right_frame, text="View", bg='#05d7ff',command=self.toggle_edit_mode)
        self.edit_button.pack(side=tk.BOTTOM, anchor='se')  # Place it at the bottom right

        # Create a text widget for displaying search results
        self.result_text = tk.Text(self.bottom_right_frame, wrap=tk.WORD, font=("Arial", 14))
        self.result_text.pack(fill='both', expand=True, padx=10, pady=10)

        # Open the file and read its content
        with open('output.txt', 'r') as file:
            content = file.read()


        # Insert the content into the text widget
        self.result_text.insert(tk.END, content)


        # Configure the row and column weights to ensure that the sections resize proportionally
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        color1 = '#020f12'
        color2 = '#05d7ff'
        color3 = '#65e7ff'
        color4 = 'BLACK'

        # Create forward and backward buttons
        self.forward_button = tk.Button(self.top_right_frame, text="Back", font=("Arial", 16, "bold"),
                               bg=color2,
                               fg=color4,
                               activebackground=color3,
                               activeforeground=color4,
                               highlightthickness=1,
                               highlightbackground=color2,
                               highlightcolor='WHITE',
                               width=10,
                               height=1,
                               bd=0,command=self.switch_to_file_processor)
        self.forward_button.place(relx=0.5, rely=0.9, anchor='center')
    

    def hide(self):
        # Hide the current window
        self.root.withdraw()

    def show(self):
        # Show the current window
        self.root.deiconify()

    def switch_to_file_processor(self):
        # Switch to the FileProcessorApp
        self.hide()
        file_processor_app.show()

    def toggle_edit_mode(self):
        if self.result_text.cget("state") == tk.DISABLED:
            self.result_text.config(state=tk.NORMAL)
            self.edit_button.config(text="View")  # Change button text when in edit mode
        else:
            self.result_text.config(state=tk.DISABLED)
            self.edit_button.config(text="Edit")  # Change button text when not in edit mode

    def find_matches(self):
        with open('output.txt', 'r') as file:
            content = file.read()

        regex = self.user_input.get()  # Get the regex from the user input

        # Display the updated content in the bottom right text widget
        self.result_text.delete(1.0, tk.END)  # Clear previous content
        self.result_text.insert(tk.END, content)

        matches = re.finditer(regex, content)
        all_word = re.findall(r'\b\w+\b', content)
        total_words = len(all_word)  # Count total words

        matched_words = 0
        word_frequency = Counter(all_word)  # Use Counter to calculate word frequency

        for match in matches:
            matched_words += len(re.findall(r'\b\w+\b', match.group()))  # Count matched words
            print(f"Match: {match.group()}, Index: {match.start()}")

            # Calculate the start and end indices of the matched text
            start_line = content.count('\n', 0, match.start()) + 1
            end_line = content.count('\n', 0, match.end()) + 1
            start_char = match.start() - content.rfind('\n', 0, match.start()) - 1
            end_char = match.end() - content.rfind('\n', 0, match.end()) - 1
            start = f"{start_line}.{start_char}"
            end = f"{end_line}.{end_char}"

            tag = f"match{match.start()}"  # Create a unique tag for this match
            self.result_text.tag_add(tag, start, end)  # Apply the tag to the range of text
            self.result_text.tag_config(tag, background="lightgreen", font=("Arial", 16, "bold"))

        # Update labels with the calculated values
        self.total_words_label.config(text=f"Total Words: {total_words}")
        self.matched_words_label.config(text=f"Matched Words: {matched_words}")


        most_common_words = word_frequency.most_common(3)
        self.most_frequent_label1.config(text=f"Most Frequent: {most_common_words[0][0]} - {most_common_words[0][1]}")
        self.most_frequent_label2.config(text=f"Second Most Frequent: {most_common_words[1][0]} - {most_common_words[1][1]}")
        self.most_frequent_label3.config(text=f"Third Most Frequent: {most_common_words[2][0]} - {most_common_words[2][1]}")



    def display_dictionary(self, heading, desc, dictionary):
        self.text_widget.insert(tk.END, f"{heading}\n\n", "bold")
        self.text_widget.tag_configure("bold", font=("Arial", 16, "bold"))
        self.text_widget.insert(tk.END, f"   {desc}\n")
        color1 = '#020f12'
        color2 = '#05d7ff'
        color3 = '#65e7ff'
        color4 = 'BLACK'
        for key, value in dictionary.items():
            # Create a button for the key
            button = tk.Button(self.root,
                               text=key,
                               command=lambda key=key: self.user_input.insert(tk.END, key),
                               font=("Arial", 16, "bold"),
                               bg=color2,
                               fg=color4,
                               activebackground=color3,
                               activeforeground=color4,
                               highlightthickness=1,
                               highlightbackground=color2,
                               highlightcolor='WHITE',
                               width=10,
                               height=1,
                               bd=0,
                               cursor='dot',
                               )

            self.text_widget.window_create(tk.END, window=button)
            self.text_widget.insert(tk.END, f":   {value}\n")
            self.text_widget.insert(tk.END, "\n")  # Add a newline character here



# In the __main__ block
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    file_processor_app = FileProcessorApp(root)
    regex_app = None  # Initialize regex_app as None
    root.mainloop()
