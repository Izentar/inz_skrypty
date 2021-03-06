import experiments as experiments

import torch
import torchvision
import torch.optim as optim
import torch.optim.lr_scheduler as scheduler
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
import torchvision.models.resnet as modResnet
import torchvision.transforms as transforms

import matplotlib.pyplot as plt

from framework import smoothingFramework as sf
from framework import defaultClasses as dc

import torch.nn.init as init
from torch.autograd import Variable

import sys
import numpy as np

import torch.backends.cudnn as cudnn
import math

def conv3x3(in_planes, out_planes, stride=1):
    return nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=stride, padding=1, bias=True)

def conv_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        init.xavier_uniform_(m.weight, gain=np.sqrt(2))
        init.constant_(m.bias, 0)
    elif classname.find('BatchNorm') != -1:
        init.constant_(m.weight, 1)
        init.constant_(m.bias, 0)

class wide_basic(nn.Module):
    def __init__(self, in_planes, planes, dropout_rate, stride=1):
        super(wide_basic, self).__init__()
        self.bn1 = nn.BatchNorm2d(in_planes)
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=3, padding=1, bias=True)
        self.dropout = nn.Dropout(p=dropout_rate)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=True)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, planes, kernel_size=1, stride=stride, bias=True),
            )

    def forward(self, x):
        out = self.dropout(self.conv1(F.relu(self.bn1(x))))
        out = self.conv2(F.relu(self.bn2(out)))
        out += self.shortcut(x)

        return out

class Wide_ResNet(nn.Module):
    def __init__(self, depth, widen_factor, dropout_rate, num_classes):
        super(Wide_ResNet, self).__init__()
        self.in_planes = 16

        assert ((depth-4)%6 ==0), 'Wide-resnet depth should be 6n+4'
        n = (depth-4)/6
        k = widen_factor

        print('| Wide-Resnet %dx%d' %(depth, k))
        nStages = [16, 16*k, 32*k, 64*k]

        self.conv1 = conv3x3(3,nStages[0])
        self.layer1 = self._wide_layer(wide_basic, nStages[1], n, dropout_rate, stride=1)
        self.layer2 = self._wide_layer(wide_basic, nStages[2], n, dropout_rate, stride=2)
        self.layer3 = self._wide_layer(wide_basic, nStages[3], n, dropout_rate, stride=2)
        self.bn1 = nn.BatchNorm2d(nStages[3], momentum=0.9)
        self.linear = nn.Linear(nStages[3], num_classes)

    def _wide_layer(self, block, planes, num_blocks, dropout_rate, stride):
        strides = [stride] + [1]*(int(num_blocks)-1)
        layers = []

        for stride in strides:
            layers.append(block(self.in_planes, planes, dropout_rate, stride))
            self.in_planes = planes

        return nn.Sequential(*layers)

    def forward(self, x):
        out = self.conv1(x)
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = F.relu(self.bn1(out))
        out = F.avg_pool2d(out, 8)
        out = out.view(out.size(0), -1)
        out = self.linear(out)

        return out

# wzorowane na pracy https://paperswithcode.com/paper/wide-residual-networks
# model wzorowany na resnet18 https://github.com/huyvnphan/PyTorch_CIFAR10/blob/master/module.py

