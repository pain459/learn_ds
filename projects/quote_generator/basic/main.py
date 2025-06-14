import random
import pyttsx3

# Quotes by mood
quotes_by_mood = {
    "stressed": [
        "Take a deep breath. This too shall pass.",
        "Sometimes doing nothing is doing something important.",
        "Peace begins with a smile."
    ],
    "happy": [
        "Happiness is a journey, not a destination.",
        "Spread love wherever you go.",
        "Enjoy the little things, for one day you’ll look back and realize they were the big things."
    ],
    "sad": [
        "Tough times never last, but tough people do.",
        "Crying is not a sign of weakness, it's a sign of being human.",
        "Even the darkest night will end and the sun will rise."
    ],
    "neutral": [
        "Every day is a fresh start.",
        "Focus on progress, not perfection.",
        "Stay patient and trust your journey."
    ]
}

# Optional: text-to-speech
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

def ask_questions():
    print("\nLet’s figure out how you're feeling today:\n")
    
    q1 = input("1. How was your day? (good/bad/okay): ").strip().lower()
    q2 = input("2. Do you feel energized or drained? (energized/drained): ").strip().lower()
    q3 = input("3. Would you rather be around people or alone? (people/alone/neutral): ").strip().lower()
    
    mood_score = 0

    # Score based on responses
    if q1 == "good":
        mood_score += 1
    elif q1 == "bad":
        mood_score -= 1
    
    if q2 == "energized":
        mood_score += 1
    elif q2 == "drained":
        mood_score -= 1
    
    if q3 == "people":
        mood_score += 1
    elif q3 == "alone":
        mood_score -= 1

    # Determine mood
    if mood_score >= 2:
        mood = "happy"
    elif mood_score <= -2:
        mood = "sad"
    elif -1 <= mood_score <= 1:
        mood = "neutral"
    else:
        mood = "stressed"

    return mood

def get_quote_by_mood(mood):
    quote = random.choice(quotes_by_mood[mood])
    print(f"\n💬 Based on your mood ({mood}), here’s your quote:\n")
    print(f"\"{quote}\"\n")
    speak(quote)

if __name__ == "__main__":
    print("🎙️ Welcome to your Mood-Based AI Quote Bot!\n")
    mood = ask_questions()
    get_quote_by_mood(mood)
    print("🌙 Sleep well and take care!\n")
