from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.result import marginal_counts

class Qtic:
    def __init__(self, backend):
        self.result = {str(i): None for i in range(9)} 
        self.backend = backend
        # 13 qubits (9 board + 4 helpers), 13 classical bits
        self.circuit = QuantumCircuit(13, 13)
        self.circuit.h([i for i in range(13)])
        
    def hadamard(self, i):
        self.circuit.h(i)

    def pauliz(self, i):
        self.circuit.z(i)

    def cnot(self, i, j):
        self.circuit.cx(i, j)

    def swap(self, i, j):
        self.circuit.swap(i, j)

    def teleportation(self, i, j, m):
        # Reinitialize Bell pair qubits
        self.circuit.reset(j)
        self.circuit.reset(m)
        self.circuit.h(j) 
        self.circuit.h(m)
        self.circuit.cx(m, j)
        self.circuit.barrier()
        
        # Sender's protocol 
        self.circuit.cx(i, m)
        self.circuit.h(i)
        self.circuit.measure(i, i)
        self.circuit.measure(m, m)
        self.circuit.barrier()
        
        # Use if_test logic (Modern Qiskit)
        with self.circuit.if_test((self.circuit.clbits[m], 1)):
            self.circuit.x(j)
        with self.circuit.if_test((self.circuit.clbits[i], 1)):
            self.circuit.z(j)

    def measure(self, i_list):
        self.circuit.measure(i_list, i_list)

    def simulate(self, shot=1024):
        # Transpile specifically for the backend
        transpiled_circuit = transpile(self.circuit, self.backend)
        
        # Run job
        job = self.backend.run(transpiled_circuit, shots=shot)
        
        result = job.result()
        counts = result.get_counts()
        
        marginals = [marginal_counts(counts, [i]) for i in range(9)]
        return marginals

    def check_measure(self, i):
        for instruction in self.circuit.data:
            if instruction.operation.name == 'measure':
                try:
                    measured_qubit_index = self.circuit.find_bit(instruction.qubits[0]).index
                    if measured_qubit_index == i:
                        return "measured"
                except:
                    continue
        return "not measured"

def instruction(input_seq, backend):
    qc = Qtic(backend)
    for item in input_seq:
        cmd = item[0]
        if cmd == "cnot":
            qc.cnot(item[1], item[2])
        elif cmd == "hadamard":
            qc.hadamard(item[1])
        elif cmd == "sigmaz":
            qc.pauliz(item[1])
        elif cmd == "swap":
            qc.swap(item[1], item[2])
        elif cmd == "teleport": 
            qc.teleportation(item[1], item[2], 10)
        elif cmd == "measure": 
            qc.measure([item[1]])
        elif cmd == "force":
            # Force a qubit to a specific state (0 or 1)
            target_qubit = item[1]
            forced_value = item[2]
            qc.circuit.reset(target_qubit)
            if forced_value == 1:
                qc.circuit.x(target_qubit)
            
    return qc

def get_the_final_state(marginals):
    record = []
    for item in marginals:
        zeros = item.get('0', 0)
        ones = item.get('1', 0)
        if ones > zeros:
            record.append(1)
        else:
            record.append(0)
    return record

def get_measured_qubit(quantum_board):
    result = []
    for i in range(9):
        if quantum_board.check_measure(i) == "measured":
            result.append(i)
    return result

def extract_measured_states(full_state_record, measured_indices):
    result = {}
    for index in measured_indices:
        result[str(index)] = full_state_record[index]
    return result