if(__name__ == '__main__'):
    def learning_rate(init, epoch):
        optim_factor = 0
        if(epoch > 160):
            optim_factor = 3
        elif(epoch > 120):
            optim_factor = 2
        elif(epoch > 60):
            optim_factor = 1

        return init*math.pow(0.2, optim_factor)

    transform_train = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.4914, 0.4822, 0.4465), std=(0.2023, 0.1994, 0.2010)),
    ]) # meanstd transformation

    trainset = torchvision.datasets.CIFAR10(root='~/.data', train=True, download=True, transform=transform_train)
    num_classes = 10

    trainloader = torch.utils.data.DataLoader(trainset, batch_size=128, shuffle=True, num_workers=2)


    net = Wide_ResNet(depth=28, widen_factor=10, dropout_rate=0.3, num_classes=num_classes)
    net.to(device="cuda:0")
    cudnn.benchmark = True

    criterion = nn.CrossEntropyLoss()

    def train(epoch):
        net.train()
        net.training = True
        train_loss = 0
        correct = 0
        total = 0
        optimizer = optim.SGD(net.parameters(), lr=learning_rate(0.1, epoch), momentum=0.9, weight_decay=5e-4)

        print('\n=> Training Epoch #%d, LR=%.4f' %(epoch, learning_rate(0.1, epoch)))
        for batch_idx, (inputs, targets) in enumerate(trainloader):
            inputs, targets = inputs.to(device="cuda:0"), targets.to(device="cuda:0") # GPU settings
            optimizer.zero_grad()
            inputs, targets = Variable(inputs), Variable(targets)
            outputs = net(inputs)               # Forward Propagation
            loss = criterion(outputs, targets)  # Loss
            loss.backward()  # Backward Propagation
            optimizer.step() # Optimizer update

            train_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += targets.size(0)
            correct += predicted.eq(targets.data).cpu().sum()

            sys.stdout.write('\r')
            sys.stdout.write('| Epoch [%3d/%3d] Iter[%3d/%3d]\t\tLoss: %.4f Acc@1: %.3f%%'
                    %(epoch, 200, batch_idx+1,
                        (len(trainset)//128)+1, loss.item(), 100.*correct/total))
            sys.stdout.flush()

    for epoch in range(200):
        train(epoch)
            
    """
if(__name__ == '__main__'):
    modelDevice = 'cuda:0'
    if(sf.test_mode().isActive()):
        modelDevice="cuda:0"

    metadata = sf.Metadata(testFlag=True, trainFlag=True, debugInfo=True)
    dataMetadata = dc.DefaultData_Metadata(pin_memoryTest=False, pin_memoryTrain=True, epoch=200, fromGrayToRGB=False,
        batchTrainSize=32, batchTestSize=100, startTestAtEpoch=[199, 200])
    optimizerDataDict={"learning_rate":0.1, "momentum":0.9, "weight_decay":0.0005}
    modelMetadata = dc.DefaultModel_Metadata(device=modelDevice, lossFuncDataDict={}, optimizerDataDict=optimizerDataDict)
    loop = 5
    modelName = "wide_resnet"
    prefix = "set_copyOfExper_"
    runningAvgSize = 10
    #num_classes = 10
    layers = [2, 2, 2, 2]
    block = modResnet.BasicBlock

    cudnn.benchmark = True


    types = ('predefModel', 'CIFAR10', 'disabled')
    try:
        stats = []
        rootFolder = prefix + sf.Output.getTimeStr() + ''.join(x + "_" for x in types)
        smoothingMetadata = dc.DisabledSmoothing_Metadata()

        for r in range(loop):

            transform_train = transforms.Compose([
                transforms.RandomCrop(32, padding=4),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
            ]) # meanstd transformation

            trainset = torchvision.datasets.CIFAR10(root='~/.data', train=True, download=True, transform=transform_train)
            num_classes = 10
            trainloader = torch.utils.data.DataLoader(trainset, batch_size=32, shuffle=True, num_workers=2)

            #########################################################################3
            #obj = models.ResNet(block, layers, num_classes=num_classes)
            obj = Wide_ResNet(depth=28, widen_factor=10, dropout_rate=0.3, num_classes=num_classes)
            obj.apply(conv_init)

            #data = dc.DefaultDataCIFAR10(dataMetadata)
            model = dc.DefaultModelPredef(obj=obj, modelMetadata=modelMetadata, name=modelName)
            #smoothing = dc.DisabledSmoothing(smoothingMetadata)
            model.getNNModelModule().to(device="cuda:0")

            optimizer = optim.SGD(model.getNNModelModule().parameters(), lr=optimizerDataDict['learning_rate'], 
                weight_decay=optimizerDataDict['weight_decay'], momentum=optimizerDataDict['momentum'])
            scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=60, gamma=0.2)
            loss_fn = nn.CrossEntropyLoss()     

            '''stat=dc.run(metadataObj=metadata, data=data, model=model, smoothing=smoothing, optimizer=optimizer, lossFunc=loss_fn,
                modelMetadata=modelMetadata, dataMetadata=dataMetadata, smoothingMetadata=smoothingMetadata, rootFolder=rootFolder,
                schedulers=[([60, 120, 160], scheduler)])'''

            for epoch in range(200):
                model.getNNModelModule().train()
                model.getNNModelModule().training = True

                model.getNNModelModule().train()
                model.getNNModelModule().training = True
                train_loss = 0
                correct = 0
                total = 0
                optimizer = optim.SGD(model.getNNModelModule().parameters(), lr=0.1, momentum=0.9, weight_decay=5e-4)

                print('\n=> Training Epoch #%d, LR=%.4f' %(epoch, 0.1))
                for batch_idx, (inputs, targets) in enumerate(trainloader):
                    inputs, targets = inputs.to(device="cuda:0"), targets.to(device="cuda:0") # GPU settings
                    optimizer.zero_grad()
                    outputs = model.getNNModelModule()(inputs)               # Forward Propagation
                    loss = loss_fn(outputs, targets)  # Loss
                    loss.backward()  # Backward Propagation
                    optimizer.step() # Optimizer update

                    train_loss += loss.item()
                    _, predicted = torch.max(outputs.data, 1)
                    total += targets.size(0)
                    correct += predicted.eq(targets.data).cpu().sum()

                    print('\r')
                    print('| Epoch [%3d/%3d] Iter[%3d/%3d]\t\tLoss: %.4f Acc@1: %.3f%%'
                            %(epoch, 200, batch_idx+1,
                                (len(trainset)//32)+1, loss.item(), 100.*correct/total))
                    sys.stdout.flush()

            #stat.saveSelf(name="stat")

            #stats.append(stat)
        #experiments.printAvgStats(stats, metadata, runningAvgSize=runningAvgSize)
    except Exception as ex:
        experiments.printException(ex, types)
"""