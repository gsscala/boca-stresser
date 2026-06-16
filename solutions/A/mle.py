# Massive heap allocation in Python
l = []
while True:
    l.append(" " * 1024 * 1024)
