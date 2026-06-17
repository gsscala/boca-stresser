import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    W = int(input_data[0])
    A = int(input_data[1])
    B = int(input_data[2])
    C = int(input_data[3])
    
    if W >= (A + B + C):
        print("S")
    else:
        print("N")

if __name__ == "__main__":
    main()
