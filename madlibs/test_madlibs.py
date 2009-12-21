import unittest
import re

def extract(story):
    """ extract placeholders from a story"""
    return find_placeholders(story, find_reusable_variables(story))

def find_reusable_variables(story):
    """ returns a collection of reusable variables in a story
    from ((animal: an animal)) it returns ['animal']
    """
    vars = re.findall('\(\(.*:.*?\)\)', story)
    return map(lambda x: x.split(':')[0][2:], vars)

def find_placeholders(story, variables):
    """ returns a collections of placeholders.
    from 'Hello ((an animal)), you are ((a color))'
    it returns ['((an animal))', '((a color))']
    """
    match = re.findall('\(\(.*?\)\)', story)
    return remove_variables_from_placeholders(match, variables)

def remove_variables_from_placeholders(match, variables):
    """ filters out the reusable variables from the placeholders 
    from ['((animal: an animal))', '((animal))', '((a color))']
    it returns ['an animal', 'a color']
    """
    match = map(lambda x: x[2:-2], match)
    for m in match:
        for v in variables:
            if m == v:
                match.remove(m)

    return  map(lambda x: x.split(':')[1] if len(x.split(':')) > 1 else x, match)

def replace(placeholders, story):
    for token in placeholders.keys():
        story = re.sub('\(\(' + token + '\)\)', placeholders[token], story)

    return story

class TestMadLibs(unittest.TestCase):
    def setUp(self):
        self.story = "I had a ((an adjective)) sandwich for lunch today. It dripped all over my ((a body part)) and ((a noun))."
        
    def test_extract_questions_from_story(self):
        self.assertEquals(['an adjective', 'a body part', 'a noun'], extract(self.story))
        
    def test_feed_answers_to_story(self):
        placeholders = {'an adjective': 'smelly', 'a body part': 'toes', 'a noun': 'bathtub'}
        expected_story = "I had a smelly sandwich for lunch today. It dripped all over my toes and bathtub."
        self.assertEquals(expected_story, replace(placeholders, self.story))

    def test_extract_reusable_variables_from_story(self):
        story = "Our favorite language is ((animal:an animal)). We think ((animal)) is better than ((an animal))."
        self.assertEquals(['an animal', 'an animal'], extract(story))
        

