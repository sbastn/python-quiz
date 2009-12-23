""" madlibs translation """
import re

class MadLibs(object):
    """ given text with ((templates)), we translate it """

    def __init__(self, story):
        self.story = story
        self.questions = self.extract(self.story)
        
    def tell_story(self, answers):
        """ tells the story back with when all the placeholders are answered """
        return self.replace(answers, self.story)

    def extract(self, story):
        """ extract placeholders from a story"""

        variables = self.find_reusable_variables(story)
        placeholders = self.find_placeholders(story)
        return self.filter_variables(placeholders, variables)

    @staticmethod
    def find_reusable_variables(story):
        """ returns a collection of reusable variables in a story
        from ((animal: an animal)) it returns ['animal']
        """

        return map(lambda x: x.split(':')[0][2:], \
                       re.findall('\(\(.*:.*?\)\)', story))

    @staticmethod
    def find_placeholders(story):
        """ returns a collections of placeholders.
        from 'Hello ((an animal)), you are ((a color))'
        it returns ['((an animal))', '((a color))']
        """

        return re.findall('\(\(.*?\)\)', story)

    @staticmethod
    def filter_variables(match, variables):
        """ filters out the reusable variables from the placeholders 
        from ['((animal: an animal))', '((animal))', '((a color))']
        it returns ['an animal', 'a color']
        """

        match = map(lambda x: x[2:-2], match)

        [match.remove(m) if m == v else None for v in variables for m in match]
        
        return  map(lambda x: x.split(':')[1] \
                        if len(x.split(':')) > 1 else x, match)

    def replace(self, answers, story):
        """ replaces the placeholders inside the story """

        placeholders = self.find_placeholders(story)

        story = self.replace_simple_placeholders(story, answers, placeholders)
        story = self.replace_variable_placeholders(story, answers, placeholders)
                
        return story

    @staticmethod
    def replace_simple_placeholders(story, answers, placeholders):
        """ replace ((a placeholders)) inside the story """

        for answer in answers.keys():
            for token in placeholders:
                if token[2:-2] == answer:
                    story = re.sub('\(\(' + answer + '\)\)', \
                                       answers[answer], story)

        return story

    @staticmethod
    def replace_variable_placeholders(story, answers, placeholders):
        """ replace ((var: a variable)) inside the story """

        token_with_vars = filter(lambda x: x \
                                     if len(x.split(':')) > 1 else None,\
                                     placeholders)

        for var_token in token_with_vars:
            var = re.split(':', var_token)[0][2:]
            placeholder = re.split(':', var_token)[1][:-2]
            story = re.sub('\(\(' + var + '\)\)', answers[placeholder], story)
            story = re.sub('\(\(' + var_token + '\)\)', \
                               answers[placeholder], story)

        return story

if __name__ == '__main__':
    the_story = raw_input('Enter a story: ')
    madlibs = MadLibs(the_story)

    if len(madlibs.questions) == 0:
        print 'next time, try to enter placeholders like ((this example))'

    the_answers = {}
    for q in madlibs.questions:
        the_answers[q] = raw_input('Enter %s: ' % q)

    print madlibs.tell_story(the_answers)
