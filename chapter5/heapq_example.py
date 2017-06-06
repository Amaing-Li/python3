# a heap is a binary tree that repects the heap property, which is that
# the first item (at index position 0) is always the samllest item.
# each of a heap's subtrees is also a heap
import heapq

heap = []
heapq.heappush(heap, (5, "rest"))
heapq.heappush(heap, (2, "work"))
heapq.heappush(heap, (4, "study"))
# heapq.heapify(alist)  # to convert a list to a heap
item = heapq.heappop(heap)  # the smallest item can be removed
print(item)

for x in heapq.merge([1, 3, 5, 8], [2, 4, 7], [0, 1, 6, 8, 9]):
    print(x, end=" ")  # prints: 0 1 1 2 3 4 5 6 7 8 8 9
