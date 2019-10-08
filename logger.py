from person import Person
from  virus import  Virus

''' Utility class responsible for logging all interactions during the simulation. '''
class Logger(object):

    def __init__(self, file_name):
        self.file_name = str(file_name)
    
    #writes the specific parameters of the simulation to the first line of the file.
    #args: size of population(int), percentage vaccinated(float), virus object
    #return none
    def write_metadata(self, pop_size, vacc_percentage, virus):
        # TODO: Finish this method. This line of metadata should be tab-delimited
        # it should create the text log that we will store all logs in.
        # TIP: Use 'w' mode when you open the file. For all other methods, use
        # the 'a' mode to append a new log to the end, since 'w' overwrites the file.
        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!
        log = open(self.file_name, 'w')
        log.write(f"population size: {pop_size}, vaccinated percent: {vacc_percentage}%, virus: {virus.name}, reprocution rate:{virus.repro_rate}%, mortality rate: {virus.mortality_rate}\n")
        log.close()

    #writes to log every interaction a sick person has during each time step.
    #args: current person(Person), random person(Person)
    #return: none
    def log_interaction(self, person, random_person, infected, did_infect):
        '''
        The format of the log should be: "{person.ID} infects {random_person.ID} \n"
        or the other edge cases:
            "{person.ID} didn't infect {random_person.ID} because {'vaccinated' or 'already sick'} \n"
        '''
        # TODO: Finish this method. Think about how the booleans passed (or not passed)
        # represent all the possible edge cases. Use the values passed along with each person,
        # along with whether they are sick or vaccinated when they interact to determine
        # exactly what happened in the interaction and create a String, and write to your logfile.
       
        log = open(self.file_name, 'a')

        #edge cases are checked first
        if not random_person.is_vaccinated:                                               #check if person is vaccinated
            if random_person.infection == None and random_person._id not in infected:     #check if person is already sick
                if did_infect:                                                              #check if the infection number was higher
                    log.write(f"{person._id} infected {random_person._id} with {person.infection.name} \n")
                    infected.append(random_person._id)
                else:
                     log.write(f"{person._id} didn't infect {random_person._id} \n")
            else:
                log.write(f"{person._id} didn't infect {random_person._id} because they're already sick \n")
        else:
            log.write(f"{person._id} didn't infect {random_person._id} because they're vaccinated \n")
    
        log.close() 

        
    #writes to log the results of every call of a Person object's .resolve_infection() method.
    #args: current person(Person), a bool???? probably not  necessary
    #return: none? might change to a bool later
    def log_infection_survival(self, person):
        ''' 
        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        # TODO: Finish this method. If the person survives, did_die_from_infection
        # should be False.  Otherwise, did_die_from_infection should be True.
        # Append the results of the infection to the logfile
        living = person.resolve_infection()
        log = open(self.file_name, 'a')
        if living:
            log.write(f"{person._id} survived the infection and is now vaccinated\n")
            log.close()
            return True          
        else:
            log.write(f"{person._id} died from the infection\n")
            log.close()
            return False
        

    #write to log the overall summary of the statistics of a time step
    #args: speicifc time step(int)
    #return: none
    def log_time_step(self, time_step_number, currInfect, infect, currDeath, death):
        ''' STRETCH CHALLENGE DETAILS:

        If you choose to extend this method, the format of the summary statistics logged
        are up to you.

        At minimum, it should contain:
            The number of people that were infected during this specific time step.
            The number of people that died on this specific time step.
            The total number of people infected in the population, including the newly infected
            The total number of dead, including those that died during this time step.

        The format of this log should be:
            "Time step {time_step_number} ended, beginning {time_step_number + 1}\n"
        '''
        # TODO: Finish this method. This method should log when a time step ends, and a
        # new one begins.
        # NOTE: Here is an opportunity for a stretch challenge!
        log = open(self.file_name, 'a')
        log.write(f"Time step {time_step_number} ended, beginning time step {time_step_number + 1}\n")
        log.write(f"{currInfect} were infected with {infect} overall were infected \n")
        log.write(f"{currDeath} were killed with {death} total dead \n")
        log.close()
        