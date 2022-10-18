class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def traverse_list(self, target):
        cur = self.head
        while cur:
            if cur.data == target:
                return cur
            cur = cur.next
        return False

    def append(self, val):
        new_node = Node(data=val)
        if self.head == None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node
            new_node.prev = cur

        return self.head

    def arr_to_list(self, arr):
        self.head = None
        for ele in arr:
            self.head = self.append(ele)
        return self.head

    # def printt(self):
    #     cur = self.head
    #     while cur:
    #         print(cur.data)
    #         cur = cur.next
    #     while cur:
    #         print(cur.data)
    #         cur = cur.prev
    #
