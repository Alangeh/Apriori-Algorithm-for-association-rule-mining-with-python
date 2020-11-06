##################################################################
######### Apriori Algorithm For Association Rule Mining ##########
################# By Lionel Ngobesing Alangeh ####################
##################################################################
import csv

###########################################################################
##  Introduction

##  Prompt user to enter the minimum support and minimum confidence parameters
minsup = int(input("Enter Minimum support value in %: "))
minconf = int(input("Enter Minimum confidence value in %: "))

#Compute frequent 1-itemset for candidates
#initialize variables
Candidate_dict1 = {} #candidate dictionary
transactions = 0 #transaction.count
Dataset = []
Transaction_arr = []

#Read dataset file and print out
with open("dataset.csv", 'r') as file:
    reader = csv.reader(file, delimiter=',')
    for line in reader:
        Transaction_arr = []
        transactions += 1
        for word in line:
            Transaction_arr.append(word)
            if word not in Candidate_dict1.keys():  # loop through to create different transaction arrays of dataset
                Candidate_dict1[word] = 1
            else:
                Candidate_dict1[word] = Candidate_dict1[word] + 1
        Dataset.append(Transaction_arr)

#####################################################################
#### use this portion if file is in txt format
"""
with open ("dataset.txt", "r") as f:
    for line in file:
        Transaction_arr = []
        transactions += 1
        for word in line.split():
            Transaction_arr.append(word)
            if word not in Candidate_dict1.keys(): #loop through to create different transaction arrays of dataset
                Candidate_dict1[word] = 1
            else:
                Candidate_dict1[word] = Candidate_dict1[word] + 1
        Dataset.append(Transaction_arr) #add to dataset array
"""
"""
###############################################################################
##Function to print output to a file / can use if needed
def print_to_file(content):
    file = open("Output.txt", "a+")
    file.write(str(content))
###############################################################################
"""

print("********************** The TEST DATA SET **************************")
print(Dataset)
print("*******************************************************************")

#Now compute Frequent 1-itemset
Freq_1_itemset = []
for key in Candidate_dict1:
    if (100 * Candidate_dict1[key] / transactions) >= minsup:
        list = []
        list.append(key) #get keys from dictionary with value greater than minsup and add to list
        Freq_1_itemset.append(list) #add this list to frequent item set array

print("********************** FREQUENT 1-ITEMSET *************************")
print(Freq_1_itemset)
print("*******************************************************************")


###########################################################################################
###########################################################################################
## The Apriori generater function to compute candidate k-itemset (freq_k) using frequent (k-1)-itemset (freq_k_1)
def apriori_gen(freq_k_1, k):
    length = k
    freq_k = []
    for list1 in freq_k_1:
        for list2 in freq_k_1:
            count = 0
            candidate = []
            if list1 != list2: #ensure non-repetition of items
                while count < length-1:
                    if list1[count] != list2[count]:
                        break
                    else:
                        count = count + 1
                else:
                    if list1[length-1] < list2[length-1]:
                        for item in list1:
                            candidate.append(item)
                        candidate.append(list2[length-1])
                        #call our has_infunction to check for infrequent subsets
                        if not has_infrequent_subset(candidate, freq_k_1, k): #if function returns *NOT FALSE*
                            freq_k.append(candidate)
                            candidate = [] #append candidate set to freq_k and empty the candidate[] array to start again
    return freq_k

####################################################################################
##Function to find subsets and sort them in order
def find_subsets(listset, size):
    if size == 0:
        return [[]]
    sortedlist = []
    for i in range(0, len(listset)):
        m = listset[i]
        remainingList = listset[i + 1:]
        for p in find_subsets(remainingList, size - 1):
            sortedlist.append([m] + p)

    return sortedlist

################################################################################
## has_infrequent_subsets function to determine if pruning is required to remove unfruitful
## candidates (candidate) using the Apriori property with prior knowledge of frequent (k-1)-itemset (freq_k_1)
def has_infrequent_subset(candidate, freq_k_1, k):
    list = []
    list = find_subsets(candidate,k)
    #loop through our iterated list in find_subsets function to generate subsets
    for item in list:
        subset = []
        for l in item:
            subset.append(l)
        subset.sort()
        if subset not in freq_k_1:
            return True
    return False

######################################################################
## Function to compute all frequent item sets
def frequent_itemsets():
    #initialize variables
    k = 2
    freq_k_1 = []
    Lk = [] #array to momentarily hold valid frequent itemset
    L = [] #array to hold final items after emptying the momentary Lk array
    count = 0
    transactions = 0
    #send all items in Frequent 1 item set to the frequest (k-1) item set
    for item in Freq_1_itemset:
        freq_k_1.append(item)
    #create new frequent k itemset
    while freq_k_1 != []:
        freq_k = [] #empty the frequent k itemset
        Lk = [] #array to momentarily hold valid itemset subsets
        freq_k = apriori_gen(freq_k_1, k-1) #call our apriori_gen function with new parameter k-1
        for candidate in freq_k:
            count = 0
            transactions = 0
            subset = set(candidate)
            #check pruning to eliminate sets which do not satisfy minsupport condition
            for Transaction_arr in Dataset:
                transactions = transactions + 1
                t = set(Transaction_arr)
                if subset.issubset(t) == True:
                    count = count + 1
            if (100 * count/transactions) >= minsup:
                candidate.sort()
                Lk.append(candidate)
        freq_k_1 = [] #re-empty the frequent k-1 itemset

        print("*********************** FREQUENT %d-ITEMSET ***********************" % k)
        print(Lk)
        print("*******************************************************************")
        #transfer items from Lk to the frequent k-1 itemset and increment value of k to calculate net k itemset
        for l in Lk:
            freq_k_1.append(l)
        k = k + 1
        if Lk != []:
            L.append(Lk)

    return L

#################################################################################################
## Function to generate association rules and print minimum support and minimum confidence values
def generate_association_rules():
    #initialize variables
    subset = []
    association_subset = [] #array to hold subsets
    m = [] #association rule relation set
    length = 0
    count = 1
    increament1 = 0
    increament2 = 0
    number = 1
    L = frequent_itemsets()
    print("******************** GENERATED ASSOCIATION RULES *********************")
    print("******* RULE ******* \t\t\t\t\t ******* {SUPPORT, CONFIDENCE} *****")
    print("---------------------------------------------------------------------")
    #for loop to loop clockwise and anticlockwise
    for list in L:
        for l in list:
            length = len(l)
            count = 1
            while count < length:
                subset = []
                association_subset = find_subsets(l, count)
                count = count + 1
                for item in association_subset:
                    increament1 = 0
                    increament2 = 0
                    subset = []
                    m = []
                    for i in item:
                        subset.append(i)
                    for Transaction_arr in Dataset:
                        if set(subset).issubset(set(Transaction_arr)) == True:
                            increament1 = increament1 + 1
                        if set(l).issubset(set(Transaction_arr)) == True:
                            increament2 = increament2 + 1
                    #satisfy conditions for confidence
                    if 100 * increament2 / increament1 >= minconf:
                        for index in l:
                            if index not in subset:
                                m.append(index)
                        support_value = 100 * increament2 / len(Dataset)
                        confidence_value = 100 * increament2 / increament1
                        print ("Rule# %d : %s --> %s \t\t\t {sup = %d/%d ,conf = %d/%d}" %(number,subset,m,increament2,len(Dataset),increament2,increament1))
                        number = number + 1
###############################################################################
#call function to generate association rules
generate_association_rules()
print ("------------------------------------------------------------------")









