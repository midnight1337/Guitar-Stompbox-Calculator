from transistors import Transistor
from bjt import Bjt
from resistors import Resistors
from collector_feedback import CollectorFeedback


transistors = [
    ("2N2222", 60),
    ("2N2223", 100)
]

r = Resistors(rb=410, rc=47, re=0.1, multiplier=10**3)
t = Transistor()

for q in transistors:
    t.add_transistor(transistor=Bjt(*q))


c = CollectorFeedback(transistor=t(model="2N2222"), **r.resistors)
c.calculate_and_save_values()
c.read_documentation()

# for k in t.transistors:
#     c = CollectorFeedback(transistor=t(model=k), **r.resistors)
#     c.calculate_and_save_values()
#     c.read_documentation()
