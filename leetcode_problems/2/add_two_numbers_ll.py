from typing import Optional 

class ListNode:
    def __init__(self, val = 0, next = None):
        self.val = val
        self.next = next 

class Solution:
    def addTwoNumbers(self, l1 : Optional[ListNode], l2 : Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        current = dummy 
        carry = 0

        while l1 or l2 or carry:
            x = l1.val if l1 else 0
            y = l2.val if l2 else 0

            total = x + y + carry 

            digit = total % 10

            carry = total //10

            current.next = ListNode(digit) 
            current = current.next

            if l1:
                l1 = l1.next 
            if l2:
                l2 = l2.next

        return dummy.next 


def build_linked_list(arr: list) -> Optional[ListNode]:
    dummy = ListNode(0)
    current = dummy
    for val in arr:
        current.next = ListNode(val)
        current = current.next
    return dummy.next 

def linked_list_to_list(ll: Optional[ListNode]) -> list:
    res = []
    while ll:
        res.append(ll.val)
        ll = ll.next 
    return res


solution = Solution()

# l1 = [2,4,3]
# l2 = [5,6,4]

l1 = [9,9,9,9,9,9,9]
l2 = [9,9,9,9]

# 1. Convert Python lists to linked lists
l1 = build_linked_list(l1)
l2 = build_linked_list(l2)

answer = solution.addTwoNumbers(l1, l2)

print(linked_list_to_list(answer))