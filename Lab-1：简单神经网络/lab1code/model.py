import numpy as np

# Neural network class
class neuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate=0.01):
        """
        Neural network with 5 fully-connected layers, including:
        input layer, 4 hidden layers and output layer.
        """
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        self.lr = learning_rate  # Learning rate

        # Initialize the weights with He initialization， which is suitable for ReLU activation function
        self.wih1 = np.random.randn(self.hidden_nodes, self.input_nodes) * np.sqrt(2 / self.input_nodes)
        self.wh1h2 = np.random.randn(self.hidden_nodes, self.hidden_nodes) * np.sqrt(2 / self.hidden_nodes)
        self.wh2h3 = np.random.randn(self.hidden_nodes, self.hidden_nodes) * np.sqrt(2 / self.hidden_nodes)
        self.wh3h4 = np.random.randn(self.hidden_nodes, self.hidden_nodes) * np.sqrt(2 / self.hidden_nodes)
        self.wh4h5 = np.random.randn(self.hidden_nodes, self.hidden_nodes) * np.sqrt(2 / self.hidden_nodes)
        self.wh5o = np.random.randn(self.output_nodes, self.hidden_nodes) * np.sqrt(2 / self.hidden_nodes)

        # ReLU activation function
        self.activation_function = lambda x: np.maximum(0, x)

    def forward(self, input_feature):
        """
        Forward pass through the network
        """
        self.inputs = np.array(input_feature, ndmin=2).T

        hidden_inputs_1 = np.dot(self.wih1, self.inputs)
        self.hidden_outputs_1 = self.activation_function(hidden_inputs_1)

        hidden_inputs_2 = np.dot(self.wh1h2, self.hidden_outputs_1)
        self.hidden_outputs_2 = self.activation_function(hidden_inputs_2)

        hidden_inputs_3 = np.dot(self.wh2h3, self.hidden_outputs_2)
        self.hidden_outputs_3 = self.activation_function(hidden_inputs_3)

        hidden_inputs_4 = np.dot(self.wh3h4, self.hidden_outputs_3)
        self.hidden_outputs_4 = self.activation_function(hidden_inputs_4)

        hidden_inputs_5 = np.dot(self.wh4h5, self.hidden_outputs_4)
        self.hidden_outputs_5 = self.activation_function(hidden_inputs_5)

        final_inputs = np.dot(self.wh5o, self.hidden_outputs_5)
        self.final_outputs = self.activation_function(final_inputs)

    def backpropagation(self, targets_list):
        """
        Backpropagate the error and update the weights
        """
        targets = np.array(targets_list, ndmin=2).T
        loss = np.sum(np.square(self.final_outputs - targets)) / 2

        output_errors = self.final_outputs - targets

        hidden_errors_5 = np.dot(self.wh5o.T, output_errors)
        hidden_errors_4 = np.dot(self.wh4h5.T, hidden_errors_5)
        hidden_errors_3 = np.dot(self.wh3h4.T, hidden_errors_4)
        hidden_errors_2 = np.dot(self.wh2h3.T, hidden_errors_3)
        hidden_errors_1 = np.dot(self.wh1h2.T, hidden_errors_2)

        # Update weights using gradient descent with momentum
        self.wh5o -= self.lr * np.dot((output_errors * (self.final_outputs > 0)), np.transpose(self.hidden_outputs_5))
        self.wh4h5 -= self.lr * np.dot((hidden_errors_5 * (self.hidden_outputs_5 > 0)), np.transpose(self.hidden_outputs_4))
        self.wh3h4 -= self.lr * np.dot((hidden_errors_4 * (self.hidden_outputs_4 > 0)), np.transpose(self.hidden_outputs_3))
        self.wh2h3 -= self.lr * np.dot((hidden_errors_3 * (self.hidden_outputs_3 > 0)), np.transpose(self.hidden_outputs_2))
        self.wh1h2 -= self.lr * np.dot((hidden_errors_2 * (self.hidden_outputs_2 > 0)), np.transpose(self.hidden_outputs_1))
        self.wih1 -= self.lr * np.dot((hidden_errors_1 * (self.hidden_outputs_1 > 0)), np.transpose(self.inputs))

        return loss
