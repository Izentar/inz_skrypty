import experiments as experiments

import torch
import torchvision
import torch.optim as optim
from framework import smoothingFramework as sf
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from framework import defaultClasses as dc

if(__name__ == '__main__'):
    #sf.StaticData.TEST_MODE = True

    #####################
    types = ('predefModel', 'CIFAR100', 'disabled')
    try:
        obj = models.alexnet()
        metadata = sf.Metadata(testFlag=True, trainFlag=True, debugInfo=True)
        dataMetadata = dc.DefaultData_Metadata(pin_memoryTest=True, pin_memoryTrain=True, fromGrayToRGB=False)
        
        smoothingMetadata = dc.DisabledSmoothing_Metadata()
        modelMetadata = dc.DefaultModel_Metadata()

        stat=dc.run(numbOfRepetition=5, modelType=types[0], dataType=types[1], smoothingType=types[2], metadataObj=metadata, 
            modelMetadata=modelMetadata, dataMetadata=dataMetadata, smoothingMetadata=smoothingMetadata, modelPredefObj=obj)
        experiments.printStats(stat, metadata)
    except Exception as ex:
        experiments.printException(ex, types)