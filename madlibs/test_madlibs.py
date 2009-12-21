import unittest
import re

def extract(story):
    match = re.findall('\(\(.*?\)\)', story)
    return map(lambda x: x[2:-2], match)

def replace(placeholders, story):
    for token in placeholders.keys():
        story = re.sub('\(\(' + token + '\)\)', placeholders[token], story)

    return story

class TestMadLibs(unittest.TestCase):
    def setUp(self):
        self.story = "I had a ((an adjective)) sandwich for lunch today. It dripped all over my ((a body part)) and ((a noun))."
        
    def test_extract_placeholders(self):
        expected_placeholders = ['an adjective', 'a body part', 'a noun']
        self.assertEquals(expected_placeholders, extract(self.story))
        
    def test_replace_placeholders(self):
        placeholders = {'an adjective': 'smelly', 'a body part': 'toes', 'a noun': 'bathtub'}
        expected_story = "I had a smelly sandwich for lunch today. It dripped all over my toes and bathtub."
        self.assertEquals(expected_story, replace(placeholders, self.story))
