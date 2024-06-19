import numpy as np
from qiskit import QuantumCircuit, QuantumRegister


class BitFlip:
    def __init__(self) -> None:
        self.bitflips = {}
        self.circuit = None

    
    def setNumQubits(self, n):
        """
        Set the number of qubits for the quantum circuit.

        Args:
            n (int): The number of qubits to set.
        """
        self.N_qubits = n


    def boost_samples(self, problem, samples: list[str], K: int = 10) -> list:
        self.bitflips.clear()
        boosted = []
        for best_sol in samples:
            bitstring_arr = np.array([int(bit) for bit in best_sol])
            bitstring_str = "".join(map(str, bitstring_arr))
            old_bitstring = bitstring_str
            best_cost = problem.cost(bitstring_str[::-1])
            old_cost = best_cost

            for _ in range (K):
                shuffled_indeces = np.arange(len(best_sol))
                np.random.shuffle(shuffled_indeces)
                for i in shuffled_indeces:
                    bitstring_altered_arr = np.copy(bitstring_arr)
                    bitstring_altered_arr[i] = not(bitstring_arr[i])

                    bitstring_altered_str = "".join(map(str, bitstring_altered_arr))
                    new_cost = problem.cost(bitstring_altered_str[::-1])
                    
                    if new_cost > best_cost: 
                        best_cost = new_cost
                        bitstring_arr = bitstring_altered_arr
                        bitstring_str = bitstring_altered_str
            self.best_bitlfips(old_bitstring, bitstring_str, float(best_cost))
            boosted.append(bitstring_str)
            boost = np.unique(boosted)
        return boost
    

    def best_bitlfips(self, old_string, new_string, cost_diff):
        old = np.array([int(bit) for bit in old_string])
        new = np.array([int(bit) for bit in new_string])
        xor = []

        for a, b in zip(old, new):
            xor.append((a and not b) or (not a and b))

        self.bitflips[str(cost_diff)] = xor


    def get_best_bitflip(self):
        max_diff = max([float(i) for i in self.bitflips.keys()])
        best_xor = self.bitflips[str(max_diff)]
        return best_xor
    

    def create_circuit(self, string):
        q = QuantumRegister(self.N_qubits)
        self.circuit = QuantumCircuit(q)
        self.circuit.x(string[::-1])

        
