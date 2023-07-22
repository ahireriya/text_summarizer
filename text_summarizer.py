import tkinter as tk
from tkinter import ttk, messagebox
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer


def summarize():
    # Get input text and number of sentences from the user
    text = text_entry.get("1.0", "end-1c")
    num_sentences = int(num_sentences_entry.get())
    
    # Tokenize the text into individual sentences
    sentences = sent_tokenize(text)
    
    # Tokenize each sentence into individual words and filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [word_tokenize(sentence.lower()) for sentence in sentences]
    words = [[word for word in sentence if word not in stop_words] for sentence in words]
    
    # Stem each word
    stemmer = PorterStemmer()
    words = [[stemmer.stem(word) for word in sentence] for sentence in words]
    
    # Calculate word frequency distribution
    all_words = [word for sentence in words for word in sentence]
    freq_dist = FreqDist(all_words)
    
    # Calculate sentence scores based on word frequency
    scores = []
    for i, sentence in enumerate(words):
        score = 0
        for word in sentence:
            score += freq_dist[word]
        scores.append((score / len(sentence), i))
    
    # Sort the sentences by score and take the top N sentences
    scores.sort(reverse=True)
    top_sentences = [sentences[i] for _, i in scores[:num_sentences]]
    
    # Join the top sentences together and display the summary
    summary = ' '.join(top_sentences)
    messagebox.showinfo("Summary", summary)


# Create the main window
root = tk.Tk()
root.title("Text Summarizer")
root.geometry("800x500")
root.configure(background="#FFC0CB")

# Add the input text box
text_label = ttk.Label(root, text="Enter the Text to Summarize:", foreground="#990000", font=("Helvetica", 16, "bold"))
text_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
text_entry = tk.Text(root, height=15, width=70, bg="#FFE5E5", fg="#000000", font=("Helvetica", 14))
text_entry.grid(row=1, column=0, padx=20, pady=20)

# Add the number of sentences input box
num_sentences_label = ttk.Label(root, text="Enter the Number of Sentences for the Summary:", foreground="#990000", font=("Helvetica", 16, "bold"))
num_sentences_label.grid(row=2, column=0, padx=20, pady=20, sticky="w")
num_sentences_entry = ttk.Entry(root, width=10, font=("Helvetica", 14))
num_sentences_entry.grid(row=3, column=0, padx=20, pady=20)

# Add the summarize button
summarize_button = ttk.Button(root, text="Summarize", command=summarize, width=30, style="Accent.TButton")
summarize_button.grid(row=4, column=0, padx=40, pady=40)

# Configure the window layout
root.columnconfigure(0, weight=1)

# Start the event loop
root.mainloop()
