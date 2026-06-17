import sys

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

sao_paulo = [
    Point(0, 100), Point(100, 0), Point(200, 0), Point(100, -100),
    Point(0, -100), Point(-100, 0), Point(-200, 0), Point(-100, 100)
]

def cross_product(a, b, c):
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

def on_segment(p, a, b):
    if cross_product(a, b, p) == 0:
        if p.x >= min(a.x, b.x) and p.x <= max(a.x, b.x) and \
           p.y >= min(a.y, b.y) and p.y <= max(a.y, b.y):
            return True
    return False

def is_inside_or_on_border(p, poly):
    n = len(poly)
    inside = False
    for i in range(n):
        j = (i - 1 + n) % n
        if on_segment(p, poly[i], poly[j]):
            return True
        if ((poly[i].y > p.y) != (poly[j].y > p.y)):
            intersectX = (poly[j].x - poly[i].x) * (p.y - poly[i].y) / (poly[j].y - poly[i].y) + poly[i].x
            if p.x < intersectX:
                inside = not inside
    return inside

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    ptr = 1
    results = []
    for _ in range(N):
        x = int(input_data[ptr])
        y = int(input_data[ptr+1])
        ptr += 2
        p = Point(x, y)
        if is_inside_or_on_border(p, sao_paulo):
            results.append("S")
        else:
            results.append("N")
    sys.stdout.write("\n".join(results) + "\n")

if __name__ == "__main__":
    main()
