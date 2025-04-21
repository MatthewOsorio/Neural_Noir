from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from openai import OpenAI
from backend.TTSSystem import TextToSpeechController

if TYPE_CHECKING:
    from AI_Context import AIContext


"""
Notes from Matt
    Here are updates I've made the the AI System and TTS to accomdate for the second detective:
        - I added an ai history component to separate what we stor in the database and the context list we feed into gpt.
        - I adjusted the system prompt to be more gpt friendly and added the [INSTRUCTION] and [MARK] steps into the system prompt
        - I have moved all the prompts to gpt from the 'asssistant' message to 'user' message because the user message has more 
            control over what gpt has to say and because 'assistant' is orignally only for gpt to keep track of what it has 
            has said previously. But since we are using the 'user' message we need to differentiate the instructions we give gpt
            and what the user says. Hence we are now supposed to prefix all user messages with [INSTRUCTION] and [MARK]. See
            the AI Inital phase for reference
        - I have refactored how we handle the generate response message so now we return both the responses and the file path 
            for both of thier speech files, this is the output now:
                [{'Speaker': 'Harris', 'Text': 'blah blah blah', 'AudioFilePath': WindowsPath('filepath')},
                {'Speaker': 'Harris', 'Text': 'blah blah blah', 'AudioFilePath': WindowsPath('filepath')}]
        - I have separated the TTS and the AudioController
        - In the TTS I implemented multithreading to speed up the audio file generation
        - I combinted all the previous AI Interrogation States into a singular Interrogation state that request evidence based on the game state from story graph

    Next Steps:
        - Modify frontend to accomodate these changes
        - Update the conversation model because I have separated the AI System from the conversation model and to account for the second detective
"""

class AI(ABC):
    def __init__(self, history):
        self.gpt = OpenAI()
        self._aiHistory= history
        self.userNervous = None
        self._tts = TextToSpeechController()

    @property
    def behavior(self) -> AIContext:
        return self._behavior
    
    @behavior.setter
    def behavior(self, behavior: AIContext) -> None:
        self._behavior = behavior

    def updateNervous(self, nervousState):
        self.userNervous = nervousState
        
    @abstractmethod
    def generateResponse(self) -> str:
        pass
    
    @abstractmethod
    def processResponse(self, userResponse):
        pass
    
    def getNervous(self):
        return self.userNervous
    
    # Creates the dictionary we return from generateResponse
    def formatResponse(self, response):
        lines = [line.strip() for line in response.split("\n") if line.strip()]
        responses = []

        for line in lines:

            if line.startswith("Detective Harris:"):
                speaker = "Harris"
                text = line[len("Detective Harris:"):].strip()
            elif line.startswith("Detective Miller:"):
                speaker = "Miller"
                text = line[len("Detective Miller:"):].strip()
            else:
                raise Exception("UNKNOWN RESPONSE FROM GPT")

            responses.append({"Speaker": speaker, "Text": text})

        return responses

    def sendToGPT(self, prompt):
        gptResponse = self.gpt.chat.completions.create(
            model= 'gpt-4o-mini',
            messages= prompt
        )

        cleanResponse = gptResponse.choices[0].message.content

        # Strictly for initial phase
        if cleanResponse == 'Correct':
            return cleanResponse

        detectiveResponses = self.formatResponse(cleanResponse)
        self.makeSpeechFile(detectiveResponses)
        self.addAIResponses(detectiveResponses) # Adds AI response to the aiHistory or the context list
        return detectiveResponses
    
    def addAIResponses(self, responseList):
        self._aiHistory.addAIResponse(self.parseDetectiveResponses(responseList))
    
    # uses the TTS to create an audio file and adds the audio file directly to the dictionary
    def makeSpeechFile(self, detectiveResponses):
        self._tts.generateTTS(detectiveResponses)

    def parseDetectiveResponses(self, responseList):
        return '\n'.join(f"Detective {r['Speaker']}: {r['Text']}" for r in responseList)