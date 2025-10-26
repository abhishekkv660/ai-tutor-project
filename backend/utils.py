# utils.py
def detect_emotion(text: str) -> str:
    """
    Detect emotion from AI response text based on keywords
    
    Args:
        text: The response text to analyze
        
    Returns:
        Emotion state: happy, thinking, explaining, confused, or neutral
    """
    text_lower = text.lower()
    
    # Define emotion keywords
    happy_keywords = [
        "correct", "great", "excellent", "yes", "wonderful", 
        "perfect", "awesome", "congratulations", "well done",
        "fantastic", "brilliant", "amazing", "good job"
    ]
    
    thinking_keywords = [
        "let me", "think", "consider", "analyze", "hmm",
        "interesting", "let's see", "pondering", "evaluating",
        "contemplating"
    ]
    
    explaining_keywords = [
        "explain", "because", "therefore", "means", "definition",
        "concept", "understand", "basically", "essentially",
        "in other words", "for example", "specifically", "namely"
    ]
    
    confused_keywords = [
        "sorry", "cannot", "don't know", "unclear", "unsure",
        "confused", "not sure", "uncertain", "ambiguous", 
        "difficult to say"
    ]
    
    # Check emotions in priority order
    if any(word in text_lower for word in happy_keywords):
        return "happy"
    elif any(word in text_lower for word in explaining_keywords):
        return "explaining"
    elif any(word in text_lower for word in thinking_keywords):
        return "thinking"
    elif any(word in text_lower for word in confused_keywords):
        return "confused"
    else:
        return "neutral"
