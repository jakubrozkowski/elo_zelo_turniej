import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- INICJALIZACJA ---
if "show_next" not in st.session_state:
    st.session_state.show_next = False
if "punkty" not in st.session_state:
    st.session_state.punkty = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "czas" not in st.session_state:
    st.session_state.czas = 5
if "reset_input" not in st.session_state:
    st.session_state.reset_input = False
if "input_key" not in st.session_state:
    st.session_state.input_key = "turniej_input_0"

# --- EKRAN STARTOWY ---
if not st.session_state.show_next:
    st.title("Elo żelo turniej")
    st.write("#### Ile razy jesteś w stanie napisać *Elo żelo*?")

    poziom = st.selectbox(
        "Wybierz poziom trudności:",
        ["Łatwy", "Trudny", "Elec Żelec"]
    )
    st.session_state.czas = 5 if "Łatwy" in poziom else 3 if "Trudny" in poziom else 2

    start = st.text_input('Wpisz "Elo żelo" aby rozpocząć')

    if start.strip().lower() == "elo żelo":
        st.session_state.punkty = 0
        st.session_state.show_next = True
        st.session_state.start_time = datetime.now()
        st.rerun()

# --- EKRAN GRY ---
else:
    st.title("START!!!")

    # Autoodświeżanie co 0.5s
    st_autorefresh(interval=100, key="elozelo_timer_tick")

    # Czas
    czas = st.session_state.czas
    start_time = st.session_state.start_time
    elapsed = (datetime.now() - start_time).total_seconds()
    remaining = round(max(0, czas - elapsed), 2)

    # Pasek + licznik
    st.progress((czas - remaining) / max(czas, 0.1))
    st.write(f"Pozostało: {remaining:.2f} s (limit: {czas:.2f} s)")

    # Reset inputa – ZANIM go wyrenderujemy
    if st.session_state.reset_input:
        st.session_state.input_key = f"turniej_input_{datetime.now().timestamp()}"
        st.session_state.reset_input = False
        st.rerun()

    # Input działa, dopóki jest czas
    if remaining > 0:
        wpis = st.text_input("Pisz!", key=st.session_state.input_key)
        if wpis.strip().lower() == "elo żelo":
            st.session_state.start_time = datetime.now()
            st.session_state.punkty += 1
            # 🎯 ODEJMIJ CZAS (coraz szybciej!)
            st.session_state.czas = max(0.5, st.session_state.czas - 0.1)
            st.session_state.reset_input = True
            st.rerun()
    else:
        st.markdown("<h2 style='color:red;'>💀 KONIEC CZASU!</h2>", unsafe_allow_html=True)
        st.text_input("Pisz!", value="Czas minął!", disabled=True)
        if st.button("Spróbuj jeszcze raz"):
            st.session_state.show_next = False
            st.session_state.start_time = None
            st.session_state.input_key = "turniej_input_0"
            st.rerun()

    st.write("Twój wynik:", st.session_state.punkty)
    st.write(f"Obecny limit czasu: {st.session_state.czas:.2f} s")
