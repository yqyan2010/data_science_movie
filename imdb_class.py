import numpy as np
#---Methods----
def create_sub_dic(string):
    dic={}
    #--Removes json notation characters-------
    string=string.translate({ord(i):None for i in "[{'':,}]"})
    #--Convert string to list to work with
    string_list=string.split()
    for j in range(0,len(string_list)):
        if string_list[j]=='id' and string_list[j+2]=='name':
            if int(string_list[j+1]) not in dic.keys():
                dic[int(string_list[j+1])]=string_list[j+3].lower()
                #--Caution: error out if id is not int---
                #--Caution: this only handles upper case to lower case----
                #----------error out if string has special characters or white space----
                #----------e.g. Animation==An1mation, but your computer won't think so---
    return(dic)

def create_sub_dic_prodcom(string,dic):
    
    string=string.translate({ord(i):None for i in "[{'':,}]"})
    
    """Find first name of production name"""    
    #--Find ind_name and ind_id with this given string---------
    #--Caution: if ' name ' and ' id ' are in the name of company, it can still throw errors-----
    ind_name=string.find(' name ')+1##--Caution, we use ' name ', b/c 'name' can be in the name of company
    ind_id=string.find(' id ')+1##--Caution, we use ' id ', b/c 'id can be in the name of company--
    
    if ind_name != 0:
        #--Slice out the name---------
        name=string[ind_name+len('name')+1:ind_id-1]
    
        """Find first id with that first name"""
        #--Update string with first name removed
        string=string[ind_name+len('name')+1:]
    
        #--Update ind_id and ind_name with new string----
        ##--Caution:ind_name can be -1 if not exist----
        ind_name=string.find(' name ')+1#--Caution: if 'name not exist',it returns -1, ind_name will be 0
        ind_id=string.find(' id ')+1
    
        #--Slice out id number---
        ###Caution:error out if you don't slice the right number---
    
        if ind_name!=0:
            idnum=int(string[ind_id+len('id')+1:ind_name-1])
        else:
            idnum=int(string[ind_id+len('id')+1:])
    
        #--Populate the result dictionary----
        if idnum not in dic.keys():
            dic[idnum]=name
    
        #--If the string still has name, continue--
        ##--Caution: this assumes that whenever there is a name, there is a id to pair with---------
        if ind_name!=0:
        
            #--Update string that it starts with next name----
            string=string[ind_name-1:]
            create_sub_dic_prodcom(string,dic)
    
    return dic

def create_id_name(arr):
    summary_dic={}
    #--arr is the numpy array of that column----
    for i in range(0,len(arr)):
        #--Get each item of the array---
        #--item is string type---
        item=arr[i]
        if item != np.nan:
        #--Get a sub dictinary of each item---
            item_dic=create_sub_dic(item)
        for key,value in item_dic.items():
            if key not in summary_dic.keys():
                summary_dic[key]=value
    return summary_dic
    
def create_count_summary(arr):
    summary_dic={}
    dic={}
    #--Create a dictinary first---
    #--Key is genre type, value is count-------
    for i in range(0,len(arr)):
        item=arr[i]
        if item!=np.nan:
            item_dic=create_sub_dic(item)
        for key,value in item_dic.items():
            if value not in summary_dic.keys():
                summary_dic[value]=1
            else:
                summary_dic[value]+=1
    #--Re-order the dictinary from top count to bottom count---
    sorted_keys=sorted(summary_dic, key=summary_dic.get, reverse=True)
    for key in sorted_keys:
        dic[key]=summary_dic[key]
    #--Caution, the summary_dic has the key as a tuple
    return dic

def create_count_summary_prodcom(arr):
    import numpy as np
    summary_dic={}
    dic={}
    #--Create a dictinary first---
    #--Key is genre type, value is count-------
    for i in range(0,len(arr)):
        #--Get each item of the numpy arr, each item is a list like string---
        item=arr[i]
        if not str(type(item))[8:13]=='float':
            #item=arr[i]
            #--Clean the string here--
            item=item.translate({ord(j):None for j in "[{'':,}]"})
            #--Add a white space in front of first name---
            item=" "+item
            #--Get productio company and its id hash table---
            item_dic=create_sub_dic_prodcom(item,{})#--In this function, it removes special characters of string---
            for key,value in item_dic.items():
                if value not in summary_dic.keys():
                    summary_dic[value]=1
                else:
                    summary_dic[value]+=1
    #--Re-order the dictinary from top count to bottom count---
    sorted_keys=sorted(summary_dic, key=summary_dic.get, reverse=True)
    for key in sorted_keys:
        dic[key]=summary_dic[key]
    #--Caution, the summary_dic has the key as a tuple
    return dic

"""Functions to return month and year"""
"""Input: numpy array structure"""
"""Output: tuple of month and year ([month],[year])"""
def getmonthyear(arr):
    month=[]
    yr=[]
    
    ##--Caution:assume each arr[i] is not empty or not nan-------
    for i in range(0,len(arr)):
        lst=arr[i].split("/")
        month.append(lst[0])
        yr.append(lst[2])
    
    return (month,yr)

"""Function that test getmonthyear"""
def test_getmonthyear(arr):
    result="Test pass"
    arr_month=getmonthyear(arr)[0]
    arr_year=getmonthyear(arr)[1]
    
    for index in range(0,len(arr)):
    #--Month should match--Year should match---
    #--Month if 10,11,12, only first digit 1 matches
        if arr[index][0:1] == arr_month[index][0:1] and arr[index][-4:] == arr_year[index]:
            pass
        else:
            print("Fail at location {}".format(index))
            result="Test fails"
    print(result)
