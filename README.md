
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
    ## WHERE: SYSTEM_PROMPT in debugger.py  
2. Structured Output Pattern: The AI organizes its response
   into Problem, Cause, Fixed Code, Explanation, and Prevention.
    ## WHERE: user_prompt in debugger.py

## Requirements

- Python 3
- An OpenAI API key
- API access and any required billing configuration

## Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

   pip install -r requirements.txt

4. Configure OPENAI_API_KEY as an environment variable.
5. Run the application:

   python main.py

## Limitations

The application analyzes code but does not execute it.
AI-generated fixes may be incorrect and should be reviewed.

## Future Improvements

- Syntax-highlighted code editor
- Copy corrected code button
- Save and load debugging sessions
- Automated tests for suggested fixes
- More prompt patterns and response evaluation
