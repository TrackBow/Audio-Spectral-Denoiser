import numpy as np
from scipy.io import wavfile
import os

def create_mixed_signal(speech_path, noise_path, output_path, snr_db=10):
    # Chargement de l'audio
    if not os.path.exists(speech_path) or not os.path.exists(noise_path):
        print(f"Erreur : Un des fichiers sources est introuvable.\nSpeech: {speech_path}\nNoise: {noise_path}")
        return

    fs_s, speech = wavfile.read(speech_path)
    fs_n, noise = wavfile.read(noise_path)
    
    # Nettoyage (Mono + Float)
    if len(speech.shape) > 1: speech = speech[:, 0]
    if len(noise.shape) > 1: noise = noise[:, 0]
    
    speech = speech.astype(np.float32)
    noise = noise.astype(np.float32)

    # Alignement des longueurs des audios
    length = min(len(speech), len(noise))
    speech = speech[:length]
    noise = noise[:length]

    # Calcul du SNR
    p_speech = np.mean(speech**2)
    p_noise = np.mean(noise**2)
    
    if p_noise == 0:
        print("Erreur : Le fichier de bruit est vide.")
        return

    factor = np.sqrt(p_speech / (p_noise * (10**(snr_db / 10))))
    noisy_signal = speech + factor * noise

    # Sauvegarde et Normalisation
    max_val = np.max(np.abs(noisy_signal))
    if max_val > 0:
        noisy_signal = (noisy_signal / max_val * 32767).astype(np.int16)
    
    wavfile.write(output_path, fs_s, noisy_signal)
    print(f"Mélange terminé : {output_path} (SNR: {snr_db}dB)")

# --- GESTION DES CHEMINS AUTOMATIQUE ---
if __name__ == "__main__":
    # Récupère le chemin du dossier où se trouve le script 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Remonte au dossier parent du projet
    project_root = os.path.dirname(current_dir)
    
    # Chemins complets
    speech_in = os.path.join(project_root, 'data', 'clean_speech.wav')
    noise_in = os.path.join(project_root, 'data', 'noise_fan.wav')
    out = os.path.join(project_root, 'data', 'noisy_signal.wav')

    # Lancement
    create_mixed_signal(speech_in, noise_in, out, snr_db=10)