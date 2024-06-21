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

    def boost_samples(self, problem, samples: list[str] | str, K: int = 10) -> list:
        """
        Random bitflips on string/list og strings to increase cost.
        Calls best_bitflips() that updates self.bitflips

        imput:
            - problem: BaseType Problem 
            - samples: string or list og strings
            - K: number of iteratations through string while flipping 
        returns:
            - list of strings after bitflips
        """
        self.bitflips.reset()
        boosted = []

        if type(samples) == str:
            samples = list(samples)

        for best_sol in samples:
            string_arr = np.array([int(bit) for bit in best_sol])
            string = "".join(map(str, string_arr))
            old_string = string
            best_cost = problem.cost(string[::-1])

            for _ in range (K):
                shuffled_indeces = np.arange(len(best_sol))
                np.random.shuffle(shuffled_indeces)

                for i in shuffled_indeces:
                    string_arr_altered = np.copy(string_arr)
                    string_arr_altered[i] = not(string_arr[i])
                    string_altered = "".join(map(str, string_arr_altered))
                    new_cost = problem.cost(string_altered[::-1])
                    
                    if new_cost > best_cost: 
                        best_cost = new_cost
                        string_arr = string_arr_altered
                        string = string_altered
                            
            self.best_bitlfips(old_string, string, float(best_cost))
            boosted.append(string)
        return boosted
    

    def best_bitlfips(self, old_string: str, new_string: str, cost: float) -> None:
        """
        Finds (old_string XOR new_string)
        Updates self.bitstrings with cost of new_string as key and XOR-string as value

        input:
            - old_string: string before bitflips
            - new_string: string after bitflips 
            - cost: cost of new_string
        returns:
            None
        """
        old = np.array([int(bit) for bit in old_string])
        new = np.array([int(bit) for bit in new_string])
        xor = []

        for a, b in zip(old, new):
            xor.append((a and not b) or (not a and b))

        self.bitflips[str(cost)] = xor


    def get_best_bitflip(self) -> str:
        """
        Returns the XOR-string with highest cost
        """
        max_diff = max([float(i) for i in self.bitflips.keys()])
        best_xor = self.bitflips[str(max_diff)]
        return best_xor
    

    def create_circuit(self, string: str) -> None:
        """
        Creates quantum circuit that performs bitflips

        input:
            - string to be applied to circuit
                if 1 at pos n - i, apply X-gate to qubit i
                if 0 at pos n - j, do nothing to qubit j
        returns:
            None
        """
        q = QuantumRegister(self.N_qubits)
        self.circuit = QuantumCircuit(q)
        xor = np.array([int(bit) for bit in string[::-1]])
        for i, x in enumerate(xor):
            if x:
                self.circuit.x(i)