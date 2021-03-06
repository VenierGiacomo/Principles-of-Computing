# Zombie Apocalypse described at: https://class.coursera.org/principlescomputing-001/wiki/view?page=zombie

"""
Grid class
"""

EMPTY = 0
FULL = 1

class Grid:
    """
    Implementation of 2D grid of cells
    Includes boundary handling
    """
    
    def __init__(self, grid_height, grid_width):
        """
        Initializes grid to be empty, take height and width of grid as parameters
        Indexed by rows (left to right), then by columns (top to bottom)
        """
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._cells = [[EMPTY for _ in range(self._grid_width)] 
                       for __ in range(self._grid_height)]
                
    def __str__(self):
        """
        Return multi-line string represenation for grid
        """
        answer = ""
        for row in range(self._grid_height):
            answer += str(self._cells[row])
            answer += "\n"
        return answer
    
    def get_grid_height(self):
        """
        Return the height of the grid for use in the GUI
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Return the width of the grid for use in the GUI
        """
        return self._grid_width


    def clear(self):
        """
        Clears grid to be empty
        """
        self._cells = [[EMPTY for _ in range(self._grid_width)]
                       for __ in range(self._grid_height)]
                
    def set_empty(self, row, col):
        """
        Set cell with index (row, col) to be empty
        """
        self._cells[row][col] = EMPTY
    
    def set_full(self, row, col):
        """
        Set cell with index (row, col) to be full
        """
        self._cells[row][col] = FULL
    
    def is_empty(self, row, col):
        """
        Checks whether cell with index (row, col) is empty
        """
        return self._cells[row][col] == EMPTY
 
    def four_neighbors(self, row, col):
        """
        Returns horiz/vert neighb of cell (row, col)
        """
        answer = []
        if row > 0:
            answer.append((row - 1, col))
        if row < self._grid_height - 1:
            answer.append((row + 1, col))
        if col > 0:
            answer.append((row, col - 1))
        if col < self._grid_width - 1:
            answer.append((row, col + 1))
        return answer

    def eight_neighbors(self, row, col):
        """
        Returns horiz/vert neighb of cell (row, col) as well as
        diagonal neighb
        """
        answer = []
        if row > 0:
            answer.append((row - 1, col))
        if row < self._grid_height - 1:
            answer.append((row + 1, col))
        if col > 0:
            answer.append((row, col - 1))
        if col < self._grid_width - 1:
            answer.append((row, col + 1))
        if (row > 0) and (col > 0):
            answer.append((row - 1, col - 1))
        if (row > 0) and (col < self._grid_width - 1):
            answer.append((row - 1, col + 1))
        if  (col > 0)and (row < self._grid_height - 1):
            answer.append((row + 1, col - 1))
        if (col < self._grid_width - 1) and (row < self._grid_height - 1) :
            answer.append((row + 1, col + 1))
        return answer
    
    def get_index(self, point, cell_size):
        """
        Takes point in screen coordinates and returns index of
        containing cell
        """
        return (point[1] / cell_size, point[0] / cell_size) 


# Queue class from http://www.codeskulptor.org/#poc_queue.py

'''
Queue class
'''

class Queue:
    """
    A simple implementation of a FIFO queue.
    """

    def __init__(self):
        """ 
        Initialize the queue.
        """
        self._items = []

    def __len__(self):
        """
        Return the number of items in the queue.
        """
        return len(self._items)
    
    def __iter__(self):
        """
        Create an iterator for the queue.
        """
        for item in self._items:
            yield item

    def __str__(self):
        """
        Return a string representation of the queue.
        """
        return str(self._items)

    def enqueue(self, item):
        """
        Add item to the queue.
        """        
        self._items.append(item)

    def dequeue(self):
        """
        Remove and return the least recently inserted item.
        """
        return self._items.pop(0)

    def clear(self):
        """
        Remove all items from the queue.
        """
        self._items = []
        

'''
student portion of Zombie Apocalypse mini-project
'''

import random

EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 'obstacle'
HUMAN = 'human'
ZOMBIE = 'zombie'


