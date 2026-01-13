import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Smell Sense Dashboard",
    layout="wide"
)

# ---------- STYLES (ONLY FONT WEIGHT CHANGE) ----------
/* FORCE TEXT VISIBILITY */
html, body, [class*="css"] {
    color: #2d1b3d !important;
    opacity: 1 !important;
}

/* Headings darker */
h1, h2, h3, h4 {
    color: #2a1538 !important;
    font-weight: 800 !important;
}

/* Table text */
table, th, td {
    color: #2d1b3d !important;
    opacity: 1 !important;
}

/* Slider labels */
label, span {
    color: #2d1b3d !important;
    opacity: 1 !important;
}
st.markdown(
    """
    <style>
    h1, h2, h3, h4, h5, h6,
p, span, label, div, th, td {
    color: #3b3651 !important;
}

thead th {
    color: #2f2b45 !important;
    font-weight: 700;
}
    .stApp { background-color: #ede7f6; }

    h1, h2, h3, h4 {
        font-weight: 700;
    }

    table, thead, tbody, tr, th, td {
        font-weight: 600;
    }

    .molecule {
        position: fixed;
        border-radius: 50%;
        opacity: 0.25;
        animation: float 20s infinite ease-in-out;
        z-index: 0;
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-30px); }
        100% { transform: translateY(0px); }
    }
    </style>

    <div class="molecule" style="width:16px;height:16px;background:#b39ddb;top:15%;left:12%;"></div>
    <div class="molecule" style="width:22px;height:22px;background:#9575cd;top:45%;left:82%;"></div>
    <div class="molecule" style="width:14px;height:14px;background:#ce93d8;top:70%;left:35%;"></div>
    """,
    unsafe_allow_html=True
)

# ---------- TITLE ----------
st.markdown(
    "<h1 style='text-align:center;'>Smell Sense Dashboard</h1>",
    unsafe_allow_html=True
)

voc_names = ["Acetone", "Isoprene", "Ethanol", "Ammonia", "Methane"]

disease_signatures = {
    "Healthy Breath": [0.2, 0.3, 0.1, 0.2, 0.2],
    "Asthma":         [0.2, 0.8, 0.1, 0.3, 0.3],
    "Diabetes":       [0.9, 0.3, 0.2, 0.4, 0.4],
    "Lung Cancer":    [0.4, 0.2, 0.5, 0.6, 0.6],
}

reference_levels = dict(zip(voc_names, disease_signatures["Healthy Breath"]))

left_col, right_col = st.columns([1.1, 1])

# ---------- LEFT ----------
with left_col:
    st.subheader("🧬 Disease Signature Reference")

    df = pd.DataFrame.from_dict(
        disease_signatures,
        orient="index",
        columns=voc_names
    )

    st.table(df.applymap(lambda x: f"{x:.1f}"))

    st.subheader("✏️ Build Your Own VOC Fingerprint")

    input_levels = {}
    for voc in voc_names:
        input_levels[voc] = st.slider(
            voc, 0.0, 1.0, reference_levels[voc], 0.01
        )

# ---------- RIGHT ----------
with right_col:
    st.subheader("🫁 Breath Radar")

    radar_r = list(input_levels.values())
    radar_theta = voc_names

    radar_r_closed = radar_r + [radar_r[0]]
    radar_theta_closed = radar_theta + [radar_theta[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=radar_r_closed,
            theta=radar_theta_closed,
            fill="toself",
            line=dict(color="#5e35b1"),
            fillcolor="rgba(94,53,177,0.3)"
        )
    )

    # ✅ ONLY CHANGE HERE: FULLY TRANSPARENT RADAR BACKGROUND
    fig.update_layout(
        polar=dict(
            radialaxis=dict(range=[0, 1], showgrid=True),
            bgcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    def similarity(a, b):
        return 1 - sum(abs(a[i] - b[i]) for i in range(len(a))) / len(a)

    user_vector = list(input_levels.values())
    scores = {d: similarity(user_vector, v) for d, v in disease_signatures.items()}

    best_match = max(scores, key=scores.get)
    best_score = scores[best_match]

    st.subheader("Similarity Score")
    st.markdown(
        f"<h2 style='color:#5e35b1;'>{best_score*100:.1f}%</h2>"
        f"<p><b>Closest Match:</b> {best_match}</p>",
        unsafe_allow_html=True
    )
