import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import io
import soundfile as sf
import matplotlib
matplotlib.use('Agg') # Ensure non-interactive backend for containers/servers
from filters import apply_fir_filter, apply_lms_filter, normalize_audio

# Page Configuration
st.set_page_config(
    page_title="Cancelación de Ruido en Audio: FIR vs LMS",
    page_icon="🔊",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1e1e2f 0%, #2a2a40 100%);
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: #4e54c8;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #8f94fb;
        transform: translateY(-2px);
    }
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
    }
    h1, h2, h3 {
        color: #8f94fb;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🔊 Cancelación de Ruido en Señales de Audio")
st.markdown("### Comparación entre Filtros FIR y Algoritmo LMS (Adaptativo)")
st.divider()

# Sidebar Controls
st.sidebar.header("🛠️ Configuración de Filtros")

# FIR Filter Parameters
st.sidebar.subheader("Paso-Bajos (FIR)")
fir_cutoff = st.sidebar.slider("Frecuencia de Corte (Hz)", 100, 8000, 2000)
fir_order = st.sidebar.slider("Orden del Filtro", 11, 301, 101, step=2)

# LMS Filter Parameters
st.sidebar.subheader("Adaptativo (LMS)")
lms_mu = st.sidebar.slider("Tasa de Aprendizaje (mu)", 0.001, 0.1, 0.01, format="%.3f")
lms_order = st.sidebar.slider("Orden del Filtro LMS", 8, 128, 32)

# File Uploaders
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📁 Señal Ruidosa Principal")
    noisy_file = st.file_uploader("Sube el archivo .wav con ruido", type=["wav"])

with col2:
    st.markdown("#### 📁 Referencia de Ruido (Solo LMS)")
    noise_ref_file = st.file_uploader("Sube el archivo de solo ruido", type=["wav"])

def plot_spectrogram(audio_data, sr, title, ax):
    D = librosa.amplitude_to_db(np.abs(librosa.stft(audio_data)), ref=np.max)
    img = librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz', ax=ax, cmap='magma')
    ax.set_title(title)
    ax.tick_params(colors='white')
    return img

if noisy_file is not None:
    try:
        # Load audio
        y_noisy, sr = librosa.load(noisy_file, sr=None)
        y_noisy = normalize_audio(y_noisy)
        
        st.write(f"**Archivo:** {noisy_file.name} | **Frecuencia de muestreo:** {sr} Hz")
        
        # Display original audio
        with st.expander("▶️ Escuchar Señal Original", expanded=True):
            st.audio(noisy_file, format="audio/wav")
            fig_orig, ax_orig = plt.subplots(figsize=(10, 2))
            ax_orig.plot(y_noisy, color='#888888', alpha=0.6)
            ax_orig.set_title("Onda Original (Ruidosa)")
            ax_orig.set_facecolor('#0e1117')
            ax_orig.tick_params(colors='white')
            st.pyplot(fig_orig)
        
        # Processing options
        st.divider()
        st.subheader("📊 Resultados del Procesamiento")
        
        res_col1, res_col2 = st.columns(2)
        
        # FIR Processing
        with res_col1:
            st.markdown("#### 1. Filtro FIR (Paso-Bajos)")
            st.caption("Elimina frecuencias altas por encima del punto de corte.")
            y_fir = apply_fir_filter(y_noisy, fir_cutoff, sr, fir_order)
            
            # Sub-tabs for Time and Frequency domains
            tab_time, tab_freq = st.tabs(["Onda", "Espectrograma"])
            
            with tab_time:
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(y_fir, color='#ff7f0e', alpha=0.8)
                ax.set_title("Señal Filtrada con FIR")
                ax.set_facecolor('#0e1117')
                ax.tick_params(colors='white')
                st.pyplot(fig)
            
            with tab_freq:
                fig_spec, ax_spec = plt.subplots(figsize=(10, 4))
                plot_spectrogram(y_fir, sr, "Espectrograma FIR", ax_spec)
                st.pyplot(fig_spec)
            
            # Download/Play
            buffer = io.BytesIO()
            sf.write(buffer, y_fir, sr, format='WAV')
            st.audio(buffer, format="audio/wav")
            st.download_button("📥 Descargar FIR", data=buffer.getvalue(), file_name="fir_filtered.wav")

        # LMS Processing
        with res_col2:
            st.markdown("#### 2. Filtro Adaptativo (LMS)")
            st.caption("Aprende la estructura del ruido y lo sustrae dinámicamente.")
            if noise_ref_file is not None:
                y_ref, _ = librosa.load(noise_ref_file, sr=sr)
                y_ref = normalize_audio(y_ref)
                
                y_lms = apply_lms_filter(y_noisy, y_ref, lms_mu, lms_order)
                
                tab_time_lms, tab_freq_lms = st.tabs(["Onda", "Espectrograma"])
                
                with tab_time_lms:
                    fig, ax = plt.subplots(figsize=(10, 4))
                    ax.plot(y_lms, color='#2ca02c', alpha=0.8)
                    ax.set_title("Señal Filtrada con LMS")
                    ax.set_facecolor('#0e1117')
                    ax.tick_params(colors='white')
                    st.pyplot(fig)
                
                with tab_freq_lms:
                    fig_spec_lms, ax_spec_lms = plt.subplots(figsize=(10, 4))
                    plot_spectrogram(y_lms, sr, "Espectrograma LMS", ax_spec_lms)
                    st.pyplot(fig_spec_lms)
                
                # Download/Play
                buffer_lms = io.BytesIO()
                sf.write(buffer_lms, y_lms, sr, format='WAV')
                st.audio(buffer_lms, format="audio/wav")
                st.download_button("📥 Descargar LMS", data=buffer_lms.getvalue(), file_name="lms_filtered.wav")
            else:
                st.info("💡 Sube una **referencia de ruido** en el panel superior derecho para habilitar el procesamiento LMS.")
                st.warning("El filtro LMS requiere una señal de ruido correlacionada para funcionar correctamente.")

    except Exception as e:
        st.error(f"Error al procesar el audio: {e}")
else:
    st.info("👆 Por favor, sube un archivo de audio para comenzar.")

st.sidebar.divider()
st.sidebar.info("Este prototipo permite ajustar parámetros en tiempo real para visualizar cómo afecta cada filtro a la cancelación de ruido.")
