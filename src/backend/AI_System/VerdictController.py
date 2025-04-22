from openai import OpenAI
from textwrap import dedent
import re

class VerdictController:
    def __init__(self):
        self._gpt= OpenAI()
        self.currentVerdict = None
        self.callbackF = None

    def deriveVerdict(self, interrogation, evidenceConvo, evidence):
        cleanEvidenceConvo = '\n'.join(line.strip() for line in evidenceConvo)

        gptInput = dedent(f"""[INSTRUCTION] You are evaluating whether the suspect, Mark Coleman, was honest about the following piece of evidence:

        [EVIDENCE] {evidence}

        You may use the full conversation history to spot contradictions or inconsistencies.

        Below is the portion of the conversation directly related to this evidence:

        {cleanEvidenceConvo}

        Return only ONE of the following verdicts:

        [[verdict: truthful]]  
        [[verdict: untruthful]]  
        [[verdict: inconclusive]]  

        **RULES**
        - Please expain your reasoning.
        - DO NOT roleplay or speak as a character.
        - DO NOT include anything except the verdict tag.
        - Only judge the suspect's honesty about the listed evidence.
        """)
        
        interrogation.append({'role': 'user', 'content': gptInput})

        gptResponse = self._gpt.chat.completions.create(
            model='gpt-4o-mini',
            messages= interrogation
        )

        cleanResponse = gptResponse.choices[0].message.content
        print(f"Verdict controller clean Response: {cleanResponse}")
        match = re.search(r'\[\[verdict:\s*(truthful|untruthful|inconclusive)\s*\]\]', cleanResponse.lower())
        if match:
            self.currentVerdict = match.group(1)
        else:
            self.currentVerdict = "inconclusive"
        print(cleanResponse)
    
    def verdictCallback(self, callback):
        self.callbackF = None
        self.callbackF = callback