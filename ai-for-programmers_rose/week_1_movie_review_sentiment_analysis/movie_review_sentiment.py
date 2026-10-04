#!/usr/bin/env python3
'''
Implement a function that analyzes movie reviews and extracts sentiment scores.

Estimated Time: 10 minutes

Requirements
Implement the analyze_sentiment() function that takes a movie review text as input and returns a dictionary with 'thought' and 'sentiment' keys
Use the OpenAI API to perform sentiment analysis on the movie reviews
Parse the API response to extract both the analysis thought process and the final sentiment (positive/negative)
Handle the API response format correctly to ensure proper extraction of the required information
'''

from openai import OpenAI

import sys, os
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_sentiment(review):
    """
    Analyze the sentiment of a movie review using structured output.
    Returns a dictionary with 'thought' and 'sentiment' keys.
    """
    # TODO: Create a prompt that:
    # 1. Asks for sentiment analysis
    # 2. Specifies the required output format
    #       thought: [analysis]
    #       sentiment: [positive/negative]
    # 3. Includes the review text
    from textwrap import dedent
    prompt = dedent("""
    Please briefly analyze/summarize this short movie review and determine if the overall sentiment expressed in the review is positive or negative. \
    Please return your output, without additional comments, structured in two lines as follows:
    
    thought: [Your brief analysis here]
    sentiment: ["positive"/"negative"]
    
    For example:
    thought: This review noted the film's beautiful cinematography.
    sentiment: positive
    
    Here's the review: "%s"

    """ % review)
    logger.info('Analyzing review "%s"',review)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    content = response.choices[0].message.content
    logger.info("Response received: %s",content)
    
    # Parse the response to extract thought and sentiment
    # The response should be in the format:
    # thought: [analysis]
    # sentiment: [positive/negative]
    
    
    
    thought= content.strip()[9:content.index('\nsentiment:')]
    sentiment = content.rstrip()[-8:]
    logger.info('Review analyzed: %s (%s)',thought,sentiment)
    ### practice with regex instead?
    result = {
        "thought": thought,
        "sentiment": sentiment
    }
    return result

def main():
    # Test cases
    reviews = [
        "This film shouldn't work at all. It doesn't have much of a story and the whole dial up internet thing is incredibly dated. However Hanks and Ryan sell it beautifully.",
        "The movie was terrible. The acting was wooden, the plot made no sense, and I want my two hours back.",
        "An absolute masterpiece! The cinematography was stunning, the acting was superb, and the story kept me engaged from start to finish."
    ]

    # Test each review
    for i, review in enumerate(reviews, start=1):
        result = analyze_sentiment(review)
        print(f"\nReview {i}:")
        print(f"Thought: {result['thought']}")
        print(f"Sentiment: {result['sentiment']}")

if __name__ == "__main__":
    logging.basicConfig(filename="movie_review.log",level=logging.INFO)
    sys.exit(main())