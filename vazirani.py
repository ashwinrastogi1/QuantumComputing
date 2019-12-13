import numpy as np
import cirq
import random as rand
import random

'''

The code below implements the Bernstein-Vazirani algorithm in the
specific instance of finding factors of a function that generates
a bitstring of given length. The code also generates bitstrings of
random lengths between 1 and 20 and checks if the algorithm returns
a correct value. Based on the current implementation, repeating this
process 100 times (took upto 20 mins) returns the correct factors/bitstring
approximately 60% of the time, i.e. the success rate of the current
implementation is about 60%. This value may vary as I ran it 3 times and
got success rates between 52% and 67%.

'''

DEFAULT_NUM_QUBITS = 4

def bitstring(bits):
    return ''.join([str(int(_)) for _ in bits])

def generate_secret_func(num_bits: int):
    position = rand.randint(0, num_bits - 1)
    return [1 if i == position else rand.randint(0, 1) for i in range(num_bits)]

def compute_algorithm(num_bits=DEFAULT_NUM_QUBITS):
    # Initializing qubits and secret bits
    input_qubits = [cirq.GridQubit(i, 0) for i in range(num_bits)]
    output_qubit = cirq.GridQubit(num_bits, 0)

    bias_bit = rand.randint(0, 1)
    factor_bits = generate_secret_func(num_bits)

    # Creating Oracle
    oracle = []
    if bias_bit:
        oracle = cirq.X(output_qubit)

    else:
        for curr_qubit, curr_bit in zip(input_qubits, factor_bits):
            if curr_bit:
                oracle.append(cirq.CNOT(curr_qubit, output_qubit))

    # Creating Bernstein Vazirani Circuit
    circuit = cirq.Circuit()
    circuit.append([cirq.X(output_qubit), cirq.H(output_qubit), cirq.H.on_each(*input_qubits)])
    circuit.append(oracle)

    circuit.append([cirq.H.on_each(*input_qubits), cirq.measure(*input_qubits, key="result")])

    # Simulating circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=3)
    freq = result.histogram(key="result", fold_func=bitstring)

    most_common_bitstring = freq.most_common(1)[0][0]
    return most_common_bitstring == bitstring(factor_bits)

def main():
    success = 0
    for i in range(100):
        num_bits = rand.randint(1, 20)
        success += int(compute_algorithm(num_bits))
    
    print("Success rate: " + str(success))

if __name__ == '__main__':
    main()
