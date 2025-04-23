from openai import OpenAI
from textwrap import dedent
from ast import literal_eval

class SentimentAnalysis:
    def __init__(self):
        self._gpt = OpenAI()
        self._allowedTones = {
            "Harris": ["aggressive", "accusatory", "mocking", "skeptical", "incredulous", "dismissive", "neutral"],
            "Miller": ["sympathetic", "concerned", "serious", "neutral", "reassuring", "disappointed", "accusatory"]
        } 

    def classifySentiment(self, detectiveResponses, allowedTones):
        latestResponse = " ".join(r["Text"] for r in detectiveResponses if "Text" in r)
        toneList = ", ".join(f'"{tone}"' for tone in allowedTones)

        # Need to create a better sentiment list
        gptInput = dedent(f"""[INSTRUCTION] You are conducting sentiment analysis for the response you will make to the player's answer to the evidence.
                                            You will classify the detective's tone in the following response:

        [RESPONSE] {latestResponse}

        Return a JSON object with a single field:
        - "sentiment": One of the following - {toneList}
        
        **RULES**
        - DO NOT roleplay or speak as a character.
         - Just respond with a valid JSON object like: {{ "sentiment": "neutral" }}
        - Do NOT add extra commentary or explanation.
        """)

        gptResponse = self._gpt.chat.completions.create(
            model='gpt-4o-mini',
            messages= [{"role": "user", "content": gptInput}]
        )

        responseText = gptResponse.choices[0].message.content
        return literal_eval(responseText)["sentiment"]
    
    def classifyEachDetective(self, responseList):
        results = {}
        for line in responseList:
            speaker = line.get("Speaker")
            text = line.get("Text")
            if speaker and text:
                allowedTones = self._allowedTones.get(speaker, ["neutral"])
                results[speaker] = self.classifySentiment([{"Text": text}], allowedTones)
        return results
