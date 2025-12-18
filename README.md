# Audio-Spectral-Denoiser
This project implements a high-level speech enhancement algorithm based on Short-Time Fourier Transform (STFT) and Spectral Subtraction. It is designed to remove stationary noise from audio recordings while preserving speech intelligibility.

#Technical Approach
The denoiser uses an optimized spectral subtraction method. Key features include:
- Noise Estimation: Calculated during the first 230ms of the signal (assumed silence).
- Over-subtraction ($\alpha=2.0$): Reduces broadband noise more aggressively to handle peaks.
- Spectral Floor ($\beta=0.02$): Prevents "musical noise" and artifacts by maintaining a natural background noise level.

#Visual Results
<img width="1200" height="600" alt="comparison" src="https://github.com/user-attachments/assets/7eac9e66-bbe8-4628-acbc-4c07c3a1ed90" />
