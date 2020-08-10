import torch as T
import torch.nn.functional as F
import torch.autograd as AG


class ConvolutionNeuralNetwork(T.nn.Module):
    def __init__(self, param1, param2): # parameters here
        super(ConvolutionNeuralNetwork, self).__init__()
        # all declarations here

    def forward(self, in1, in2): # all Inputs here
        # all functional stuff here
        this.featureMatrix = Input()
        this.conv2d = F.conv2d(this.featureMatrix)
        this.a_BatchNormalization1 = F.batch_norm(this.conv2d)
        this.a_RectifiedLinearUnit1 = F.relu(this.a_BatchNormalization1)
        this.maxPool2d = F.max_pool2d(this.a_RectifiedLinearUnit1)
        this.out = Output(this.maxPool2d)
        
        return (out1, out2) # all Outputs here

class ConvolutionNeuralNetwork1(T.nn.Module):
    def __init__(self, param1, param2): # parameters here
        super(ConvolutionNeuralNetwork1, self).__init__()
        # all declarations here

    def forward(self, in1, in2): # all Inputs here
        # all functional stuff here
        this.convOutputAsInput = Input()
        this.conv2d = F.conv2d(this.convOutputAsInput)
        this.a_BatchNormalization2 = F.batch_norm(this.conv2d)
        this.a_RectifiedLinearUnit2 = F.relu(this.a_BatchNormalization2)
        this.maxPool2d = F.max_pool2d(this.a_RectifiedLinearUnit2)
        this.out = Output(this.maxPool2d)
        
        return (out1, out2) # all Outputs here

