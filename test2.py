# test algorthim
# By Kevin Gonzaez (SimpleXTeam Leader)

import random
import platform
import os

keyValues = {"A": ["BKSHDKJSHDJKSHKJ", "C", "skjhdkjashkjdhak", "djlksajdlkajsld", "sadlkasjdlkja"]}
testWrite = []


holdvalue = []
listIndexCounter = []
maxLength = 35

def clearTerminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")



def write(vParamToWrite):
    for x in vParamToWrite:
        vHTMLReturn = " ".join(x)
        print vHTMLReturn
    
    

def getlength():
    count = 0
    for v in holdvalue:
        count += len(v)
    return count

clearTerminal()

for x in keyValues:
    innerList = keyValues[x]
    innerListlength = len(innerList)
    holdvalue_counter = 0
    loopCounter = 0
    loopIterator = 0
    for loopIterator in range(innerListlength):
        print "-------- TEST CONDITION {} ({}) --------".format(loopCounter, loopIterator)
        # if loopIterator != innerListlength:
        # print "-------------------------------------------------"
        # print "[+] Checking: {} and {}".format(innerList[loopIterator], innerList[loopIterator+1])
        # print "-------------------------------------------------"

        if len(holdvalue) == 0:
            print "[+] List has nothing"
            if len(innerList[loopIterator]) + len(innerList[loopIterator+1]) > 35:
                holdvalue.append(innerList[loopIterator])
            else:
                holdvalue.extend((innerList[loopIterator], innerList[loopIterator+1]))
                loopIterator += 2
                print "[+] loopIterator {}".format(loopIterator)
        else:
            # print "-------------------------------------------------"
            # print "[+] Got Length: {}".format(len(innerList[loopIterator]) + len(innerList[loopIterator+1]))
            # print "-------------------------------------------------"
            # if list has values
            tempVar = len(holdvalue)

            #checksum holdvalue elements
            for holdValueCounter in holdvalue:
                print "[+] Read -> {}".format(holdValueCounter)
                holdvalue_counter += len(holdValueCounter)

            print "[+] Total: {} | with checksum {}".format(getlength(), getlength()+holdvalue_counter)


            # for iterator in range(tempVar):
            if len(innerList[loopIterator]) + holdvalue_counter < 35:
                print "[+] Value is still less than the maximum ({}, {}, {})".format(loopIterator, innerList[loopIterator], len(innerList[loopIterator])+holdvalue_counter)
            # if len(innerList[loopIterator]) - len(holdvalue[iterator]) > 0:
                # print "[+] Checking Difference: {} - {}".format(len(innerList[loopIterator]) - len(holdvalue[iterator]))
                print "[+] InnerList (keyvalues): {}".format(innerList)

                # check if element already exists inside if the list


                if innerList[loopIterator+1] in holdvalue:
                    print "[-] DEBUG ERROR: {}".format(holdvalue)
                    loopIterator += 2
                    loopCounter += 1
                    continue
                else:
                    print "[+] Appending To List: {}".format(innerList[loopIterator+1])
                    holdvalue.append(innerList[loopIterator+1])


            else:
                # print "[+] BreakingPoint {} ({})".format(len(holdvalue[iterator]) - len(innerList[loopIterator]), innerList[loopIterator])

                y = 0
                for vCheck in holdvalue:
                    y += len(vCheck)

                testWrite.append(holdvalue)

                # print "[/\] Value is still less than the maximum ({}, {}, {})".format(loopIterator, innerList[loopIterator], len(innerList[loopIterator])+holdvalue_counter)
                print "[+] Checked Element {} ({})".format(innerList[loopIterator], len(innerList[loopIterator]) + holdvalue_counter)
                print "[+] Reached Max Value: {}".format(y)
                print "[+] Sending List: {}".format(holdvalue)
                print "[+] Sending Parameter -> {}".format(holdvalue)
                print "[+] Send Write List: {}".format(testWrite)
                # clearList(holdvalue)
                holdvalue = []
                loopCounter += 1
                continue
        loopCounter += 1
        holdvalue_counter = 0
        print holdvalue
            
            

        # if len(innerList[loopIterator]) + len(innerList[loopIterator+1]) > 35:
        #     holdvalue.append(innerList[loopIterator])
        # else:
        #     # print "-------------------------------------------------"
        #     # print "[+] Got Length: {}".format(len(innerList[loopIterator]) + len(innerList[loopIterator+1]))
        #     # print "-------------------------------------------------"
        #     if len(holdvalue) == 0:
        #     # If list has nothing extend to list the first two values
        #         holdvalue.extend((innerList[loopIterator], innerList[loopIterator+1]))
        #         loopIterator = loopIterator + 2
        #     else:

        #         # if list has values
        #         tempVar = len(holdvalue)

        #         #checksum holdvalue elements
        #         for holdValueCounter in holdvalue:
        #             holdvalue_counter += len(holdValueCounter)


        #         # for iterator in range(tempVar):
        #         if len(innerList[loopIterator]) + holdvalue_counter < 35:
        #             print "[+] Value is still less than the maximum"
        #         # if len(innerList[loopIterator]) - len(holdvalue[iterator]) > 0:
        #             # print "[+] Checking Difference: {} - {}".format(len(innerList[loopIterator]) - len(holdvalue[iterator]))
        #             print "[+] InnerList (keyvalues): {}".format(innerList)

        #             # check if element already exists inside if the list
        #             if innerList[loopIterator] in holdvalue:
        #                 continue
        #             else:
        #                 print "[+] Appending To List: {}".format(innerList[loopIterator])
        #                 holdvalue.append(innerList[loopIterator])
        #         else:
        #             # print "[+] BreakingPoint {} ({})".format(len(holdvalue[iterator]) - len(innerList[loopIterator]), innerList[loopIterator])

        #             y = 0
        #             for vCheck in holdvalue:
        #                 y += len(vCheck)

        #             print "[+] Reached Max Value: {}".format(y)
        #             print "[+] Sending List: {}".format(holdvalue)
        #             print "[+] Sending Parameter -> {}".format(holdvalue)
        #             clearList(holdvalue)
        #             continue
        #         print "-------- DONE --------".format(loopCounter)
        #     loopCounter += 1
        #     holdvalue_counter = 0
        #     print holdvalue

x = 0
for y in holdvalue:
    x += len(y)

print "Final Value: {}".format(x)
print "-----------------------------"
print write(testWrite)
