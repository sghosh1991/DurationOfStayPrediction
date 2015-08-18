# Clickstream Analysis: KDD Cup 2000
# The decision tree algorithm implemented is described here 
# http://www-users.cs.umn.edu/~kumar/dmbook/ch4.pdf
import math
import time
import random

ARRAY_1D = 1
ARRAY_2D = 2

counter = 0

import sys
chi = float(sys.argv[1])
#print chi
if chi == 0.01:
    chi_score = 6.65
elif chi == 0.05:
    chi_score = 3.85
elif chi == 1:
    chi_score = 0
else:
    print 'Please specify proper threshold (0.01, 0.05, 1)'
    sys.exit()

class Tree:
    def __init__(self, attribute, attr_value, left, right, label):
        self.attribute = attribute
        self.attr_value = attr_value
        self.left      = left
        self.right     = right
        self.label     = label

    def label_node(self, data, results):

        if results.count(1) >= results.count(0):
            #counter += 1
            #print counter
            return 1
        else:
            return 0
class Click:
    def __init__(self, trainfeat, trainlabs, testfeat, testlabs):
        before = time.time()
        self.trainfeat = self.read_file(trainfeat)

        self.trainfeat = self.make_array(self.trainfeat, ARRAY_2D)

        self.trainlabs  = self.read_file(trainlabs)
        self.trainlabs  = self.make_array(self.trainlabs, ARRAY_1D)
        
        self.testfeat = self.read_file(testfeat)
        self.testfeat = self.make_array(self.testfeat, ARRAY_2D)
        
        self.testlabs  = self.read_file(testlabs)
        self.testlabs  = self.make_array(self.testlabs, ARRAY_1D)

        after = time.time()
        #print "Time", after-before
        #self.under_sample(self.trainfeat, self.trainlabs)
    
    def under_sample(self, data, results):
        print "Length is(Before) ", len(data), len(results)
        trim = []
        for i, val in enumerate(results):
            if val == 0:
                trim.append(i)
        
        for i in xrange(25000):
            trim.remove(random.choice(trim))
        
        print len(trim)
        trim.sort(reverse=True)
        
        for i in trim:
            try:
                del data[i]
                del results[i]
            except Exception:
                print i
        print "Length is(After) ", len(data), len(results)
    
    def over_sample(self, data, results):
        for i, val in enumerate(results):
            if val == 1:
                data.append(data[i])
    
    def read_file(self, filename):
        with open(filename, "r") as f:
            return f.read()
        #lines = [i for i in open(filename) if i[:-1]]
        #return lines

    def find_mean(self, data, attr_index):
        total = 0
        for data_arr in data:
            total += data_arr[attr_index]
        return total/len(data)

    def median(self, lst):
        sortedLst = sorted(lst)
        lstLen = len(lst)
        index = (lstLen - 1) // 2
    
        if (lstLen % 2):
            return sortedLst[index]
        else:
            return (sortedLst[index] + sortedLst[index + 1])/2.0
    def find_median(self, data, attr_index):
        try:
            total = []
            for data_arr in data:
                total.append(data_arr[attr_index])
            return self.median(total)
        except Exception:
            print data_arr, attr_index
    
    def stopping_condition(self, data, results, attr_list):
        # If all attributes are explored, we need to stop growing the tree
        if attr_list.count(0) == 0:
            return 1
        len_results = len(results)

        #If it is a pure set, we have to stop growing the tree
        if ( results.count(0) == len_results or
             results.count(1) == len_results ):
            return 1
        
        return 0
    def find_true_median(self, data, attr_index):
        unique = set()
        for data_arr in data:
            unique.add(data_arr[attr_index])
        
        return self.median(unique)
        
    def attribute_value(self, data, results, attr):
        return self.find_median(data, attr)
        #return self.find_true_median(data, attr)
        #return self.find_mean(data, attr)
    
    def create_node(self):
        return Tree(-1, -1, None, None, -1)
    
    def get_entropy(self, results):
        # Pure subset
        if len(results) == 0:
            return 0
        
        p_yes = float(results.count(1))/len(results)
        p_no  = float(results.count(0))/len(results)
        
        # Pure subset
        if p_yes == 0 or p_no == 0:
            return 0
        
        entropy = -p_yes*math.log(p_yes, 2) -p_no*math.log(p_no, 2)
        
        return entropy
      
    def get_best_attr_to_split(self, data, results, attr_list):
        entropy = self.get_entropy(results)
        info_gain = 0
        final_index = -1
        
        for attr_index, attr_explored in enumerate(attr_list):
            # If attribute not explored yet
            if not attr_explored :
                attr_value = self.attribute_value(data, results, attr_index)
                #print "Attr Value", attr_value
                data_true, results_greater = self.filter_data(data, results, attr_index, attr_value,"Greater")
                data_false, results_lesser = self.filter_data(data, results, attr_index, attr_value, "Lesser")
                entropy_greater = self.get_entropy(results_greater)
                entropy_lesser  = self.get_entropy(results_lesser)
                entropy_attr = (float(len(results_greater))/len(results)) * entropy_greater + \
                               (float(len(results_lesser))/len(results)) * entropy_lesser
                if entropy_attr == 0:
                    # Pure set. Max gain
                    #print 'Max Gain'
                    info_gain = entropy
                    final_index = attr_index
                    break
                info_gain_attr = entropy - entropy_attr
                if info_gain_attr >= info_gain:
                    info_gain = info_gain_attr
                    final_index = attr_index
        
        return final_index
                    
    def filter_data(self, data, results, attr_index, attr_value, true_false, just_length=False ):
        filt_data = []
        filt_result = []
        
        if just_length:
            length = 0
        for i,data_arr in enumerate(data):
            if true_false == "Greater" :
                if data_arr[attr_index] >= attr_value:
                    if just_length:
                        length += 1
                    filt_data.append(data_arr)
                    filt_result.append(results[i])
            elif true_false == "Lesser" :
                if data_arr[attr_index] < attr_value:
                    if just_length:
                        length += 1
                    filt_data.append(data_arr)
                    filt_result.append(results[i])
        if just_length:
            return length
        
        return filt_data, filt_result
    
    def attribute_irrelevant(self, data, results, attr_index, attr_value, chi_score=6.65):
        N = float(len(results))
        n_yes = float(results.count(1))
        n_no  = float(results.count(0))
        
            
        data_true, T1 = self.filter_data(data, results, attr_index, attr_value,"Greater")
        data_false, T2 = self.filter_data(data, results, attr_index, attr_value, "Lesser")
        
        n_yes_expect_greater = n_yes * len(T1)/N
        n_no_expect_greater  = n_no *len(T1)/N
        
        n_yes_expect_lesser = n_yes * len(T2)/N
        n_no_expect_lesser  = n_no *len(T2)/N
        if n_yes_expect_greater == 0 or n_no_expect_greater == 0 or n_yes_expect_lesser == 0 or n_no_expect_lesser == 0:
            S = float('+inf')
        else:            
            S = (n_yes_expect_greater - T1.count(1))**2/n_yes_expect_greater + (n_no_expect_greater - T1.count(0))**2/n_no_expect_greater \
                + (n_yes_expect_lesser - T2.count(1))**2/n_yes_expect_lesser + (n_no_expect_lesser - T2.count(0))**2/n_no_expect_lesser
        #print "Chi Sqaure Value ", S
        if S < chi_score: # Threshold = 0.01, Degrees of Freedom = 1, Chi Score = 6.65
        #if S  < 3.85:    # Threshold = 0.05, Degrees of Freedom = 1, Chi Score = 3.85
        #if S  < 0:       # Threshold = 1,    Degrees of Freedom = 1, Chi Score = 0.00
            return True
        else:
            return False
            
    def build_tree(self, data, results, attr_list ):
        global counter
        global chi_score
        
        if self.stopping_condition(data, results, attr_list):
            leaf_node = self.create_node()
            leaf_node.label = leaf_node.label_node(data, results)
            counter += 1
            return leaf_node
        else:
            root = self.create_node()
            counter += 1
            root.attribute = self.get_best_attr_to_split(data, results, attr_list)
            root.attr_value = self.attribute_value(data, results, root.attribute)
            #print root.attribute
            attr_list[root.attribute] = 1
            # If the node doesn't meet the chi-sqaure criterion, stop growing the tree
            if self.attribute_irrelevant(data, results, root.attribute, root.attr_value, chi_score):
                root.label = root.label_node(data, results)
                return root
            
            data_true, results_true = self.filter_data(data, results, root.attribute, root.attr_value,"Greater")
            data_false, results_false = self.filter_data(data, results, root.attribute, root.attr_value, "Lesser")
            
            root.left = self.build_tree(data_true, results_true, attr_list[:])
            root.right = self.build_tree(data_false, results_false, attr_list[:])
            return root

    def make_1D_array(self, string):
        #print type(string), string
        array = [int(x) for x in string.split()]
        return array
    def make_array(self, string, arr_type):
        if arr_type == ARRAY_1D:
            return self.make_1D_array(string)
        else:
            array_2D = []
            for array in string.split('\n'):
                array_2D.append(self.make_1D_array(array))

            return array_2D
    def classify_new_data(self, tree, data_arr):
        try:
            while tree.label == -1:
                if data_arr[tree.attribute] >= tree.attr_value:
                    tree = tree.left
                else:
                    tree = tree.right
            return tree.label
        except Exception:
            print tree.attribute, data_arr
    
    def classify(self, tree, data):
        classified_data = []
        
        for  data_arr in data:
            classified_data.append(self.classify_new_data(tree, data_arr))
        return classified_data
    def compare(self, arr1, arr2):
        correct = 0
        wrong = 0
        for i in xrange(len(arr1)):
            if arr1[i] == arr2[i]:
                correct += 1
            else:
                wrong += 1
        return correct, wrong
    
before = time.time()

c = Click("trainfeat.csv", "trainlabs.csv", "testfeat.csv", "testlabs.csv")
#c = Click("trainfeat.csv", "trainlabs.csv", "trainfeat.csv", "trainlabs.csv")


# Create a list of attributes
attr = [0 for x in xrange(len(c.trainfeat[0]))]

#import sys
#sys.setrecursionlimit(10000) # 10000 is an example, try with different values

tree = c.build_tree(c.trainfeat, c.trainlabs, attr)
#print 'build tree done'

results = c.classify(tree, c.testfeat)
print 'Number of Ones = ', results.count(1)
print 'Number of Zeroes =', results.count(0)
print 'Number of nodes in Tree =', counter
correct, wrong = c.compare(results, c.testlabs)


print "Correct Predictions =", correct
print "Total Predictions = ", correct+wrong
print 'Percentage = ', (float(correct)/(correct+wrong))*100

after = time.time()
print 'Total Run Time: ', after-before

counter = 0
def in_order(tree):
    global counter
    if tree.label != -1:
        print tree.label,
        counter +=1
        return
    in_order(tree.left)
    counter += 1
    print tree.label,
    in_order(tree.right)

