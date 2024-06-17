from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Parameter

from .base_mixer import Mixer


class Y(Mixer):
    def create_circuit(self):
        q = QuantumRegister(self.N_qubits)
        mixer_param = Parameter("x_beta")

        self.circuit = QuantumCircuit(q)
        self.circuit.ry(-2 * mixer_param, range(self.N_qubits))