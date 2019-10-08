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
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected=1):
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
        #for files
        self.file_name = "{}simulation_pop_{}_vp_{}_infected_{}.txt".format(virus.name, pop_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name)

        #ints
        self.pop_size = pop_size 
        self.currentAlive = pop_size
        self.total_infected = initial_infected 
        self.vacc = int(vacc_percentage*pop_size) 
        self.total_dead = 0 
        self.initial_infected = initial_infected 
        self.curr_infected = 0 
        self.curr_dead = 0      
       
        #floats
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        
        #class objects
        self.virus = virus  #Virus object
        
        #lists
        self.newly_infected = []    #list of id's of newly infected
        self.population = self._create_population() # List of Person objects
        
        
        

    #populates a list with person objects
    #args: num of initial infected(int), population size(int)
    #return: list of person's
    def _create_population(self):
        # TODO: Finish this method!  This method should be called when the simulation
        # begins, to create the population that will be used. This method should return
        # an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).

        # Use the attributes created in the init method to create a population that has
        # the correct intial vaccination percentage and initial infected.
        people = []
        id = 0
        pop_size = self.pop_size - self.initial_infected - self.vacc
        for x in range(self.initial_infected):
            people.append(Person(id, False, self.virus))
            id+=1
        for x in range(self.vacc):
            people.append(Person(id, True))
            id+=1
        for x in range(pop_size):
            people.append(id)
            id+=1
        return people

    #gets the current percent of vaccinated people
    #args: none
    #return: none
    def convertPercent(self):
        percentage = int(self.vacc/self.pop_size)
        return percentage


    #checks if the simulation should end
    #end if everyone is dead or vaccinated
    #args: none
    #return: bool
    def simulation_should_continue(self):
        # TODO: Complete this helper method.  Returns a Boolean.
        self.vacc_percentage = self.convertPercent()
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

        while self.simulation_should_continue():
            self.time_step()
            for people in self.population:
                if not people.resolve_infection:
                    self.curr_dead+=1
                    self.total_dead+=1
            self._infect_newly_infected()
            self.logger.log_time_step(time_step_counter, self.curr_infected, self.total_infected, self.curr_dead, self.total_dead)
            time_step_counter+=1

        print('The simulation has ended after {time_step_counter} turns.'.format(time_step_counter))

    #computes 1 time step in simulation
    #args: none
    #return: none
    def time_step(self):
        '''This includes:
            1. 100 total interactions with a random person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        self.curr_dead = 0
        self.curr_infected = 0
        for person in self.population:
            if person.infection != None:
                # for p in random.sample(self.population, k=min(len(self.population), 100)):
                #     pass
                for y in range(100):
                    #get a new  random person to interact with as long as the random is a dead person
                    while True:
                        try:
                            self.interaction(person, random.choice(self.population))
                        except:
                            continue
                        else:
                            break

    #deals with interaction of 2 living people
    #args: infected person(Person), random person(Person)
    #return: none
    def interaction(self, person, random_person):
        # Assert statements are included to make sure that only living people are passed in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

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

        success = None
        infect = random.uniform(0,1)
        if random_person.is_vaccinated or random_person.infection != None or infect < person.virus.repro_rate:
            success = False
        else:
            success = True
            self.curr_infected+=1
            self.total_infected+=1
        self.logger.log_interaction(person, random_person, self.newly_infected, success)
            
        
    #iterates through ther persons list and infects whoever's id is on the newly infected list
    #afterwards it resets the newly infected list to blank
    #args: none
    #return: none
    def _infect_newly_infected(self):
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        for person in self.population:
            if person._id in self.newly_infected:
                person.infection = self.virus
                self.total_infected+=1
                self.newly_infected.remove(person._id)


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

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    sim.run()