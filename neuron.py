import random
from muscle import Muscle
import dill


def relu(x):
    return max(0, x)

def sigmoid(x):
    return 1 / (1 + 2.71828 ** -x)

def tanh(x):
    return (2 / (1 + 2.71828 ** (-2 * x))) - 1

def binary(x):
    return 1 if x > 0 else 0


class NeuronParameters:
    def __init__(self, num_inputs, activation_function=lambda x: x, bias=True):
        self.num_inputs = num_inputs
        self.weights = [2 * random.random() - 1 for i in range(num_inputs)]
        self.biases = [2 * random.random() - 1 for i in range(num_inputs)] if bias else [0 for i in range(num_inputs)]
        self.activation_function = activation_function

    def __repr__(self):
        return str(self.weights) + "\n" + str(self.biases)

    def save(self, filename):
        with open(filename, "wb") as f:
            dill.dump(self, f)
        
    @staticmethod
    def load(filename):
        with open(filename, "rb") as f:
            return dill.load(f)

class Neuron:
    def __init__(self, parameters, inputs=None):
        self.activation = 0
        self.temp_activation = 0
        self.parameters = parameters

        if inputs == None:
            self.inputs = []
        else:
            self.inputs = inputs

    def __repr__(self):
        return f"Activation: {self.activation}\nParameters: {self.parameters}\n"

    def calc_activation(self):
        if self.parameters.num_inputs != len(self.inputs):
            raise Exception("Number of inputs does not match number of weights")

        self.temp_activation = 0
        for i in range(len(self.inputs)):
            self.temp_activation += self.inputs[i].activation * self.parameters.weights[i] + self.parameters.biases[i]
        self.temp_activation = self.parameters.activation_function(self.temp_activation)

        return self.temp_activation

    def update_activation(self):
        self.activation = self.temp_activation

class MotorNeuron(Neuron):
    def __init__(self, muscle, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.muscle = muscle
    
    def update_activation(self):
        self.activation = self.temp_activation
        self.muscle.set_activation(self.activation)


if __name__ == "__main__":
    n1 = Neuron(NeuronParameters(2, activation_function=relu))
    n2 = Neuron(NeuronParameters(2))
    n3 = Neuron(NeuronParameters(2))

    n1.inputs = [n2, n3]
    n2.inputs = [n1, n3]
    n3.inputs = [n1, n2]

    n1.calc_activation()
    n1.update_activation()

    print(n1)

 