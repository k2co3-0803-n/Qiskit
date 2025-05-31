import qiskit
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
import random
from math import log2
from math import ceil
import matplotlib.pyplot as plt

def c_amod15(a, l):
    if a not in [2, 4, 7, 8, 11, 13]:
        raise ValueError("a must be one of the following values: 2, 4, 7, 8, 11, or 13.")
    U = QuantumCircuit(4)
    if a in [2, 13]:
        U.swap(3, 2)
        U.swap(2, 1)
        U.swap(1, 0)
    elif a in [4, 11]:
        U.swap(3, 1)
        U.swap(2, 0)
    elif a in [7, 8]:
        U.swap(1, 0)
        U.swap(2, 1)
        U.swap(3, 2)
    if a in [7, 11, 13]:
        U.x([0, 1, 2, 3])
    
    U_power = U.repeat(2 ** l)
    gate = U_power.to_gate()
    gate.name = f"{a}^{2 ** l} mod 15"
    c_gate = gate.control()
    
    return c_gate


