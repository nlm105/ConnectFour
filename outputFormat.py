import pickle

# with open("X.pkl", "rb") as f:
#     arr = pickle.load(f)
#
# print(arr)
# print(len(arr))

def outputArr():
    with open("X.pkl", "rb") as f:
        arr = pickle.load(f)

    print(arr)
    print(len(arr))

def changeLoser(arr):
    arr = arr.copy()
    for i in arr:
        i[1] = i[1]*-1
    return arr

def setTurns(arr, totalTurns):
    arr = arr.copy()
    for i in arr:
        i[1] = totalTurns - i[1] + 1 # add one because w/out winning turn is 0 and want it to be one
    return arr
