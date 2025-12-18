import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import stft, istft
import os

def denoise_audio():
    # 1. Chemins
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    input_path = os.path.join(project_root, 'data', 'noisy_signal.wav')
    output_path = os.path.join(project_root, 'data', 'denoised_signal.wav')

    # 2. Chargement
    fs, noisy_signal = wavfile.read(input_path)
    
    # 3. STFT
    # nperseg=1024 (fenêtre de ~23ms à 44.1kHz)
    f, t, Zxx = stft(noisy_signal, fs=fs, nperseg=1024)
    
    # On récupère le module (amplitude) et la phase
    magnitude = np.abs(Zxx)
    phase = np.angle(Zxx)

    # 4. Estimation du bruit (Noise Estimation)
    # On suppose que les 10 premières fenêtres ne contiennent que du bruit
    noise_estimation = np.mean(magnitude[:, :10], axis=1, keepdims=True)

    # --- 5. Soustraction Spectrale Optimisée ---
    alpha = 2.0  # Facteur d'over-subtraction (plus il est haut, plus on enlève de bruit)
    beta = 0.02  # Spectral floor (évite de mettre à zéro absolu)

    # Application de la formule : Result = Magnitude - alpha * Noise
    magnitude_denoised = magnitude - alpha * noise_estimation
    
    # Au lieu de np.maximum(..., 0), on applique le spectral floor
    # Si la valeur est trop basse, on garde une fraction du bruit d'origine (beta)
    magnitude_denoised = np.where(magnitude_denoised > beta * noise_estimation, 
                                  magnitude_denoised, 
                                  beta * noise_estimation)
    # 6. Reconstruction
    # On réapplique la phase d'origine au nouveau module
    Zxx_denoised = magnitude_denoised * np.exp(1j * phase)
    
    # ISTFT pour revenir dans le domaine temporel
    _, denoised_signal = istft(Zxx_denoised, fs=fs)

    # 7. Sauvegarde
    denoised_signal = np.clip(denoised_signal, -32768, 32767).astype(np.int16)
    wavfile.write(output_path, fs, denoised_signal)
    
    # 8. Visualisation (Sauvegarde en PNG si la fenêtre ne s'ouvre pas)
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.pcolormesh(t, f, 20 * np.log10(magnitude + 1e-10), shading='gouraud')
    plt.title('Spectrogramme Bruité')
    plt.subplot(2, 1, 2)
    plt.pcolormesh(t, f, 20 * np.log10(magnitude_denoised + 1e-10), shading='gouraud')
    plt.title('Spectrogramme Nettoyé')
    plt.tight_layout()
    plt.savefig(os.path.join(project_root, 'data', 'comparison.png'))
    print(f"Traitement terminé. Fichier : {output_path}")

if __name__ == "__main__":
    denoise_audio()