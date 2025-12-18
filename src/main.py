import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

fs, data = wavfile.read('../data/clean_speech.wav')

print(f"Fréquence d'échantillonnage : {fs} Hz")
print(f"Durée : {len(data)/fs:.2f} secondes")

# Visualisation temporelle
plt.figure(figsize=(10, 4))
plt.plot(data)
plt.title("Signal Audio Brut (Temporel)")
plt.xlabel("Échantillons")
plt.ylabel("Amplitude")
plt.show()