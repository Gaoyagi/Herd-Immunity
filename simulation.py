import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
'''
class Simulation(object):
   
    #initializes: logger(Logger), pop_size(int),
    def __init__(self, pop_size, vacc_percentage, initial_infected=1, virus):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        # TODO: Store each newly infected person's ID in newly_infected attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.
        self.file_name = "{}simulation_pop_{}_vp_{}_infected_{}.txt".format(virus.name, pop_size, vacc_percentage, initial_infected)
        self.newly_infected = []
        self.logger = Logger(self.file_name)
        self.pop_size = pop_size # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected = 0 # Int
        self.current_infected = 0 # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.vacc = vacc_percentage*pop_size
        self.total_dead = 0 # Int
        self.population = self._create_population(pop_size) # List of Person objects
        
        self.next_person_id = 0 # Int
        
        

    #populates a lsit with person objects
    #args: num of initial infected(int), population size(int)
    #return: list of person's
    def _create_population(self, pop_size, init_infected, init_vacc, virus):
        # TODO: Finish this method!  This method should be called when the simulation
        # begins, to create the population that will be used. This method should return
        # an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).

        # Use the attributes created in the init method to create a population that has
        # the correct intial vaccination percentage and initial infected.
        people = []
        id = 0
        pop_size -= init_infected - init_vacc
        for x in range(init_infected):
            people.append(People(id, False, virus))
            id+=1
        for x in range(init_infected):
            people.append(People(id, False, virus))
            id+=1
        return people

    def convertPercent(self):
        self.vacc_percentage = self.vacc/self.pop_size
    #checks if the simulation should end
    #end if everyone is dead or vaccinated
    #args: none
    #return: bool
    def simulation_should_continue(self):
        # TODO: Complete this helper method.  Returns a Boolean.
        if self.vacc_percentage == 1:
            return False
        elif self.total_dead == self.pop_size:
            return False
        else:
            return True 

    #runs simualtion until simulation_should_continue says stop
    #args: none
    #return: none
    def run(self):
        # TODO: Finish this method.  To simplify the logic here, use the helper method
        # _simulation_should_continue() to tell us whether or not we should continue
        # the simulation and run at least 1 more time_step.

        # TODO: Keep track of the number of time steps that have passed.
        # HINT: You may want to call the logger's log_time_step() method at the end of each time step.
        # TODO: Set this variable using a helper
        time_step_counter = 0
        should_continue = None

        while self.simulation_should_continue():
        # TODO: for every iteration of this loop, call self.time_step() to compute another
        # round of this simulation.
            self.time_step()
        print('The simulation has ended after {time_step_counter} turns.'.format(time_step_counter))
        pass

    #TODO: computes 1 time step in simulation
    #args: none
    #return: none
    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a randon person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        # TODO: Finish this method.
        pass
    
    #deals with interaction of  2 living people
    #args: infected person(Person), random person(Person)
    #return: none
    def interaction(self, person, random_person):
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

        # TODO: Finish this method.
        #  The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0 and 1.  If that number is smaller
            #     than repro_rate, random_person's ID should be appended to
            #     Simulation object's newly_infected array, so that their .infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call slogger method during this method

        success = False
        infect = random.randint(0,1)
        if(infect < person.virus.repro_rate):
                success = True
        logger.log_interaction(person, random_person, newly_infected, success)
        
    #iterates through ther persons list and infects whoever's id is on the newly infected list
    #afterwards it resets the newly infected list to blank
    #args: none
    #return: none
    def _infect_newly_infected(self):
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        for person in self.population:
                if person._id in newly_infected:
                    person.infection = self.virus
                    newly_infected.remove(person._id)


if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_num = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(name, repro_rate, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    sim.run()