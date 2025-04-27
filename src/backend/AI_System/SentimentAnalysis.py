import json
import re
from openai import OpenAI
from textwrap import dedent
import threading

# class written by Christine 
class SentimentAnalysis:
    def __init__(self):
        self._gpt = OpenAI()
        self._allowedTones = {
            "Harris": ["aggressive", "accusatory", "mocking", "skeptical", "incredulous", "dismissive"],
            "Miller": ["sympathetic", "concerned", "serious", "reassuring", "disappointed", "accusatory"]
        }

    def classifySentiment(self, response, allowedTones):
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

        [RESPONSE] {response}

        You must classify the **emotional tone** or **interrogation style** used by the detective. Choose only one of the following tones, based on this specific character's behavior:
        {toneList}

        **CONTEXT**
        - Harris is aggressive, cynical, skeptical, or mocking. His lines may sound accusatory, dismissive, or sarcastic.
        - Miller is calm, empathetic, and supportive. He may sound concerned, disappointed, or serious.

        **RULES**
        - Your response MUST be a JSON object like: {{ "sentiment": "mocking" }}
        - You can only use the 'aggressive' tag for Harris when it is absolutely appropriate.
        - Do NOT return Markdown or explanation.
        """)

        response = self._gpt.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{"role": "user", "content": gptInput}]
        ).choices[0].message.content.strip()

        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", response, flags=re.IGNORECASE | re.MULTILINE)
        
        try:
            return json.loads(cleaned)["sentiment"]
        except Exception as e:
            print(f"Sentiment parsing failed:\nRaw: {response}\nCleaned: {cleaned}\nError: {e}")
            match = re.search(r'"sentiment"\s*:\s*"(\w+)"', cleaned)
            if match:
                return match.group(1).strip()
            return "neutral"

    def classifyEachDetective(self, responseList):
        threads = []

        for index, response in enumerate(responseList):
            thread = threading.Thread(target=self.classifyWorker, args= (index, response["Speaker"], response["Text"], responseList))
            thread.start()
            threads.append(thread)
        
        for thread in threads: 
            thread.join()
    
    def classifyWorker(self, index, speaker, text, responseList):
        allowedTones = self._allowedTones.get(speaker, ["neutral"])
        sentiment = self.classifySentiment(text, allowedTones)

        if not isinstance(sentiment, str):
            sentiment = "neutral"

        responseList[index]["Sentiment"] = sentiment

    def getSentiment(self):
        return {
            "Harris": self._harrisSentiment,
            "Miller": self._millerSentiment
        }