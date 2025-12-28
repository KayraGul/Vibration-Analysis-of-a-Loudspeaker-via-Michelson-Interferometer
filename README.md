# 🎵 Vibration Analysis of a Loudspeaker via Michelson Interferometer

This project presents an experimental study on detecting and analyzing **mechanical vibrations** using a **modified Michelson interferometer**. By mounting one interferometer mirror on a **loudspeaker**, vibrations induced by sound waves are converted into **optical path length modulations**, which are measured through changes in the interference pattern and analyzed using **Fast Fourier Transform (FFT)** techniques.

---

## 📹 Project Demonstration

Watch the live **demonstration video** of the setup and results:

<iframe width="560" height="315" src="https://www.youtube.com/embed/KqWnFWd6NJk" title="Project Demonstration Video" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

[👉 Open on YouTube](https://youtu.be/KqWnFWd6NJk)

---

## 🔬 Project Overview

- **Objective:**  
  To precisely measure vibration frequencies produced by a loudspeaker using optical interferometry.

- **Core Idea:**  
  Vibrations of a mirror alter the optical path difference, producing time-dependent intensity variations at the photodetector. These variations encode the vibration frequencies.

- **Key Techniques:**  
  - Michelson interferometry  
  - Optical vibration sensing  
  - Photodiode signal acquisition  
  - FFT-based frequency analysis  

---

## 🧪 Experimental Setup

- 532 nm green laser  
- Michelson interferometer  
- Loudspeaker-mounted mirror  
- Beam splitter and precision mirrors  
- Diverging and converging lenses for fringe magnification  
- BPW 34 S photodiode with TLV2462 amplifier  
- Arduino Uno for high-speed data acquisition (~3.8 × 10⁴ samples/s)  
- MATLAB and Python for signal generation and FFT analysis  

---

## 📊 Methodology

1. Generate controlled vibration frequencies using MATLAB (single, double, and triple sine waves).  
2. Introduce vibrations via the loudspeaker-mounted mirror.  
3. Record photodetector voltage output using Arduino.  
4. Apply Hann-windowed FFT to extract frequency components.  
5. Compare detected frequencies with the known input signals.  
6. Extend analysis to complex audio signals (music and speech) and reconstruct frequency spectra.

---

## 📈 Results Summary

- Accurate detection of vibration frequencies between **50 Hz and 2000 Hz**  
- Consistent frequency error of approximately **0.1%**  
- Successful identification of multiple simultaneous frequencies  
- Reconstructed complex audio spectra closely matched reference signals  
- Reduced sensitivity observed at higher frequencies (~5000 Hz)

---

## ⚠️ Limitations & Error Sources

- External vibration noise despite seismic isolation  
- Non-ideal laser beam homogeneity  
- Optical component losses and reflections  
- Harmonic distortion from loudspeaker nonlinearity  
- FFT convolution effects due to finite sampling time  

---

## ✅ Conclusion

This experiment demonstrates that a **modified Michelson interferometer** can function as a sensitive optical vibrometer. The system reliably extracts vibration frequencies introduced by a loudspeaker and validates the effectiveness of combining interferometric techniques with digital signal processing. With improved optical components and vibration isolation, the sensitivity and measurable frequency range could be further enhanced.

---

## 📄 Full Report

For complete theoretical background, experimental details, figures, and analysis, see:

**PHYS211_FinalReport.pdf**
