import sys

def main():
    s = sys.stdin.read().strip()
    if not s:
        return
    
    estados = [
        "BR-AC", "BR-AL", "BR-AP", "BR-AM", "BR-BA", "BR-CE", "BR-DF", "BR-ES",
        "BR-GO", "BR-MA", "BR-MT", "BR-MS", "BR-MG", "BR-PA", "BR-PB", "BR-PR",
        "BR-PE", "BR-PI", "BR-RJ", "BR-RN", "BR-RS", "BR-RO", "BR-RR", "BR-SC",
        "BR-SP", "BR-SE", "BR-TO"
    ]
    
    correspondencias = 0
    bate_com_sp = False
    
    for estado in estados:
        eh_compativel = True
        for i in range(5):
            if s[i] != '?' and s[i] != estado[i]:
                eh_compativel = False
                break
        
        if eh_compativel:
            correspondencias += 1
            if estado == "BR-SP":
                bate_com_sp = True
                
    if bate_com_sp:
        if correspondencias == 1:
            print("S")
        else:
            print("T")
    else:
        print("N")

if __name__ == "__main__":
    main()
