import unittest
from signals import Signal

class Receiver:
    def __init__(self):
        self.count = 0

    def slot(self):
        self.count += 1


class ReceiverWithArg:
    def __init__(self):
        self.count = 0

    def slot(self, arg):
        self.count += arg


class Test(unittest.TestCase):
    def testSignalLen(self):
        receiver = Receiver()
        signal = Signal()
        self.assertEqual(len(signal), 0)
        signal.connect(receiver.slot)
        self.assertEqual(len(signal), 1)

    def testOneSlot(self):
        receiver = Receiver()
        signal = Signal()
        signal.connect(receiver.slot)
        signal()
        self.assertEqual(receiver.count, 1)

    def testTwoSlots(self):
        receiver1 = Receiver()
        receiver2 = Receiver()
        signal = Signal()
        signal.connect(receiver1.slot)
        signal.connect(receiver2.slot)
        signal()
        self.assertEqual(receiver1.count, 1)
        self.assertEqual(receiver2.count, 1)

    def testDisconnect(self):
        receiver = Receiver()
        signal = Signal()
        signal.connect(receiver.slot)
        signal.disconnect(receiver.slot)
        signal()
        self.assertEqual(receiver.count, 0)
        self.assertEqual(len(signal), 0)

    def testDisconnectWeakSlot(self):
        receiver = Receiver()
        signal = Signal()
        signal.connect(receiver.slot)
        del receiver
        self.assertEqual(len(signal), 0)

    def testCantConnectMethodTwice(self):
        """Actually testing an implementation limitation..."""
        receiver = Receiver()
        signal = Signal()
        signal.connect(receiver.slot)
        signal.connect(receiver.slot)
        self.assertEqual(len(signal), 1)

    def testSignalWithArguments(self):
        receiver = ReceiverWithArg()
        signal = Signal()
        signal.connect(receiver.slot)
        signal(123)
        self.assertEquals(receiver.count, 123)

if __name__ == "__main__":
    unittest.main()
