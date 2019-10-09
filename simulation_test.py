from simulation import  Simulation
from person import Person
from logger import Logger
from virus import Virus

def test_create_population():
    virus = Virus("memes", 0.69, 0.42)
    sim = Simulation(10,)