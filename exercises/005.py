#Given the head of a singly linked list, return the middle node of the linked list.
#If there are two middle nodes, return the second middle node.

class Node:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def __init__(self):
        self.head = Node()

    def append(self, number) -> Node:
        new_node = Node(number)         # Create a new node with the given number
        current = self.head             # Set the current node as the head of the linked list
        while current.next != None:     # Traverse to the last node of the linked list
            current = current.next      
        current.next = new_node         # Assign the new node as the next node of the last node, this is why 
                                        # e.g. current.next --> None => Node(1) --> None
                                        # e.g. current.next becomes Node(1) with self.val = 1 and self.next = None
        return current.next


my_array = [1, 2, 3, 4, 5, 6]
sol = Solution()
results = []
for i in my_array:
    result = sol.append(i)
    result_str = f'head: {result.val} next: {result.next.val}'
    results.append(result_str)
print(results)
