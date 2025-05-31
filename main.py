import qiskit
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
import random
from math import log2
from math import ceil
import matplotlib.pyplot as plt

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Preparation of a number that is coprime to N
def coprime(N):
    x = random.randint(2, N - 1)
    if gcd(N, x) == 1:
        return x
    else:
        coprime(N)

def modular_multipllication(qc, x, N, register1, register2):
    if x not in [2, 4, 7, 8, 11, 13]:
        raise ValueError("x must be one of the following values: 2, 4, 7, 8, 11, or 13.")
    
    U = QuantumCircuit(4)

    if x == 2:
        U.swap(3, 2)
        U.swap(2, 1)
        U.swap(1, 0)
    elif x == 4:
        U.swap   

def step3(N, x, epsilon):
    L = log2(N)
    num_register1 = ceil(2 * L + 1 + log2(3 + 1 / (2 * epsilon)))
    quantum_register1 = QuantumRegister(num_register1, 'register1')
    num_register2 = ceil(L)
    quantum_register2 = QuantumRegister(num_register2, 'register2')
    classical_register = ClassicalRegister(num_register1, 'classical_register')
    qc = QuantumCircuit(quantum_register1, quantum_register2, classical_register)
    qc.h(quantum_register1)
    qc.x(quantum_register2)
    qc.draw('mpl')
    plt.show()

step3(15, 2, 0.01)