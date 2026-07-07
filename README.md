🌹 Petals Around the Rose
 
A terminal-based implementation of the classic logic puzzle "Petals Around the Rose", built with Python and Rich for an enhanced interactive experience.
**About the Game
 
Petals Around the Rose is a puzzle game based on interpreting the hidden pattern created by rolling dice. 
The challenge is simple:
 - Work out the secret rule that determines the number of petals around the rose.
 
Each round: 
1. The dice are rolled.
2. The game calculates the hidden petal count.
3. You enter your guess.
4. The game provides feedback and tracks your progress.
 
The catch?
 
The rule is not revealed. The player must discover it through observation, logic, and persistence.
 
** Features: 
- Animated dice rolling experience
- Rich terminal-based interface
- Score and streak tracking
- Progressive hints to help players learn
- Feedback after incorrect guesses
- Challenge yourself to build longer streaks
- Standalone Windows executable available

**Getting Started:
 
Option 1 — Download and Play (Windows)
 
No Python installation required.
1. Download the latest "PetalsGame.exe" from the Releases section.
2. Run the executable.
3. Start solving the puzzle.
 
Option 2 — Run from Source
 
Requirements: 
- Python 3.10+
- pip
 
Clone the repository: 
Navigate into the project:
cd Petals-Around-the-Rose
 
Create and activate a virtual environment:
python -m venv .venv
 
Windows:
.venv\Scripts\activate
 
Install dependencies:
pip install -r requirements.txt
 
Run the game:
python -m petals
 
**Project Structure:
 
Potentate/
│
├── src/
│   └── petals/
│       ├── __main__.py   # Application entry point
│       ├── game.py       # Main game loop
│       ├── dice.py       # Dice rolling logic
│       ├── logic.py      # Petal calculation rules
│       └── ui.py         # Terminal interface
│
├── tests/
│   ├── test_game.py
│   └── test_logic.py
│
├── requirements.txt
├── pyproject.toml
└── README.md
 
**Testing:
The project includes automated tests using "pytest".
 
Run tests:
pytest
Built With: 
- Python
- Rich
- PyInstaller
- pytest
 
**Learning Goals: 
This project was created to explore:
 
- Python application architecture
- Package structure using the "src" layout
- Automated testing
- Terminal UI design
- Application packaging
- Creating a distributable Windows application
 
Enjoy the challenge, and remember:  The rose is always watching. 🌹