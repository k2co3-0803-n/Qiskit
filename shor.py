import qiskit
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
import random
from math import log2
from math import ceil
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
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
qc.barrier()

for l, ctrl in enumerate(qreg_meas):
    qc.append(c_amod15(a, l), qargs=([ctrl] + qreg_aux[:]))

qc.barrier()
qc.append(qft_dagger(qreg_meas), qargs=qreg_meas)

qc.barrier()
qc.measure(qreg_meas, creg_meas)

qc.draw('mpl')
plt.show()

# 修正: Qiskit 2.0.2のSamplerV2の使用方法
shots = 10000
backend = AerSimulator()

# 回路の最適化
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_qc = pm.run(qc)

# SamplerV2の使用
sampler = Sampler(mode=backend)
job = sampler.run([isa_qc], shots=shots)
result = job.result()

# 結果の取得（Qiskit 2.0.2対応）
counts = result[0].data.out.get_counts()

# 測定結果を頻度順にソート
sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

print('Register Output    Phase      Count   Probability')
print('------------------------------------------------')

measured_phases = []
for output, count in sorted_counts:
    decimal_output = int(output, 2)
    phase = decimal_output / (2 ** n_meas)
    probability = count / shots
    measured_phases.append((phase, count))
    print(f"{output:>8s} ({decimal_output:>3d})  {phase:>6.3f}     {count:>5d}   {probability:>7.3f}")

print('\nPhase Fraction Analysis')
print('Phase      Fraction    Possible r    Count')
print('------------------------------------------')

# 周期候補の分析
period_candidates = {}
for output, count in sorted_counts:
    decimal_output = int(output, 2)
    phase = decimal_output / (2 ** n_meas)
    frac = Fraction(phase).limit_denominator(15)
    
    if frac.denominator > 1 and frac.denominator < 15:
        r = frac.denominator
        if r in period_candidates:
            period_candidates[r] += count
        else:
            period_candidates[r] = count
        print(f"{phase:>6.3f}    {frac.numerator:>2d}/{frac.denominator:<2d}        {r:>2d}        {count:>5d}")

# 最も可能性の高い周期を選択
if period_candidates:
    sorted_periods = sorted(period_candidates.items(), key=lambda x: x[1], reverse=True)
    most_likely_r = sorted_periods[0][0]
    
    print(f'\nPeriod Estimation (sorted by frequency):')
    print('----------------------------------------')
    for r, total_count in sorted_periods:
        probability = total_count / shots
        print(f"r = {r:>2d}    Count: {total_count:>5d}    Probability: {probability:>6.3f}")
    
    print(f'\nMost likely period: r = {most_likely_r}')
    
    # 因数分解の実行
    if most_likely_r % 2 == 0:
        factor1 = np.gcd(a**(most_likely_r//2) - 1, N)
        factor2 = np.gcd(a**(most_likely_r//2) + 1, N)
        
        print(f'\nFactorization attempt with r = {most_likely_r}:')
        print(f'gcd({a}^{most_likely_r//2} - 1, {N}) = {factor1}')
        print(f'gcd({a}^{most_likely_r//2} + 1, {N}) = {factor2}')
        
        if factor1 > 1 and factor1 < N:
            print(f'\nSuccess! {N} = {factor1} × {N // factor1}')
        elif factor2 > 1 and factor2 < N:
            print(f'\nSuccess! {N} = {factor2} × {N // factor2}')
        else:
            print(f'\nNo non-trivial factors found')
    else:
        print(f'\nPeriod r = {most_likely_r} is odd, retry needed')
else:
    print('\nNo valid period candidates found')

# 結果の可視化
plot_distribution(counts, title=f"Shor's Algorithm Results (N={N}, a={a})")
plt.show()