from torch.nn import Linear, ReLU, Tanh, Module

input_size = 2 * 14
hidden_size = 16
output_size = 14 * 3

class MotorControl(Module):
    def __init__(self):
        super(MotorControl, self).__init__()
        self.fc1 = Linear(input_size , hidden_size)
        self.relu1 = ReLU()
        self.fc2 = Linear(hidden_size, output_size)
        self.tanh = Tanh()

    def forward(self, x):
        x = self.relu1(self.fc1(x))
        x = self.tanh(self.fc2(x))
        return x

if __name__ == "__main__":
    net = MotorControl() 
    print(net)