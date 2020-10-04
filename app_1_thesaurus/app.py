# import modules
import sys
import json 
from difflib import get_close_matches
import mysql.connector

#check if local encyclopedia was passed via command line
if len(sys.argv) > 1:
    #get thesaurus-json file from command line arguments
    file = sys.argv[1]

    # Opening JSON file 
    with open(file) as json_file: 
        # convert json to python dict
        data = json.load(json_file) 
else:
    print('Querying data from remote database!\n')
    # quit()

#create thesaurus-class
class LocalThesaurus():

    # initiate instance
    def __init__(self, data):
        self.data = data

    #returns a description for a word, based on values saved for a key in data
    def description(self, word):
        # if word exists in self.data keys, return word and list of descriptions
        try:
            desc = self.data[word]
            return word, desc

        # if word does not exist in self.data keys and a keyError is thrown
        except KeyError:

            # check and correct for mispelling and return correctly spelled word and description
            spell_check_output = self.catch_misspelling(word, self.data.keys())

            if spell_check_output:
                return spell_check_output, self.data[spell_check_output]

            # if word does not exist, return error message 
            return 'Error', 'Your word does not exist! Be serious!'

    #returns misspelling-correctiond using a prompt for verification
    def catch_misspelling(self, word, word_list):

        #check for title-capitalized spelling (e.g for country names)
        if word.title() in self.data.keys():
            return word.title()

        # check for uppercase spelling (e.g. for abbreviations)
        elif word.upper() in self.data.keys():
            return word.upper()
        
        # check for misspellings
        else:
            # get up to 3 most closely related spellings
            correct_spelling = get_close_matches(word, word_list, cutoff=0.75)

            # check if related spellings could be detected
            if correct_spelling:

                # iterate over list of detected related spelling 
             for spelling in correct_spelling:

                    # prompt for confirmation of spelling
                    test = input(f'Did you mean {spelling}? (y/n): ').lower()

                    # if confirmed, return that word
                    if test == 'y' or test == 'yes' or test == 'yep':
                        return spelling
                        break

                    # otherwise continue loop
                    elif test == 'n' or test == 'no' or test == 'nope':
                        continue

                    else:
                        print('That is not a valid option!')
                        quit()

        # if no spelling option could be confirmed, return None
        return None
    
    #pretty prints the returned descirptions
    def pretty_print(self, word):
        #save (corrected) word and description list in descriptions
        descriptions = self.description(word)

        #check for error messages:
        if descriptions[0] == 'Error':
            print(f'\n{descriptions[1]}')

        # otherwise print correct word 
        else:
            print(f'\n"{descriptions[0]}" has {len(descriptions[1])} description(s): \n')

            # print descriptions for that word
            for description in descriptions[1]:
                print(f'\u2022 {description}')

class RemoteThesaurus():
    def __init__(self, user = "ardit700_student", password = "ardit700_student", host = "108.167.140.122", database = "ardit700_pm1database"):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.con = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database
        )

    def connect(self, user, password, host, database):

        cursor = self.con.cursor()
        return cursor

    def get_results(self, word):
        cursor = self.connect(self.user, self.password, self.host, self.database)
        query = cursor.execute(f"SELECT Definition FROM Dictionary WHERE Expression = '{word}'")
        results = cursor.fetchall()

        if results:
            return word, results
        else:
            return 'Key_Error', 'Your word does not exist! Be serious!'

    #pretty prints the returned descirptions
    def pretty_print(self, word):
        #save (corrected) word and description list (of tuples) in descriptions
        descriptions = self.get_results(word)

        #check for error messages:
        if descriptions[0] == 'Key_Error':
            print(f'\n{descriptions[1]}')

        # otherwise print correct word 
        else:
            print(f'\n"{descriptions[0].title()}" has {len(descriptions[1])} description(s): \n')

            # print descriptions for that word - NOTE: each 'description' is a tuple with one value inside
            for description in descriptions[1]:
                print(f'\u2022 {description[0]}')


if __name__ == "__main__":
    word = input('Type a word: ').lower()
    print('\n')
    if len(sys.argv) > 1:
        thesaurus = LocalThesaurus(data)
        thesaurus.pretty_print(word)
    else:
        thesaurus = RemoteThesaurus()
        thesaurus.pretty_print(word)
    

