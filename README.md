# Neural Noir

**An AI-powered detective interrogation game set in the 1950s, built with Panda3D and OpenAI.**

Neural Noir puts you in the hot seat as a murder suspect being interrogated by two AI-driven detectives, the aggressive Detective Harris and the empathetic Detective Miller. Speak your answers aloud, defend yourself against mounting evidence, and try to walk away a free person.

> Senior Project for CS 425 - Christine Angela Barlaan, Evie Nivera, Matthew Osorio

## The Story

You play as a 27-year-old photographer at Reno Media Company who has been brought in for questioning. Your boss, CEO Vinh Davis, has been found dead, beaten in his own home with no signs of forced entry. A neighbor overheard an argument about a work dispute shortly before the murder. The detectives think you did it.

The interrogation unfolds across multiple phases. Evidence is introduced piece by piece, crime scene photos, witness statements, blood-stained clothing, ballistics reports, and the AI judges whether your responses are truthful, untruthful, or inconclusive. Your cumulative verdicts determine the ending: **Not Guilty**, **Guilty**, or **Inconclusive**.

## Features

- **Voice-driven gameplay**, Speak your responses using your microphone. Speech is captured and transcribed via the OpenAI Whisper API.
- **Dual AI detectives**, Two distinct detective personalities powered by GPT-4o-mini, each with their own interrogation style and emotional tone.
- **AI text-to-speech**, Detective dialogue is voiced aloud using OpenAI's TTS API with unique voices for each character (Ash for Harris, Onyx for Miller).
- **Sentiment analysis**, Each detective response is classified by emotional tone (aggressive, sympathetic, mocking, concerned, etc.) to drive animations and UI.
- **Evidence-based story graph**, 10 pieces of evidence across three interrogation phases (Early, Mid, Final), each prompting up to three rounds of questioning before an AI-generated verdict.
- **Multiple endings**, Your honesty across all evidence determines the final verdict, with critical evidence carrying extra weight.
- **3D interrogation room**, Built in Panda3D with Blender-modeled environments, character animations, and atmospheric lighting.
- **Optional biometric integration**, Supports the EmotiBit wearable sensor to read heart rate, skin temperature, and electrodermal activity (EDA). When connected, the AI detectives react to your physical nervousness.
- **Intro cinematic**, A skippable video introduction sets the noir atmosphere before gameplay begins.
- **Local database logging**, All interactions and verdicts are stored in a local SQLite database per session.
- **Difficulty settings**, Normal and hard modes with different verdict thresholds.

## Architecture

```
src/
├── main.py                      # Application entry point (Panda3D ShowBase)
├── backend/
│   ├── BackendInterface/        # GameManager, central orchestrator
│   ├── AI_System/               # AIController, AI behaviors (Strategy pattern),
│   │                              sentiment analysis, verdict generation
│   ├── StoryGraph/              # Evidence graph, scene management, verdict logic
│   ├── GameStateSystem/         # Game state enum and observer-pattern manager
│   ├── SRSystem/                # Speech-to-text via Whisper API
│   ├── TTSSystem/               # Text-to-speech and audio playback
│   ├── BiometricSystem/         # EmotiBit integration (heart rate, EDA, temperature)
│   ├── Conversation/            # Conversation model and DB persistence
│   └── Database/                # SQLite controller and session management
├── frontend/
│   ├── ui/
│   │   ├── interrogationRoom.py # Main gameplay room (3D scene, game loop)
│   │   ├── tutorialRoom.py      # Tutorial mode
│   │   ├── menu/                # Main menu, settings, audio, pause, quit
│   │   ├── overlay/             # HUD: subtitles, evidence display, push-to-talk,
│   │   │                          user speech feedback, flashbacks
│   │   ├── warnings/            # Data usage consent
│   │   └── animations.py        # Character and scene animations
│   └── stages/                  # State-specific UI logic (states 1–5)
Assets/
├── Audio/                       # Sound effects and ambient audio
├── Fonts/                       # Typography
├── Images/                      # Evidence photos, backgrounds, UI elements
├── Scenes/                      # 3D scene files
└── Video/                       # Intro cinematic
blender/                         # Blender source files and exported models
```

## Prerequisites

- **Python 3.12**
- **OpenAI API key**, Set as the `OPENAI_API_KEY` environment variable. Used for GPT-4o-mini (dialogue and verdicts), Whisper (speech-to-text), and TTS (detective voices).
- **Microphone**, Required for voice input.
- **PortAudio**, System dependency for PyAudio.
  - macOS: `brew install portaudio`
  - Ubuntu/Debian: `sudo apt-get install portaudio19-dev`
  - Windows: Typically bundled with the PyAudio wheel.
- **EmotiBit** *(optional)*, For biometric feedback during gameplay.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MatthewOsorio/Neural_Noir.git
   cd Neural_Noir
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv env
   source env/bin/activate        # macOS/Linux
   env\Scripts\activate           # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-key-here"       # macOS/Linux
   set OPENAI_API_KEY=your-key-here            # Windows CMD
   $env:OPENAI_API_KEY="your-key-here"         # Windows PowerShell
   ```

## Running the Game

From the project root:

```bash
cd src
python main.py
```

The game will open a Panda3D window. After accepting the data usage notice, you'll reach the main menu where you can start a new game, adjust settings (volume, difficulty, EmotiBit toggle), or play the tutorial.

## Game States

The interrogation progresses through five phases:

1. **Initial Phase**, Baseline questions to establish your identity (name, employer, role, relationship to the victim).
2. **Early Interrogation**, First evidence is presented: crime scene photos, witness testimonies, a bar receipt.
3. **Mid Interrogation**, Pressure mounts with blood-stained clothing, alleyway photos, and neighbor statements.
4. **Final Interrogation**, The most damning evidence: the murder weapon, the victim's notebook, your camera film, and the ballistics report.
5. **End Game**, All verdicts are tallied and the final outcome is determined.

## How Verdicts Work

After each piece of evidence, the AI evaluates your responses and assigns a verdict: **Truthful**, **Untruthful**, or **Inconclusive**. Certain pieces of evidence are flagged as "critical" and carry additional weight in the final determination.

**Normal mode**, You're found guilty if 6+ verdicts are untruthful, and not guilty if 7+ are truthful. Failing all critical evidence is an automatic guilty verdict; passing all critical evidence plus 6 others is an automatic acquittal.

**Hard mode**, The thresholds tighten: guilty at 4+ untruthful, not guilty requires 8+ truthful.

## Tech Stack

- **Panda3D 1.10**, 3D rendering, scene management, and GUI
- **OpenAI API**, GPT-4o-mini for dialogue and verdicts, Whisper for speech recognition, TTS for voice synthesis
- **Blender**, 3D modeling and animation
- **SQLite**, Local session and verdict storage
- **BrainFlow**, EmotiBit biometric sensor interface
- **Pygame**, Audio playback
- **SpeechRecognition**, Microphone input handling

## Regarding Code Integrated from Other Sources

All code was developed by the team. Any similarities to online resources stem from implementation styles as suggested by the [Panda3D Manual for Python, Version 1.10](https://docs.panda3d.org/1.10/python/index) and the [OpenAI API documentation](https://platform.openai.com/docs/overview).
