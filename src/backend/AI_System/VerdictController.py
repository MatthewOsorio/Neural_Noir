from openai import OpenAI
from textwrap import dedent
from ast import literal_eval

class VerdictController:
    def __init__(self):
        self._gpt = OpenAI()
        self.currentVerdict = None
        self.callbackF = None

    def deriveVerdict(self, interrogation, evidenceConvo, evidence):
        cleanEvidenceConvo = '\n'.join(line.strip() for line in evidenceConvo)

        gptInput = dedent(f"""[INSTRUCTION] You are evaluating whether the suspect, Mark Coleman, was honest about the following piece of evidence:

        [EVIDENCE] {evidence}

        You may use the full conversation history to spot contradictions or inconsistencies.

        Below is the portion of the conversation directly related to this evidence:

        {cleanEvidenceConvo}

        Return a JSON object with two fields:
        - "verdict": Must be one of the following strings: "truthful", "untruthful", or "inconclusive"
        - "reasoning": A concise explanation (1-3 sentences) justifying the verdict

        **RULES**
        - Please explain your reasoning.
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
        responseDict = literal_eval(cleanResponse)

        return responseDict["verdict"]