import hashlib
import multiprocessing 
import time

stop_event = multiprocessing.Array('c', b'\0' * 20)

def ConvertValueToStr(num, indexTable): #Getting a int num and convert this to str
    text = ""
    if(num == 0): return indexTable[0]
    basis = len(indexTable)
    while (not num == 0):
        text += indexTable[num % basis]
        num //= basis
    return text[::-1]

def StringToValue(string, indexTable): #Getting string and convert it to int value
    basis = len(indexTable)
    num = 0
    count = 0
    for i in string[::-1]:
        num += basis ** count * indexTable.index(i)
        count += 1  

    return num

def RunOptionsProcess(start, end, md5, indexTable, stop_event):
    lst = list(start) 
    lstIndex = []
    for c in lst:
       lstIndex.append(indexTable.index(c))
    listEnd = list(end)
    password = ""
    #count = 1

    if(md5 == hashlib.md5(("".join(lst).encode())).hexdigest()):
        return("".join(lst))

    while(listEnd != lst):
        i = -1
        #count += 1

        while(lst[i] == indexTable[-1] and i > -len(lst)):
            lst[i] = indexTable[0]
            lstIndex[i] = 0
            i-=1
        if(lst[i] == indexTable[-1]):
            lst[i] = indexTable[0]
            lstIndex[i] = 0
            lstIndex.insert(0, 0)
            lst.insert(0, indexTable[0])
        else:
            lstIndex[i] += 1
            lst[i] = indexTable[lstIndex[i]] #chr(ord(lst[i]) + 1)
        if(md5 == hashlib.md5(("".join(lst).encode())).hexdigest()):
            password = "".join(lst)
            stop_event.value = password.encode() 
            break
    #print(count)  
    #print(lst)
    
def RunAllOptions(start, end, md5, indexTable, processAmount = 4):
    print("Start")
    processes = []
    global stop_event
    startNum = StringToValue(start, indexTable)
    endNum = StringToValue(end, indexTable)
    size = (endNum - startNum) // processAmount
    lastLen = len(start)

    for i in range(processAmount):
        if(i == 0): 
            newStart = start
        else:
            newStart = ConvertValueToStr(int(startNum + size * i) + 1, indexTable)
            if(lastLen > len(newStart)):
                newStart = (indexTable[0] *  (lastLen - len(newStart))) + newStart 
            else:
                lastLen = len(newStart)
        if(processAmount != i + 1):
            newEnd = ConvertValueToStr(int(startNum + size * (i + 1)), indexTable)
            if(lastLen > len(newEnd)):
                newEnd = (indexTable[0] *  (lastLen - len(newEnd))) + newEnd
            else:
                lastLen = len(newEnd)
        else:
            newEnd = end

        #print(newStart, newEnd)
        processes.append(multiprocessing.Process(target = RunOptionsProcess, args= 
            (newStart, newEnd, md5, indexTable, stop_event, )))
    
    for p in processes:
        p.start()

    while any(process.is_alive() for process in processes) and stop_event.value == b'':
        time.sleep(0.1)

    for p in processes:
        p.terminate()
    if(stop_event.value == b''):
        return("password was not found")
    elif(stop_event.value.decode() == "E N D"):
        return("server force stop")
    else:
        return(stop_event.value.decode())

def BruteForce(start, end, md5, processAmount = 4, indexTable = []):
    if(indexTable == []):
        for i in range(ord('a'), ord('z') + 1):
            indexTable.append(chr(i))

    return(RunAllOptions(start, end, md5, indexTable, processAmount)) #זה הבדיקה עצמה של האפשרויות
        
def main():
    start = "a" 
    end =  "z" * 5 #כרגע 9 מוגדר בתור התו האחרון בגלל שהוא הוכנס אחרון לרשימה של האינקדסים
    targetMD5 = hashlib.md5(("agzvb").encode()).hexdigest()
    processAmount = 6

    password = BruteForce(start, end, targetMD5, processAmount)
    print(password)


if __name__ =='__main__':
    main()