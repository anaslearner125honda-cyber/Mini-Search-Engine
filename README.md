# Mini Search Engine
A lightweight text search engine built from scratch using Python, utilizing a Trie for word indexing and a Max-Heap for frequency ranking.


## Key Features
- **File Frequency Ranking**: Search for any specific word to find the top 5 files where it appears the most, along with its exact repetition count in each file.
- **Prefix Search & Autocomplete**: Enter a prefix to retrieve the top 5 most frequent matching words across the entire dataset[cite: 1].
- **Interactive CLI Menu**: Simple and clean command-line interface for smooth user interaction.
- **Built From Scratch**: Implemented core data structures (Trie and Heap) manually without relying on external search libraries[cite: 1].


## Architecture & Data Structures Used
The project is structured into modular components, leveraging custom-built data structures for efficiency:
- **Trie (Prefix Tree)**: Used for rapid word indexing and prefix matching. Each node maintains a dictionary (`information`) mapping filenames to their exact word repetition counts.
- **Heap (`heapq`)**: Implemented for top-$K$ frequency ranking. It efficiently extracts the top 5 files or top 5 autocomplete words without sorting the entire dataset, maintaining an optimal $O(N \log K)$ complexity.
- **Data Flow**: Text files are parsed character-by-character to extract words -> inserted into the Trie -> queried using Min/Max heaps to retrieve ranked results.


## How to Run / Installation
1. **Download or Clone**: Download the entire repository folder to ensure the `datafiles` directory stays connected with the script.
2. **Prerequisites**: Make sure **Python 3** is installed on your system.
3. **Run the Program**: Open your terminal or command prompt in the project directory and execute:
   ```bash
   python search_engine.py


## Adding Custom Data & Formatting Rules

You can expand the search dataset by placing additional `.txt` files inside the `datafiles` folder[cite: 1]. To ensure accurate word indexing, please follow this formatting rule:
- **Word Boundary Parsing**: The engine treats any character outside of letters (`a-z`) and numbers (`0-9`) as a word separator. 
- **Punctuation Note**: Avoid using apostrophes or special symbols inside words (e.g., words like "don't" will be split into "don" and "t"). Use standard spaces, commas, and full stops to separate words properly.


## Lessons Learned
- First, I thoroughly studied and implemented Heaps and Tries independently from scratch.
- Then, I combined both data structures together to build this functional Search Engine project.