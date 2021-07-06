# Yahtzee (simplified) described at: https://class.coursera.org/principlescomputing-001/wiki/view?page=yahtzee

"""
Test suite for gen_all_holds in "Yahtzee"
"""

##import poc_simpletest
##
##def run_suite(gen_all_holds):
##    """
##    Some informal testing code for gen_all_holds
##    """
##    
##    # create a TestSuite object
##    suite = poc_simpletest.TestSuite()
##    
##    # test gen_all_holds on various inputs
##    hand = tuple([])
##    suite.run_test(gen_all_holds(hand), set([()]), "Test #1:")
##
##    hand = tuple([4, 2])
##    suite.run_test(gen_all_holds(hand), set([(), (4,), (2,), (4, 2)]), "Test #2:")
##    
##    hand = tuple((1, 2, 2))
##    suite.run_test(gen_all_holds(hand), set([(), (1,), (2,), (1, 2), (2, 2), (1, 2, 2)]), "Test #3:")
##
##    hand = tuple((2, 1, 2))
##    suite.run_test(gen_all_holds(hand), set([(), (1,), (2,), (1, 2), (2, 1), (2, 2), (2, 1, 2)]), "Test #4:")
##
##    hand = tuple([6, 2, 3])
##    suite.run_test(gen_all_holds(hand),set([(), (6,), (2,), (6, 2), (3,), (6, 3), (2, 3), (6, 2, 3)]), "Test #5:")
##
##    suite.report_results()
##    


'''
planner for Yahtzee
simplified (only allow discard and roll, only score against upper level)
'''

# used to increase the timeout, if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


def gen_all_sequences(outcomes, length):
    '''
    iterative function that enumerates the set of all sequences of outcomes of given length;
    original code from the lecture, do not modify
    '''
    answer = set([()])
    for _ in range(length):
        temp_set = set()
        for partial_sequence in answer:
            for el in outcomes:
                new_seq = list(partial_sequence)
                new_seq.append(el)
                temp_set.add(tuple(new_seq))
        answer = temp_set
    return answer


def score(hand):
    '''
    compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card

    hand (die values in a tuple): full yahtzee hand

    returns an integer score
    '''
    # empty hand returns 0
    if not hand:
        return 0
    
    maximum = []
    for el in hand:
        maximum.append(hand.count(el) * el)
    return max(maximum)


def expected_value(held_dice, num_die_sides, num_free_dice):
    '''
    compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides

    held_dice (a tuple): dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    returns a floating point expected value
    '''
    scores = []
    sides = [die for die in range(1, num_die_sides + 1)]
    possible_sequence = gen_all_sequences(sides, num_free_dice)

    for el in possible_sequence:
        scores.append(score(held_dice + el))
    
    return float(sum(scores)) / len(scores)

    
def gen_all_holds(hand):
    '''
    generate all possible choices of dice from hand to hold

    hand (a tuple): full yahtzee hand

    returns a set of tuples, where each tuple is dice to hold
    '''
    hand = [()]
    for el in hand:
        for subset in hand:
            hand = hand + [tuple(subset) + (el, )]
           
    return set(hand)
            
    
def strategy(hand, num_die_sides):
    '''
    compute the hold that maximizes the expected value when the discarded dice are rolled

    hand (a tuple): full yahtzee hand
    num_die_sides: number of sides on each die

    returns a tuple (where the first element is the expected score,
    the second element is a tuple of the dice to hold)
    '''
    result = (0.0, ())
    curr_val = float('-inf')
    
    for el in gen_all_holds(hand):
        # looking for maximum value, keeping track along the way
        value = expected_value(el, num_die_sides, len(hand) - len(el))
        if value > curr_val:
            curr_val = value
            result = (curr_val, el)
    
    return result

#print strategy((1,), 6)
#print strategy((1, 8, 8), 6)

def run_example():
    '''
    compute the dice to hold and expected score for an example hand
    '''
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print 'Best strategy for hand ', hand, 'is to hold', hold, 'with expected score', hand_score
    
    
#run_example()

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
