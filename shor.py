import qiskit
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
import random
from math import log2
from math import ceil
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction
from qiskit.primitives import StatevectorSampler as Sampler
from oracle import c_amod15
from qft_dagger import qft_dagger
from qiskit.visualization import plot_distribution

N = 15
a = 7

n_meas = 8
qreg_meas = QuantumRegister(n_meas, name="meas")
qreg_aux = QuantumRegister(4, name="aux")
creg_meas = ClassicalRegister(n_meas, name="out")

qc = QuantumCircuit(qreg_meas, qreg_aux, creg_meas)
qc.h(qreg_meas)
qc.x(qreg_aux[0])

for l, ctrl in enumerate(qreg_meas):
    qc.append(c_amod15(a, l), qargs=([ctrl] + qreg_aux[:]))

qc.append(qft_dagger(qreg_meas), qargs=qreg_meas)

qc.measure(qreg_meas, creg_meas)
qc.draw('mpl')
plt.show()

shots = 10000
sampler = Sampler()
sampler_job = sampler.run([qc], shots=shots)
answer = sampler_job.result()
counts = answer[0].data.out.get_counts()

rows, measured_phases = [], []
# 修正: countsから測定結果を取得
for output in counts:
    decimal_output = int(output, 2)  # バイナリ文字列を整数に変換
    phase = decimal_output / (2 ** n_meas)
    measured_phases.append(phase)
    rows.append(f"{decimal_output:3d} {decimal_output:3d}/{2 ** n_meas} = {phase:.3f}")

print('Register Output    Phase')
print('------------------------')
for row in rows:
    print(row)

rows = []
for phase in measured_phases:
    frac = Fraction(phase).limit_denominator(15)
    # 有効な結果のみを表示（分母が1でない場合）
    if frac.denominator > 1:
        rows.append(f'{phase:10.3f}    {frac.numerator:2d}/{frac.denominator:2d} {frac.denominator:13d}')

print('Phase Fraction Guess for r')
print('------------------------')
for row in rows:
    print(row)

# 期間rの推定
print('\nEstimated period r:')
for phase in measured_phases:
    frac = Fraction(phase).limit_denominator(15)
    if frac.denominator > 1 and frac.denominator < 15:
        print(f'r = {frac.denominator}')

# 最も頻度の高い測定結果から期間を推定
most_frequent = max(counts, key=counts.get)
decimal_most_frequent = int(most_frequent, 2)
phase_most_frequent = decimal_most_frequent / (2 ** n_meas)
frac_most_frequent = Fraction(phase_most_frequent).limit_denominator(15)

print(f'\nMost frequent measurement: {most_frequent} (decimal: {decimal_most_frequent})')
print(f'Corresponding phase: {phase_most_frequent:.3f}')
print(f'Estimated period r: {frac_most_frequent.denominator}')

# 因数分解の実行
if frac_most_frequent.denominator > 1:
    r = frac_most_frequent.denominator
    if r % 2 == 0:  # rが偶数の場合のみ
        factor1 = np.gcd(a**(r//2) - 1, N)
        factor2 = np.gcd(a**(r//2) + 1, N)
        print(f'\nFactors of {N}: {factor1} × {factor2} = {factor1 * factor2}')
    else:
        print(f'\nPeriod r={r} is odd, need to run algorithm again')