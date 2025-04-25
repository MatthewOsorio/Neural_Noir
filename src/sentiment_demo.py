from backend.AI_System.SentimentAnalysis import SentimentAnalysis

def test_sentiment_output():
    sentiment_analyzer = SentimentAnalysis()

    # Simulate a Phase 2 GPT output
    fake_gpt_responses = [
        {"Speaker": "Harris", "Text": "You expect us to believe that? Come on, Mark."},
        {"Speaker": "Miller", "Text": "Help us understand your side of the story, we just want the truth."}
    ]

    result = sentiment_analyzer.classifyEachDetective(fake_gpt_responses)
    print("Sentiment classification result:")
    for speaker, sentiment in result.items():
        print(f"{speaker}: {sentiment}")

if __name__ == "__main__":
    test_sentiment_output()
