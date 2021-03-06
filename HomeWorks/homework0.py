# Question 3

def clock_helper(total_seconds):
    '''
    Function that returns seconds past the minute
    '''
    seconds_in_minute = total_seconds % 60

# it's a trick , nothing is returned
print 'Question 3 returns:', clock_helper(90), '\n'


# Question 8

def valid_dictionary_keys(key):
    '''
    helper function for checking dictionary keys
    '''
    print 'Question 8 results:'
    dictionary = {}
    try:
        dictionary[key] = 1234
        print key, 'is a valid key, results in:', dictionary
    except TypeError:
        print key, 'is not a valid key!'
        
valid_dictionary_keys(False)
valid_dictionary_keys(set([]))
valid_dictionary_keys({})
valid_dictionary_keys("")
valid_dictionary_keys([])
valid_dictionary_keys(0)
print


# Question 9

def appendsums(lst):
    '''
    ppend the sum of the last three elements of list to list 25 times
    loops for 25 times
    '''
    for loop in xrange(25):
        new_last = sum(lst[len(lst) - 3:])
        lst.append(new_last)
    return lst


# test it: should print out '230'
sum_three = [0, 1, 2]
appendsums(sum_three)
print 'Correct answer for testing Question 9 is 230, compare with result:'
print sum_three[10], '\n'
print 'Correct answer for Question 9 is 101902, compare with result:'
print sum_three[20], '\n'


# Question 10

class BankAccount:
    '''
    simple bank acount class
    the deposit and withdraw methods each change the account balance
    '''
    def __init__(self, initial_balance):
        '''creates an account with the given balance'''
        self.balance = initial_balance
        self.fees = 0
        
    def deposit(self, amount):
        '''deposits the amount into the account'''
        self.balance += amount

    def withdraw(self, amount):
        '''
        withdraws the amount from the account; Each withdrawal resulting in a
        negative balance also deducts a penalty fee of 5 dollars from the balance
        '''
        self.balance -= amount
        if self.balance < 0:
            self.balance -= 5
            self.fees += 1
    
    def get_balance(self):
        '''returns the current balance in the account'''
        return self.balance
    
    def get_fees(self):
        '''returns the total fees ever deducted from the account'''
        return self.fees * 5


# test it, should print out '10' & '5'
my_account = BankAccount(10)
my_account.withdraw(15)
my_account.deposit(20)
print 'Correct answers for testing Question 10 are 10 & 5, compare with results:'
print my_account.get_balance(), my_account.get_fees(), '\n'
my_account = BankAccount(10)
my_account.withdraw(5)
my_account.deposit(10)
my_account.withdraw(5)
my_account.withdraw(15)
my_account.deposit(20)
my_account.withdraw(5) 
my_account.deposit(10)
my_account.deposit(20)
my_account.withdraw(15)
my_account.deposit(30)
my_account.withdraw(10)
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(50) 
my_account.deposit(30)
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(5) 
my_account.deposit(20)
my_account.withdraw(15)
my_account.deposit(10)
my_account.deposit(30)
my_account.withdraw(25) 
my_account.withdraw(5)
my_account.deposit(10)
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(10) 
my_account.withdraw(15)
my_account.deposit(10)
my_account.deposit(30)
my_account.withdraw(25) 
my_account.withdraw(10)
my_account.deposit(20)
my_account.deposit(10)
my_account.withdraw(5) 
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(5) 
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(5)
print 'Correct answers for Question 10 are: -60 & 75, compare with results:'
print my_account.get_balance(), my_account.get_fees(), '\n'
