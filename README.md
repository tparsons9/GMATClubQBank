---

# Question Bank App

This application provides an interface for users to interact with a question bank. Users can attempt questions, bookmark them, review past attempts, and more. The app is built using the `tkinter` library in Python, making it a GUI-based application.

## Features

1. **Question Viewer**: Shows questions to the user. Users can navigate through questions using the "Next" button.
2. **Timer**: Users can start a timer when attempting a question. The timer can be paused and resumed.
3. **Answer Input**: Users can input their answer and check if it's correct.
4. **Bookmarking**: Users can bookmark questions for later review.
5. **Reviewing Past Attempts**: After answering a question, users can review their past attempts and notes for that question.
6. **URL Navigation**: Users can click a button to be taken to a web page related to the question.
7. **Calculator**: Users have the option to open a calculator utility to help them solve the question.



## Setup

1. Ensure you have Python installed on your machine.
2. Install the required libraries using pip:
```
pip install pillow numpy
```
3. Place all your questions in a JSON file named `question_dict.json`. The format should match the structure expected by the app (with fields for attempts, bookmarks, etc.).
4. Place all question images in a folder named `screenshots`. The naming convention for images should be `question_<id>.png`. Note: This is only for `app_with_screenshots.py`. 
5. The icons for the calculator, bookmark, and URL buttons should be placed in the root directory and named `calculator.png`, `bookmark.png`, `bookmark2.png`, and `url.png` respectively.

## Usage

1. Run the script:
```
python app.py
```
2. Click on the "Open Question Bank" button.
3. Attempt questions, use the calculator, bookmark questions, and navigate to URLs as needed.
4. After attempting a question, you can review past attempts and save notes.
5. To exit the app, click on the "Quit" button.

## Additional Notes

- The timer starts automatically when you navigate to a question's URL.
- The calculator can be toggled on or off. Please note that this is for a Mac-based calculator app, you will need to modify accordingly for your system. 
- The app saves the updated question data (including bookmarks, notes, etc.) to `question_dict.json` upon exit.
- You can create visualizations to understand which categories of questions you are having the most trouble with, or review notes in a json reader. 

---
