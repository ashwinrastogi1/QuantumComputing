import numpy as np
import cirq
import random as rand


# Initializing qubits and secret bits
DEFAULT_NUM_QUBITS = 4
input_qubits = [cirq.GridQubit(i, 0) for i in range(DEFAULT_NUM_QUBITS)]
output_qubit = cirq.GridQubit(DEFAULT_NUM_QUBITS, 0)

bias_bit = rand.randint(0, 1)
factor_bits = [rand.randint(0, 1) for i in range(DEFAULT_NUM_QUBITS)]

# Creating Oracle
oracle = None
if bias_bit:
    oracle = cirq.X(output_qubit)

else:
    for curr_qubit, curr_bit in zip(input_qubits, factor_bits):
        if curr_bit:
            oracle = cirq.CNOT(curr_qubit, output_qubit)
            break

# Creating Bernstein Vazirani Circuit
circuit = cirq.Circuit()
circuit.append([cirq.X(output_qubit), cirq.H(output_qubit), cirq.H.on_each(*input_qubits)])

if oracle:
    circuit.append(oracle)

circuit.append([cirq.H.on_each(*input_qubits), cirq.measure(input_qubits, key="result")])
print(circuit)

# Simulating circuit
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=3)
freq = result.histogram(ley="result", fold_fun=bitstring)
print('Sampled results:\n{}'.format(freq))

most_common_bitstring = freq.most_common(1)[0][0]
print('Most common matches secret factors:\n{}'.format(
    most_common_bitstring == bitstring(factor_bits)))

def bitstring(bits):
    return ''.join([str(int(_)) for _ in bits])