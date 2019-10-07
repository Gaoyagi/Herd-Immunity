from person import Person
from  virus import  Virus
 ''' Utility class responsible for logging all interactions during the simulation. '''
class Logger(object):

    def __init__(self, file_name):
        self.file_name = str(file_name)+".txt"
    
    #writes the specific parameters of the simulation to the first line of the file.
    #args: size of population(int), percentage vaccinated(float), virus object
    #return none
    def write_metadata(self, pop_size, vacc_percentage, virus):
        # TODO: Finish this method. This line of metadata should be tab-delimited
        # it should create the text file that we will store all logs in.
        # TIP: Use 'w' mode when you open the file. For all other methods, use
        # the 'a' mode to append a new log to the end, since 'w' overwrites the file.
        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!
        file = open(self.file_name, 'w')
        file.write(f"""population size:{pop_size}, vaccinated percent:{vacc_percentage}%, 
                    virus: {virus.name}, reprocution rate:{virus.repro_rate}%, mortality rate:{virus.mortality_rate}      \n""")
        file.close()

    #writes to file every interaction a sick person has during each time step.
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
       
        file = open(self.file_name, 'a')

        #edge cases are checked first
        if not random_person.vaccinated:
            if random_person.infection == None:
                if not did_infect:
                    file.write(f"{person.id} didn't infect {random_person.id}")"
                else:
                    file.write(f"{person.id} infected {random_person.id} with {person.infection.name}")
                    infected.append(random_person._id)
            else:
                file.write(f"{person.id} didn't infect {random_person.id} because they are already sick")
        else:
            file.write(f"{person.id} didn't infect {random_person.id} because they are vaccinated")
    
        file.close() 

        
    #writes to file the results of every call of a Person object's .resolve_infection() method.
    #args: current person(Person), a bool???? probably not  necessary
    #return: none? might change to a bool later
    def log_infection_survival(self, person, did_die_from_infection):
        ''' 
        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        # TODO: Finish this method. If the person survives, did_die_from_infection
        # should be False.  Otherwise, did_die_from_infection should be True.
        # Append the results of the infection to the logfile
        living = person.resolve_infection()
        file = open(self.file_name, 'a')
        if living:
            file.write(f"{person._id} survived the infection and is now vaccinated")
        else:
            file.write(f"{person._id} died from the infection")
        file.close()

    #write to file the overall summary of the statistics of a time step
    #args: speicifc time step(int)
    #return: none
    def log_time_step(self, time_step_number):
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
        