
# DebugMate AI

An AI-powered desktop application that helps programmers
understand code errors and learn how to fix them.

## Features

- Multiple programming language options
- AI-generated debugging diagnosis
- Corrected code suggestions
- Beginner-friendly or detailed explanations
- Follow-up questions
- Tkinter desktop interface

## Technologies

- Python
- Tkinter
- OpenAI Python SDK
- OpenAI Responses API

## Prompt Engineering

1. Persona Pattern: The AI acts as a patient programming tutor.
    
Where: SYSTEM_PROMPT in debugger.py
The model is assigned the role of a patient programming tutor. It is instructed to explain errors clearly, preserve the user's approach when possible, and acknowledge uncertainty.

Why it helps: The same code question can receive different responses depending on the role assigned to the AI. The tutor persona is intended to produce explanations that are more appropriate for learners than terse, expert-oriented responses.

2. Structured Output Pattern: The AI organizes its response
   into Problem, Cause, Fixed Code, Explanation, and Prevention.
    
Where: The system instructions and user_prompt in debugger.py

The model must organize its response into five named sections: Problem, Cause, Fixed Code, Explanation, and Prevention.

Why it helps: A consistent structure makes responses easier to navigate and makes it simpler for users to find the corrected code without reading the entire explanation.

## Requirements

- Python 3
- An OpenAI API key
- API access and any required billing configuration

## Setup

1. Clone the repository.
2. Create and activate a virtual environment.

   python -m venv .venv
   .venv\Scripts\Activate.ps1

3. Install dependencies:

   pip install -r requirements.txt

4. Configure OPENAI_API_KEY as an environment variable.

   setx OPENAI_API_KEY "YOUR_API_KEY_HERE"

5. Run the application:

   python main.py
