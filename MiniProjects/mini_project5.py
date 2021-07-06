# Word Wrangler described at: https://class.coursera.org/principlescomputing-001/wiki/view?page=wrangler




"""
provided code for Word Wrangler game
"""



class WordWrangler:
    """
    Game class for Word Wrangler
    """
    
    def __init__(self, word_list, remdup, intersect, mergesort, substrs):
        self._word_list = word_list
        self._subset-str = []
        self._guessed-str = []

        self._remove_duplicates = remdup
        self._intersect = intersect
        self._merge_sort = mergesort
        self._substrs = substrs

    def start_game(self, entered_word):
        """
        Start a new game of Word Wrangler
        """
        if entered_word not in self._word_list:
            print "It is not a word!s"
            return
        
        strings = self._substrs(entered_word)
        sorted_str = self._merge_sort(strings)
        all_str = self._remove_duplicates(sorted_str)
        self._guessed-str = []     
        self._subset-str = self._intersect(self._word_list, all_str)     
        for word in self._subset-str:
            self._guessed-str.append("*" * len(word))
        self.enter_guess(entered_word)           
        
    def enter_guess(self, guess):
        """
        Take an entered guess and update the game
        """        
        if ((guess in self._subset-str) and 
            (guess not in self._guessed-str)):
            guess_idx = self._subset-str.index(guess)
            self._guessed-str[guess_idx] = self._subset-str[guess_idx]

    def peek(self, peek_index):
        """
        Exposed a word given in index into the list self._subset-str
        """
        self.enter_guess(self._subset-str[peek_index])
        
    def get_str(self):
        """
        Return the list of strings for the GUI
        """
        return self._guessed-str
    

def run_game(wrangler):
    """
    Start the game.
    """
    poc_wrangler_gui.run_gui(wrangler)
    
    
'''
student code for Word Wrangler game
'''

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = 'assets_scrabble_words3.txt'


# functions to manipulate ordered word lists

def remove_duplicates(list1):
    '''
    eliminate (function can be iterative) duplicates in a sorted list;
    returns a new sorted list with the same elements in list1, without duplicates
    '''
    screened = []
    for el in list1:
        
        if el not in screened:
            screened.append(el)

    return screened

def intersect(list1, list2):
    '''
    compute (this function can be iterative) the intersection of two sorted lists;
    returns a new sorted list containing only elements that are in  both list1 and list2
    '''
    screened = []
    for el in list1:
        
        if el in list2:
            screened.append(el)
            
    return screened




def merge(list1, list2):
    '''
    merge (function can be iterative) two sorted lists;
    returns a new sorted list containing all of the elements that are in either list1 and list2
    '''
    merged = []

    copy1, copy2 = list1[:], list2[:]
    while min(copy1, copy2):
        if copy1[0] < copy2[0]:
            merged.append(copy1[0])
            copy1.pop(0)
        else:
            merged.append(copy2[0])
            copy2.pop(0)

    if copy1:
        merged += copy1
    else:
        merged += copy2
   
    return merged
                
def merge_sort(list1):
    '''
    sort (function shall be recursive!) the elements of list1, makes use of merge() function;
    returns a new sorted list with the same elements as list1
    '''
    
    if len(list1) <= 1:
        return list1
    
    half = len(list1) / 2
    
    return merge(merge_sort(list1[:half]), merge_sort(list1[half:]))
    



def gen_all_str(word):
    '''
    generate (function shall be recursive!) all strings that can be composed
    from the letters in word in any order;
    returns a list of all strings that can be formed from the letters in word
    '''
    # recursvie function
    if not word:
        return ['']
    
    poss = []
    
    for string in gen_all_str(word[1:]):
        for index in range(len(string) + 1):
           
            poss.append(string[:index] + word[0] + string[index:])
            
    return gen_all_str(word[1:]) + poss


# function to load words from a file

def load_words(filename):
    '''
    load word list from the file named filename;
    returns a list of strings
    '''
    try:
        file = open(filename)
    except IOError as e:
        print 'Your scrabble words file is missing. '
     
    return [word[:-1] for word in file]
    
def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_str)
    provided.run_game(wrangler)

# uncomment when you are ready to try the game
# run()
