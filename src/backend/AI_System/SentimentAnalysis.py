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

        toneDescriptions = {
            "aggressive": "Direct, forceful, confrontational",
            "accusatory": "Blaming, pressing guilt",
            "mocking": "Sarcastic, teasing, belittling",
            "skeptical": "Doubtful, questioning truthfulness",
            "incredulous": "Unbelieving, shocked or stunned",
            "dismissive": "Minimizing, brushing off",
            "neutral": "Flat, emotionless, factual",
            "sympathetic": "Caring, understanding",
            "concerned": "Worried, emotionally attentive",
            "serious": "Focused, professional, intense",
            "reassuring": "Comforting, calming",
            "disappointed": "Let down, subtly hurt"
        }

        toneList = "\n".join(f'- "{tone}": {toneDescriptions[tone]}' for tone in allowedTones if tone in toneDescriptions)

        gptInput = dedent(f"""[INSTRUCTION] You are conducting sentiment analysis on a detective's dialogue in a crime investigation scene.

        [RESPONSE] {latestResponse}

        You must classify the **emotional tone** or **interrogation style** used by the detective. Choose only one of the following tones, based on this specific character's behavior: {toneList}

        **CONTEXT**
        - Harris is aggressive, cynical, skeptical, or mocking. His lines may sound accusatory, dismissive, or sarcastic.
        - Miller is calm, empathetic, and supportive. He may sound concerned, disappointed, or serious.

        **RULES**
        - Your response MUST be a JSON object like: {{ "sentiment": "mocking" }}
        - If the line uses sarcasm, suspicion, disbelief, or blunt confrontation — DO NOT mark it as "neutral".
        - Use "neutral" ONLY if the line is purely factual and emotionally flat.
        - Never include explanation — just return the JSON.

        Output:
        """)

        gptResponse = self._gpt.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{"role": "user", "content": gptInput}]
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
                sentiment = self.classifySentiment([{"Text": text}], allowedTones)
                results[speaker] = sentiment if sentiment else "neutral"

                if isinstance(sentiment, list):
                    results[speaker] = sentiment[0] if sentiment else "neutral"
                else:
                    results[speaker] = sentiment if sentiment else "neutral"

        return results