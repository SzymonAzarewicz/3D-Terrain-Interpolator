import numpy as np
from scipy import io
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def wczytaj_dane(sciezka):
    return io.loadmat(sciezka)['data_map']

def oblicz_wysokosci(punkty_znane, wysokosci_znane, punkty_do_obliczenia):
    wyniki = np.zeros(len(punkty_do_obliczenia))
    
    for i, punkt in enumerate(punkty_do_obliczenia):
        odleglosci = np.sqrt(np.sum((punkty_znane - punkt) ** 2, axis=1))
        odleglosci[odleglosci < 0.0000001] = 0.0000001
        wagi = 1 / (odleglosci ** 2)
        wyniki[i] = np.sum(wagi * wysokosci_znane) / np.sum(wagi)
    
    return wyniki

def main():
    # Wczytanie danych
    dane = wczytaj_dane(r"C:\Users\azare\OneDrive\Pulpit\popr_7\data_map.mat")
    
    # Tworzenie siatki punktów
    x = np.linspace(min(dane[:, 0]), max(dane[:, 0]), 30)
    y = np.linspace(min(dane[:, 1]), max(dane[:, 1]), 30)
    X, Y = np.meshgrid(x, y)
    
    # Obliczenie wysokości dla siatki punktów
    punkty_siatki = np.column_stack((X.flatten(), Y.flatten()))
    wysokosci = oblicz_wysokosci(dane[:, :2], dane[:, 2], punkty_siatki)
    Z = wysokosci.reshape(X.shape)
    
    # Tworzenie wykresu
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    def aktualizuj_wykres(klatka):
        ax.clear()
        wysokosc_aktualna = Z * (klatka / 50)
        ax.plot_surface(X, Y, wysokosc_aktualna, cmap='terrain')
        ax.scatter(dane[:, 0], dane[:, 1], dane[:, 2], c='red', marker='o', s=10)
        ax.set_title('Teren 3D')
    
    animacja = FuncAnimation(fig, aktualizuj_wykres, frames=51, interval=100, repeat=False)
    plt.show()

if __name__ == "__main__":
    main()
