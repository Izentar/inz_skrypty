import experiments as experiments # ustawia główny folder

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
    sf.StaticData.TEST_MODE = True

    metadata = sf.Metadata(testFlag=True, trainFlag=True, debugInfo=True)
    dataMetadata = dc.DefaultData_Metadata(pin_memoryTest=True, pin_memoryTrain=True, epoch=1, fromGrayToRGB=False)

    #####################
    types = ('predefModel', 'CIFAR10', 'disabled')

    try:
        stats = []
        for r in range(5):
            obj = models.alexnet()
            metadata.resetOutput()
            smoothingMetadata = dc.DisabledSmoothing_Metadata()
            
            modelMetadata = dc.DefaultModel_Metadata()

            stat=dc.run(numbOfRepetition=1,modelType=types[0], dataType=types[1], smoothingType=types[2], metadataObj=metadata, 
                modelMetadata=modelMetadata, dataMetadata=dataMetadata, smoothingMetadata=smoothingMetadata, modelPredefObj=obj, 
                rootFolder="cifar10")

            stats.append(stat)

        experiments.printStats(stats, metadata)
    except Exception as ex:
        experiments.printException(ex, types)