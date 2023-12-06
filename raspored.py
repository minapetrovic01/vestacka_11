def postavi_balansirane_figure(n, m):
    if n % 2 != 0 or m % 8 != 0:
        print("Nemoguće postaviti figure sa zadatim uslovima.")
        return

    tabla = [[' ' for _ in range(n)] for _ in range(n)]
    
    crne=bele=m/2

    # Postavljanje figura na svako drugo crno polje u neparnim redovima
    for i in range(1, n, 2):
        for j in range(0, n, 2):
            if crne > 0:
                tabla[i][j] = 'C'
                crne -= 1
    # Postavljanje figura na svako drugo crno polje u parnim redovima
    for i in range(2, n, 2):
        for j in range(1, n, 2):
            if bele > 0:
                tabla[i][j] = 'B'
                bele -= 1

    # Provera i ispis tabele
    for row in tabla:
        print(row)

# Primer poziva funkcije sa n=8 i m=16
postavi_balansirane_figure(12,8)