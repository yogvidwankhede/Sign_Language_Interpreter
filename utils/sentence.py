import spacy
import random
import pyttsx3
# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Keywords

# Sample sentences

# Generate a meaningful sentence containing the keywords


def generate_sentence(keywords):  # sourcery skip: hoist-similar-statement-from-if, hoist-statement-from-if
    engine = pyttsx3.init()
    matching_sentences = []
    sentences = [
    "How are You?",
    "I am Good",
    "Please, Help! ",
    "Where is Washroom ?",
    "What Time is it?",
    "I am Sorry",
    "Have You Understood?",
    "Yes, I Understood"
    ]

    # Iterate through the sentences to find those containing the keywords
    if len(keywords) > 1:
        for sentence in sentences:
            doc = nlp(sentence)
            contains_keywords = all(
                keyword in [token.text for token in doc] for keyword in keywords)
            if contains_keywords:
                matching_sentences.append(sentence)

        # Randomly select a sentence from the matching ones
        if matching_sentences:
            generated_sentence = random.choice(matching_sentences)
            mytext = generated_sentence
            print(mytext)
        else:
            mytext = ' '.join(keywords)
            print(mytext)
        
        engine.say(mytext)
        engine.setProperty("rate", 120)
        engine.runAndWait()
    else:
        mytext = keywords[0]
        engine.say(mytext)
        engine.setProperty("rate", 120)
        engine.runAndWait()
        print(mytext)
        

    # Generate and print a meaningful sentence