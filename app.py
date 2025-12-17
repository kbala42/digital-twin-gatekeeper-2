import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# -----------------------------
# 0. Page Config & The Hook
# -----------------------------
st.set_page_config(page_title="Case 14: Holmes' Final Verdict", page_icon="🛡️", layout="wide")

st.title("🛡️ Case 14: The Digital Twin Gatekeeper")

# Görsel notunu kaldırdım, sadece açıklama:
st.markdown("""
**Detective Watson's Diary - December 31, 1895**

*“After the accident, Holmes said, ‘An engineer doesn’t just solve the problem, Watson, he also knows the cost of his solution.’”
Our task is no longer just to avoid crashing into a wall. It's to find the **right balance** between Speed, Safety and Energy."*

**Task:** Analyze the accident, manage the energy, and attend the "Commissioning Meeting" with the Gatekeeper.
""")
st.markdown("---")

# -----------------------------
# 1. Sidebar - Detective Stages
# -----------------------------
st.sidebar.header("🕵️‍♂️ Investigation Files")

stage = st.sidebar.radio(
    "Case Stage:",
    ["1. Scene: Accident Analysis",
     "2. Engineering Intuition: Feel the Energy",
     "3. Gatekeeper: Decision Meeting"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🏗️ Robot Parameters")

x_ref = 1.0
x_min, x_max = -0.5, 1.5
v_max = 2.5

# -----------------------------
# SIMULATION ENGINE
# -----------------------------
def simulate_cart(m, c, Kp, Kd, x_ref, x0=0, v0=0, t_max=5.0, dt=0.01):
    n_steps = int(t_max / dt)
    t = np.linspace(0, t_max, n_steps)
    x = np.zeros(n_steps); x[0] = x0
    v = np.zeros(n_steps); v[0] = v0
    u = np.zeros(n_steps)
    energy = np.zeros(n_steps) # Kinetic Energy

    for k in range(n_steps - 1):
        e = x_ref - x[k]
        u_val = Kp * e - Kd * v[k]
        u[k] = np.clip(u_val, -50, 50)
        
        # F = ma -> a = F/m
        a = (-c * v[k] + u[k]) / m
        
        v[k+1] = v[k] + a * dt
        x[k+1] = x[k] + v[k] * dt
        
        # Energy (1/2 * m * v^2) - For a simple indicator
        energy[k+1] = 0.5 * m * v[k+1]**2
        
    return t, x, v, u, energy

# -----------------------------
# STAGE 1: SCENE OF THE INCIDENT (Active Diagnosis)
# -----------------------------
if stage == "1. Scene: Accident Analysis":
    st.sidebar.info("Mod: Evidence Gathering.")

    m_twin, c_twin = 2.0, 1.0
    m_true, c_true = 2.5, 0.2
    Kp, Kd = 15.0, 2.0

    t, x_twin, v_twin, u_twin, e_twin = simulate_cart(m_twin, c_twin, Kp, Kd, x_ref)
    t, x_true, v_true, u_true, e_true = simulate_cart(m_true, c_true, Kp, Kd, x_ref)

    st.subheader("🔍 Crime Scene Investigation")

    col1, col2 = st.columns([2, 1])
    with col1:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.fill_between(t, x_max, 2.0, color='red', alpha=0.1, label="Wall (Accident)")
        ax.plot(t, x_twin, 'b--', linewidth=2, label="Expected (Twin)")
        ax.plot(t, x_true, 'r-', linewidth=3, label="Actual")
        ax.axhline(x_ref, color='k', linestyle=':', label="Target")
        ax.legend()
        st.pyplot(fig)

    with col2:
        st.markdown("### 📝 Detective Questions")
        answer = st.radio("Where did the two lines start to diverge?", 
                          ["I don't know yet", "at 0.5 seconds", "at 1.5 seconds", "at 3.0 seconds"])

        if answer == "at 1.5 seconds":
            st.success("✅ **CORRECT!** At this point, 'Lack of Friction' manifests itself.")
        elif answer != "I don't know yet":
            st.warning("Look again, Watson. There was no difference when the robot sped up, but it couldn't slow down when it should have.")

# -----------------------------
# STAGE 2: FEEL THE ENERGY (Physical Intuition)
# -----------------------------
elif stage == "2. Engineering Intuition: Feel the Energy":
    st.sidebar.warning("Mode: Feel the Physics.")
    st.sidebar.markdown("**Task:** Monitor how the KD (Brake) parameter absorbs 'Kinetic Energy'.")

    Kp = st.sidebar.slider("Engine Power (Kp)", 1.0, 50.0, 20.0)
    Kd = st.sidebar.slider("Brake Power (Kd)", 0.0, 20.0, 2.0)

    # Simulation (On a Real Robot)
    m_real = 2.5  # Heavy robot
    c_real = 0.2  # Slippery surface
    t, x, v, u, energy = simulate_cart(m_real, c_real, Kp, Kd, x_ref)

    col1, col2 = st.columns([2, 1])

    with col1:
        # Position
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(t, x, 'b-', linewidth=2, label="Position")
        ax.fill_between(t, x_max, 2.0, color='red', alpha=0.1, label="Wall")
        ax.axhline(x_ref, color='k', linestyle=':')
        ax.legend()
        st.pyplot(fig)

        # ENERGY INDICATOR
        # Hata veren görsel etiketi buradan kaldırıldı.
        fig2, ax2 = plt.subplots(figsize=(8, 3))
        ax2.fill_between(t, 0, energy, color='orange', alpha=0.4, label="Dangerous Energy")
        ax2.set_ylabel("Joule")
        ax2.legend()
        st.pyplot(fig2)

    with col2:
        st.markdown("### 🧠 Holmes's Lesson")
        if np.max(energy) > 5.0 and Kd < 5.0:
            st.error("🔥 **High Energy!** The robot has accumulated too much energy, and the brakes (Kd) aren't enough to dissipate it. A collision with the wall is inevitable.")
        elif Kd > 10.0:
            st.success("🧊 **Strong Braking:** Look at the orange graph. Energy is rapidly dissipating. High Kd is swallowing momentum.")
        else:
            st.info("Kp is the gas pedal, it loads energy. Kd is the brake pedal, it absorbs energy. Find the balance.")

# -----------------------------
# STAGE 3: GATEKEEPER MEETING
# -----------------------------
elif stage == "3. Gatekeeper: Decision Meeting":
    st.sidebar.success("Mod: Negotiation")
    st.sidebar.markdown("**Task:** Defend the design. It's not enough for it to just be 'safe,' it's important what it does.")

    Kp = st.sidebar.slider("Final Kp", 1.0, 50.0, 25.0)
    Kd = st.sidebar.slider("Final Kd", 0.0, 20.0, 8.0)

    # Simulation
    m_worst = 2.0 * 1.2
    c_worst = 0.5 * 0.7
    t, x, v, u, e = simulate_cart(m_worst, c_worst, Kp, Kd, x_ref)

    # Metrics
    margin_pos = x_max - np.max(x)
    
    # Settling time logic corrected
    error_margin = 0.05
    in_zone = np.abs(x - x_ref) < error_margin
    # Find the last time it was OUT of the zone
    if np.any(~in_zone):
        last_out_idx = np.where(~in_zone)[0][-1]
        settling_time = t[last_out_idx]
    else:
        settling_time = 0.0
        
    # Cost calculation corrected
    u_cost = np.sum(np.abs(u)) * 0.01 

    st.subheader("🛡️ Gatekeeper Decision Panel")

    c1, c2, c3 = st.columns(3)

    # 1. Security
    c1.metric("Safety Margin", f"{margin_pos:.2f} m")
    if margin_pos > 0.2:
        c1.success("Perfect")
    elif margin_pos > 0:
        c1.warning("Risky")
    else: 
        c1.error("ACCIDENT")

    # 2. Speed (Efficiency)
    c2.metric("Arrival Time", f"{settling_time:.2f} s")
    if settling_time < 1.5:
        c2.success("Fast")
    elif settling_time < 3.0:
        c2.warning("Medium")
    else: 
        c2.error("Slow")

    # 3. Cost
    c3.metric("Energy Cost", f"£{u_cost:.0f}")
    if u_cost < 50:
        c3.success("Cheap")
    else: 
        c3.warning("Expensive")

    st.markdown("---")

    # CONTEXTUAL DECISION
    st.write("### 🏛️ Final Decision:")

    if margin_pos <= 0:
        st.error("⛔ **REJECTED:** Security breach. Discussion closed.")
    elif margin_pos > 0.2 and settling_time > 3.0:
        st.info("⚠️ **CONDITIONAL APPROVAL:** This design is suitable for 'Fragile Glass Handling'. However, it is too slow for the 'Fast Packaging' line.")
    elif margin_pos > 0.1 and settling_time < 1.5:
        st.success("✅ **FULL APPROVAL:** This design is perfect for 'High-Speed Logistics'. The energy cost is a bit high, but the speed makes it worthwhile.")
    else:
        st.warning("🤔 **REVIEW:** The design works, but it doesn't stand out in any area (Speed or Safety).")

# -----------------------------
# Holmes' Guide
# -----------------------------
with st.expander("📚 Holmes's Notes: The Art of Compromise"):
    st.markdown("""
    **There is no perfection in engineering, only balance:**
    * If you make it safer, it will slow down.
    * If you do it faster, you expend energy and the risk increases.
    * **Your job:** To know what the customer wants (Speed? Security?) and design accordingly.
    """)