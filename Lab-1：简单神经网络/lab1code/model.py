import numpy as np


# neural network class
class neuralNetwork:

    # initialize the neural network
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate=0.1):
        """
        The network consists of these kinds of layer:
        input layer, hidden layers and output layer.
        Here defined these layers.
        :param input_nodes: dimension of input
        :param hidden_nodes: dimension of hidden nodes
        :param output_nodes: dimension of output
        :param learning_rate: the learning rate of neural network
        """
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        self.inputs = None  # input data
        self.hidden_outputs_1 = None
        self.hidden_outputs_2 = None
        self.hidden_outputs_3 = None
        self.hidden_outputs_4 = None
        self.hidden_outputs_5 = None
        self.final_outputs = None  # the output of output layer
        self.lr = learning_rate  # learning rate

        """
        The network contains three full-connected layer, 
        so the network contains five layers in total.
        """
        # init the weight of layers
        self.wih1 = np.random.normal(0.0, pow(self.input_nodes, -0.5) * 0.1,
                                     (self.hidden_nodes, self.input_nodes))
        self.wh1h2 = np.random.normal(0.0, pow(self.input_nodes, -0.5) * 0.1,
                                     (self.hidden_nodes, self.hidden_nodes))
        self.wh2h3 = np.random.normal(0.0, pow(self.input_nodes, -0.5) * 0.1,
                                      (self.hidden_nodes, self.hidden_nodes))
        self.wh3h4 = np.random.normal(0.0, pow(self.input_nodes, -0.5) * 0.1,
                                      (self.hidden_nodes, self.hidden_nodes))
        self.wh4h5 = np.random.normal(0.0, pow(self.input_nodes, -0.5) * 0.1,
                                      (self.hidden_nodes, self.hidden_nodes))
        self.wh5o = np.random.normal(0.0, pow(self.input_nodes, -0.5) * 0.1,
                                      (self.output_nodes, self.hidden_nodes))
        self.activation_function = lambda x: 1. / (1 + np.exp(-x))

    def forward(self, input_feature):
        """
        Forward the neural network
        :param input_feature: single input image, flattened [784, ]
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
        Propagate backwards
        :param targets_list: output onehot code of a single image, [10, ]
        """
        targets = np.array(targets_list, ndmin=2).T
        loss = np.sum(np.square(self.final_outputs - targets)) / 2

        # 输出层的误差
        output_errors = self.final_outputs - targets

        # 反向传播误差并更新权重
        hidden_errors_5 = np.dot(self.wh5o.T, output_errors)
        hidden_errors_4 = np.dot(self.wh4h5.T, hidden_errors_5)
        hidden_errors_3 = np.dot(self.wh3h4.T, hidden_errors_4)
        hidden_errors_2 = np.dot(self.wh2h3.T, hidden_errors_3)
        hidden_errors_1 = np.dot(self.wh1h2.T, hidden_errors_2)

        # 更新权重：采用梯度下降法
        self.wh5o -= self.lr * np.dot((output_errors * self.final_outputs * (1.0 - self.final_outputs)),
                                      np.transpose(self.hidden_outputs_5))

        self.wh4h5 -= self.lr * np.dot((hidden_errors_5 * self.hidden_outputs_5 * (1.0 - self.hidden_outputs_5)),
                                       np.transpose(self.hidden_outputs_4))

        self.wh3h4 -= self.lr * np.dot((hidden_errors_4 * self.hidden_outputs_4 * (1.0 - self.hidden_outputs_4)),
                                       np.transpose(self.hidden_outputs_3))

        self.wh2h3 -= self.lr * np.dot((hidden_errors_3 * self.hidden_outputs_3 * (1.0 - self.hidden_outputs_3)),
                                       np.transpose(self.hidden_outputs_2))

        self.wh1h2 -= self.lr * np.dot((hidden_errors_2 * self.hidden_outputs_2 * (1.0 - self.hidden_outputs_2)),
                                       np.transpose(self.hidden_outputs_1))

        self.wih1 -= self.lr * np.dot((hidden_errors_1 * self.hidden_outputs_1 * (1.0 - self.hidden_outputs_1)),
                                      np.transpose(self.inputs))

        return loss
