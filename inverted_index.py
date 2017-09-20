from collections import defaultdict

def inv_index(collection):
    inv_idx = defaultdict(list)
    for i,c in enumerate(collection):
        for word in c:
            inv_idx[word].append(i+1)
    return inv_idx

