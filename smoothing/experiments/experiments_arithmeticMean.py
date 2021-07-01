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
    #sf.StaticData.TEST_MODE = True

    metadata = sf.Metadata(testFlag=True, trainFlag=True, debugInfo=True)
    dataMetadata = dc.DefaultData_Metadata(pin_memoryTest=True, pin_memoryTrain=True, epoch=1, fromGrayToRGB=False)
    loop = 3

    #####################
    types = ('predefModel', 'CIFAR10', 'generalizedMean')
    try:
        stats = []
        rootFolder = sf.Output.getTimeStr() +  ''.join(x + "_" for x in types) + "set"
        for r in range(loop):
            obj = models.alexnet()
            metadata.resetOutput()
            smoothingMetadata = dc.DefaultSmoothingOscilationGeneralizedMean_Metadata(epsilon=1e-4, hardEpsilon=1e-7, weightsEpsilon=1e-6)
            
            modelMetadata = dc.DefaultModel_Metadata()

            stat=dc.run(numbOfRepetition=7,modelType=types[0], dataType=types[1], smoothingType=types[2], metadataObj=metadata, 
                modelMetadata=modelMetadata, dataMetadata=dataMetadata, smoothingMetadata=smoothingMetadata, modelPredefObj=obj,
                rootFolder=rootFolder)
            stats.append(stat.pop()) # weź pod uwagę tylko ostatni wynik (najlepiej wyćwiczony)
            for i in stat: # stwórz wykresy dla pozostałych
                i.printPlots(startAt=-10)
        experiments.printStats(stats, metadata)
    except Exception as ex:
        experiments.printException(ex, types)


    #####################
    types = ('predefModel', 'CIFAR10', 'generalizedMean')
    try:
        stats = []
        rootFolder = sf.Output.getTimeStr() +  ''.join(x + "_" for x in types) + "set"
        for r in range(loop):
            obj = models.alexnet()
            metadata.resetOutput()

            smoothingMetadata = dc.DefaultSmoothingOscilationGeneralizedMean_Metadata(epsilon=1e-4*5, hardEpsilon=1e-7*5, weightsEpsilon=1e-6*5)
            modelMetadata = dc.DefaultModel_Metadata()

            stat=dc.run(numbOfRepetition=3,modelType=types[0], dataType=types[1], smoothingType=types[2], metadataObj=metadata, 
                modelMetadata=modelMetadata, dataMetadata=dataMetadata, smoothingMetadata=smoothingMetadata, modelPredefObj=obj,
                rootFolder=rootFolder)
            stats.append(stat.pop()) # weź pod uwagę tylko ostatni wynik (najlepiej wyćwiczony)
            for i in stat: # stwórz wykresy dla pozostałych
                i.printPlots(startAt=-10)
        experiments.printStats(stats, metadata)
    except Exception as ex:
        experiments.printException(ex, types)

    #####################
    types = ('predefModel', 'CIFAR10', 'generalizedMean')
    try:
        stats = []
        rootFolder = sf.Output.getTimeStr() +  ''.join(x + "_" for x in types) + "set"
        for r in range(loop):
            obj = models.alexnet()
            metadata.resetOutput()
            
            smoothingMetadata = dc.DefaultSmoothingOscilationGeneralizedMean_Metadata(epsilon=1e-3, hardEpsilon=1e-6, weightsEpsilon=1e-5)
            modelMetadata = dc.DefaultModel_Metadata()

            stat=dc.run(numbOfRepetition=3,modelType=types[0], dataType=types[1], smoothingType=types[2], metadataObj=metadata, 
                modelMetadata=modelMetadata, dataMetadata=dataMetadata, smoothingMetadata=smoothingMetadata, modelPredefObj=obj,
                rootFolder=rootFolder)
            stats.append(stat.pop()) # weź pod uwagę tylko ostatni wynik (najlepiej wyćwiczony)
            for i in stat: # stwórz wykresy dla pozostałych
                i.printPlots(startAt=-10)
        experiments.printStats(stats, metadata)
    except Exception as ex:
        experiments.printException(ex, types)

    #####################
    types = ('predefModel', 'CIFAR10', 'generalizedMean')
    try:
        stats = []
        rootFolder = sf.Output.getTimeStr() +  ''.join(x + "_" for x in types) + "set"
        for r in range(loop):
            obj = models.alexnet()
            metadata.resetOutput()
            
            smoothingMetadata = dc.DefaultSmoothingOscilationGeneralizedMean_Metadata(epsilon=1e-5, hardEpsilon=1e-8, weightsEpsilon=1e-7)
            modelMetadata = dc.DefaultModel_Metadata()

            stat=dc.run(numbOfRepetition=3,modelType=types[0], dataType=types[1], smoothingType=types[2], metadataObj=metadata, 
                modelMetadata=modelMetadata, dataMetadata=dataMetadata, smoothingMetadata=smoothingMetadata, modelPredefObj=obj,
                rootFolder=rootFolder)
            stats.append(stat.pop()) # weź pod uwagę tylko ostatni wynik (najlepiej wyćwiczony)
            for i in stat: # stwórz wykresy dla pozostałych
                i.printPlots(startAt=-10)
        experiments.printStats(stats, metadata)
    except Exception as ex:
        experiments.printException(ex, types)