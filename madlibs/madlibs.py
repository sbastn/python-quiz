import re

class MadLibs(object):
    def __init__(self, story):
        self.story = story
        self.questions = self.extract(story)
        
    def tell_story(self, answers):
        return self.replace(answers, self.story)

    def extract(self, story):
        """ extract placeholders from a story"""

        variables = self.find_reusable_variables(story)
        placeholders = self.find_placeholders(story)
        return self.remove_variables_from_placeholders(placeholders, variables)

    def find_reusable_variables(self, story):
        """ returns a collection of reusable variables in a story
        from ((animal: an animal)) it returns ['animal']
        """

        vars = re.findall('\(\(.*:.*?\)\)', story)
        return map(lambda x: x.split(':')[0][2:], vars)

    def find_placeholders(self, story):
        """ returns a collections of placeholders.
        from 'Hello ((an animal)), you are ((a color))'
        it returns ['((an animal))', '((a color))']
        """

        return re.findall('\(\(.*?\)\)', story)

    def remove_variables_from_placeholders(self, match, variables):
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

    def replace(self, answers, story):
        """ replaces the placeholders inside the story """

        placeholders = self.find_placeholders(story)

        story = self.replace_simple_placeholders(story, answers, placeholders)
        story = self.replace_variable_placeholders(story, answers, placeholders)
                
        return story

    def replace_simple_placeholders(self, story, answers, placeholders):
        """ replace ((a placeholders)) inside the story """

        for answer in answers.keys():
            for token in placeholders:
                if token[2:-2] == answer:
                    story = re.sub('\(\(' + answer + '\)\)', answers[answer], story)

        return story

    def replace_variable_placeholders(self, story, answers, placeholders):
        """ replace ((var: a variable)) inside the story """

        token_with_vars = filter(lambda x: x if len(x.split(':')) > 1 else None, placeholders)

        for var_token in token_with_vars:
            var = re.split(':', var_token)[0][2:]
            placeholder = re.split(':', var_token)[1][:-2]
            story = re.sub('\(\(' + var + '\)\)', answers[placeholder], story)
            story = re.sub('\(\(' + var_token + '\)\)', answers[placeholder], story)

        return story

if __name__ == '__main__':
    story = raw_input('Enter a story: ')
    m = MadLibs(story)

    if len(m.questions) == 0:
        print 'next time, try to enter placeholders like ((this example))'

    answers = {}
    for q in m.questions:
        answers[q] = raw_input('Enter %s: ' % q)

    print m.tell_story(answers)