class Zombie(Grid): 
    
    '''
    class for simulating zombie pursuit of human on grid with obstacles
    '''

    def __init__(self, grid_height, grid_width, obstacles = None, 
                 zombie_list = None, human_list = None):
        '''
        create a simulation of given size with given obstacles, humans, and zombies
        '''
        Grid.__init__(self, grid_height, grid_width)   
        if obstacles != None:
            for cell in obstacles:
                self.set_full(cell[0], cell[1])
            
            self._obstacle_list = obstacles
        else:
            self._obstacle_list = []
        if zombie_list != None:
            self._zombies = list(zombie_list)
        else:
            self._zombies = []
        if human_list != None:
            self._humans = list(human_list)  
        else:
            self._humans = []
            
    def clear(self):
        '''
        set cells in obstacle grid to be empty,
        reset zombie and human lists to be empty
        '''        
        self._zombies = []
        self._humans = []
        Grid.clear(self)    
        
    def add_zombie(self, row, col):
        '''
        add a zombie to the zombie list
        '''
        self._zombies.append((row, col))
                
    def num_zombies(self):
        '''
        return current number of zombies
        '''
        return len(self._zombies)
          
    def zombies(self):
        '''
        generator that yields the zombies in the order they were added
        '''
        for zombie in self._zombies:
            yield zombie

    def add_human(self, row, col):
        '''
        add human to the human list
        '''
        self._humans.append((row, col))
        
    def num_humans(self):
        '''
        return current number of humans
        '''
        return len(self._humans)
        
    def humans(self):
        '''
        generator that yields the humans in the order they were added
        '''
        for human in self._humans:
            yield human

    def obstacle(self):
        '''
        generator that yields the list of obstacles
        '''
        for obstacle in self._obstacle_list:
            yield obstacle

    def compute_distance_field(self, entity_type):
        '''
        function computes a 2D dist field, dist at member of entity_queue is zero;
        shortest paths avoid obstacles and use distance_type distances
        '''
        
        distance_field =[[self._grid_height * self._grid_width for _ in range(self._grid_width)] 
                         for __ in range(self._grid_height)]

        
        visited = Grid(self._grid_height, self._grid_width) 
        for obstacle in self.obstacle():
            visited.set_full(obstacle[0], obstacle[1])
        
        
        boundary = Queue()   
        if entity_type == ZOMBIE:
            list_type = self._zombies
        elif entity_type == HUMAN:
            list_type = self._humans

        
        for item in list_type:
            boundary.enqueue(item)
            visited.set_full(item[0], item[1])
            distance_field[item[0]][item[1]] = 0

        
        while boundary:
            cell = boundary.dequeue()
            neighb = visited.four_neighbors(cell[0], cell[1])
            for resident in neighb:
                if visited.is_empty(resident[0], resident[1]):
                    distance_field[resident[0]][resident[1]] = min(distance_field[resident[0]][resident[1]],
                                                                   distance_field[cell[0]][cell[1]] + 1)
                    visited.set_full(resident[0], resident[1])
                    boundary.enqueue(resident)                               

        return distance_field    

    def move_humans(self, zombie_distance):
        '''
        function that moves humans away from zombies, diagonal moves are allowed,
        returns noting
        '''
        temp_humans = []
        for human in self.humans():
            neighb = self.eight_neighbors(human[0], human[1])
            
            dist = [zombie_distance[human[0]][human[1]]]
            location = [human]
            
            for resident in neighb:
                if self.is_empty(resident[0], resident[1]):
                    
                    dist.append(zombie_distance[resident[0]][resident[1]])
                    location.append(resident)
            
            safest = location[dist.index(max(dist))]          
            self.set_empty(human[0], human[1])
            temp_humans.append(safest)
            
        self._humans = temp_humans

    
    def move_zombies(self, human_distance):
        '''
        function that moves zombies towards humans, diagonal moves are NOT allowed,
        returns nothing
        '''
        temp_zombies = []

        for zombie in self._zombies:
            neighb = self.four_neighbors(zombie[0], zombie[1])
            
            dist = [human_distance[zombie[0]][zombie[1]]]
            location = [zombie]
            
            for resident in neighb:
                if self.is_empty(resident[0], resident[1]):
                    
                    dist.append(human_distance[resident[0]][resident[1]])
                    location.append(resident)
            
            closest = location[dist.index(min(dist))]          
            self.set_empty(zombie[0], zombie[1])
            temp_zombies.append(closest)
            
        self._zombies = temp_zombies


# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Zombie(30, 40))
