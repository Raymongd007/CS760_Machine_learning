import weka.core
import weka.core.converters
import weka.core.dataset
import weka.core.jvm as jvm
import numpy as np
jvm.start()

#load arff file
filename = "test.arff"
dataset = weka.core.converters.load_any_file(filename)
dataset.class_is_last()
print("loading complete")
print("number of instances: " + str(dataset.num_instances))
print("number of attributes: " + str(dataset.num_attributes))

#get the i th instance from training set
i = 2 #suppose i=2
instance = dataset.get_instance(i - 1)

#print attributes of the instance
print(instance.values) 
print(type(instance.values)) #instance.values has the type of numpy array


jvm.stop()
import weka.core
import weka.core.converters
import weka.core.dataset
import weka.core.jvm as jvm
import numpy as np
jvm.start()

#load arff file
filename = "test.arff"
dataset = weka.core.converters.load_any_file(filename)
dataset.class_is_last()
print("loading complete")
print("number of instances: " + str(dataset.num_instances))
print("number of attributes: " + str(dataset.num_attributes))

#get the i th instance from training set
i = 2 #suppose i=2
instance = dataset.get_instance(i - 1)

#print attributes of the instance
print(instance.values) 
print(type(instance.values)) #instance.values has the type of numpy array


jvm.stop()
