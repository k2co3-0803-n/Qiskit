import qiskit
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
import random
from math import log2
from math import ceil
import matplotlib.pyplot as plt
import numpy as np

def qft_dagger(qreg):
    qc = QuantumCircuit(qreg)

    for j in range(qreg.size // 2):
        qc.swap(qreg[j], qreg[-1-j])
    for itarg in range(qreg.size):
        for ictrl in range(itarg):
            power = ictrl - itarg - 1
            qc.cp(-2. * np.pi * (2 ** power), ictrl, itarg)
        
        qc.h(itarg)
    
    qc.name = "QFT^dagger"
    return qc