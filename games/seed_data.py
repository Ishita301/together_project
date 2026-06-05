from games.models import TruthOrDare, ThisOrThatQuestion
from features.models import DateIdea

# Truth Questions
truths = [
    ("cute", "What's your favorite memory of us so far?"),
    ("cute", "What's one small thing I do that makes you smile?"),
    ("cute", "What's your favorite photo of us together?"),
    ("cute", "What was the first thing you noticed about me?"),
    ("romantic", "When did you first realize you had feelings for me?"),
    ("romantic", "What's your favorite thing about our relationship?"),
    ("romantic", "Describe your perfect date with me in 3 words."),
    ("funny", "What's the most embarrassing thing you've done for me?"),
    ("funny", "If I were a food, what would I be and why?"),
    ("deep", "What's one thing you want us to achieve together?"),
    ("deep", "What's your biggest fear about our future?")
]

for cat, content in truths:
    TruthOrDare.objects.get_or_create(
        content=content,
        type="truth",
        defaults={"category": cat}
    )

# Dare Questions
dares = [
    ("cute", "Send me your current selfie right now!"),
    ("cute", "Write me a 3-line poem and send it in chat."),
    ("funny", "Do your best impression of me on video call."),
    ("funny", "Sing me a song right now and send a voice note."),
    ("romantic", "Tell me 5 things you love about me."),
    ("romantic", "Describe our future life together."),
    ("deep", "Write down your 3 wishes for our relationship."),
    ("deep", "Tell me your favorite memory of us in detail.")
]

for cat, content in dares:
    TruthOrDare.objects.get_or_create(
        content=content,
        type="dare",
        defaults={"category": cat}
    )

# This Or That
tots = [
    ("Beach or Mountains?", "Beach", "Mountains", "🏖️", "⛰️"),
    ("Calls or Texts?", "Calls", "Texts", "📞", "💬"),
    ("Coffee or Tea?", "Coffee", "Tea", "☕", "🍵"),
    ("Morning or Night?", "Morning", "Night", "🌅", "🌙"),
    ("Hugs or Kisses?", "Hugs", "Kisses", "🤗", "💋"),
    ("Netflix or Date Night?", "Netflix", "Date Night", "🎬", "💑"),
    ("Pizza or Pasta?", "Pizza", "Pasta", "🍕", "🍝"),
    ("Dogs or Cats?", "Dogs", "Cats", "🐶", "🐱"),
    ("Summer or Winter?", "Summer", "Winter", "☀️", "❄️"),
    ("Long drive or Long walk?", "Long drive", "Long walk", "🚗", "🚶")
]

for q, a, b, ea, eb in tots:
    ThisOrThatQuestion.objects.get_or_create(
        question=q,
        defaults={
            "option_a": a,
            "option_b": b,
            "emoji_a": ea,
            "emoji_b": eb
        }
    )

# Date Ideas
ideas = [
    ("Watch a Movie Together", "Pick the same movie and watch it on call together.", "virtual", "🎬"),
    ("Cook the Same Recipe", "Both cook the same dish and video call while eating.", "creative", "🍳"),
    ("Online Game Night", "Play online games together.", "virtual", "🎮"),
    ("Stargazing Call", "Look at the stars together on a clear night call.", "chill", "🌟"),
    ("Sunrise Watch", "Set alarms and watch the sunrise together.", "chill", "🌅"),
    ("Bake Together", "Bake cookies or a cake together.", "creative", "🍪"),
    ("Movie Marathon", "Watch an entire film series together.", "chill", "📺"),
    ("Create a Playlist", "Make a playlist for each other.", "creative", "🎵")
]

for title, desc, cat, emoji in ideas:
    DateIdea.objects.get_or_create(
        title=title,
        defaults={
            "description": desc,
            "category": cat,
            "emoji": emoji
        }
    )

print("✅ Sample data inserted")
print("Truth/Dare:", TruthOrDare.objects.count())
print("This Or That:", ThisOrThatQuestion.objects.count())
print("Date Ideas:", DateIdea.objects.count())