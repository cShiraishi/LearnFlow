import streamlit as st
import time
from stats_manager import add_xp

def render_pomodoro_timer():
    st.markdown("<h2 class='text-gradient'>🍅 Pomodoro Focus</h2>", unsafe_allow_html=True)
    
    # Initialize Session State Variables
    if 'pomo_time_left' not in st.session_state:
        st.session_state.pomo_time_left = 25 * 60
    if 'pomo_is_running' not in st.session_state:
        st.session_state.pomo_is_running = False
    if 'pomo_mode' not in st.session_state:
        st.session_state.pomo_mode = "Work"  # Work or Break

    # Settings Expander
    with st.expander("⚙️ Timer Settings"):
        work_duration = st.number_input("Work Duration (minutes)", min_value=1, max_value=60, value=25)
        break_duration = st.number_input("Break Duration (minutes)", min_value=1, max_value=30, value=5)

    # Timer Logic Helpers
    def start_timer():
        st.session_state.pomo_is_running = True
        
    def pause_timer():
        st.session_state.pomo_is_running = False
        
    def reset_timer():
        st.session_state.pomo_is_running = False
        st.session_state.pomo_mode = "Work"
        st.session_state.pomo_time_left = work_duration * 60

    def switch_mode():
        if st.session_state.pomo_mode == "Work":
            st.session_state.pomo_mode = "Break"
            st.session_state.pomo_time_left = break_duration * 60
        else:
            st.session_state.pomo_mode = "Work"
            st.session_state.pomo_time_left = work_duration * 60
        st.session_state.pomo_is_running = False

    # Main Timer Display
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Determine Color based on mode
        color = "#ef233c" if st.session_state.pomo_mode == "Work" else "#70e000"
        mode_icon = "🧠" if st.session_state.pomo_mode == "Work" else "☕"
        
        st.markdown(f"<h3 style='text-align: center; color: {color};'>{mode_icon} {st.session_state.pomo_mode} Mode</h3>", unsafe_allow_html=True)
        
        # Calculate time string
        mins, secs = divmod(st.session_state.pomo_time_left, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        
        # Big Timer Text
        st.markdown(f"""
        <div style="
            text-align: center; 
            font-size: 6rem; 
            font-weight: 900; 
            font-family: 'Outfit', sans-serif; 
            color: #edf6f9;
            text-shadow: 0 0 20px {color};
            margin-top: -20px;
            margin-bottom: 20px;
        ">
            {time_str}
        </div>
        """, unsafe_allow_html=True)

    # Controls
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("▶ START", use_container_width=True, type="primary"):
            start_timer()
            st.rerun()
    with c2:
        if st.button("⏸ PAUSE", use_container_width=True):
            pause_timer()
            st.rerun()
    with c3:
        if st.button("🔁 RESET", use_container_width=True):
            reset_timer()
            st.rerun()
    with c4:
        if st.button("Next Mode ⏭", use_container_width=True):
            switch_mode()
            st.rerun()

    # Countdown Visuals (ProgressBar)
    total_time = (work_duration * 60) if st.session_state.pomo_mode == "Work" else (break_duration * 60)
    progress = 1 - (st.session_state.pomo_time_left / total_time)
    st.progress(min(max(progress, 0.0), 1.0))

    # Auto-Countdown Logic
    if st.session_state.pomo_is_running:
        if st.session_state.pomo_time_left > 0:
            time.sleep(1) # Wait 1 second
            st.session_state.pomo_time_left -= 1
            st.rerun() # Force refresh to update display
        else:
            # Timer Finished
            st.session_state.pomo_is_running = False
            st.balloons()
            st.success(f"{st.session_state.pomo_mode} Session Complete!")
