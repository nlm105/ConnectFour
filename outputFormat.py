import pickle

with open("X.pkl", "rb") as f:
    arr = pickle.load(f)

print(arr)
print(len(arr))
