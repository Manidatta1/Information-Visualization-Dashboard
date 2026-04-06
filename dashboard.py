"""
U.S. Chronic Disease Indicators — Streamlit Dashboard (No-Scroll Layout)
INFO 4602/5602 | Individual Project

Install:  pip install streamlit pandas matplotlib
Run:      streamlit run dashboard.py
Data:     Place U_S__Chronic_Disease_Indicators.csv in the same folder.
"""

import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="U.S. Chronic Disease Indicators",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .block-container {
      padding-top: 0.30rem !important;
      padding-bottom: 0rem !important;
      padding-left: 0.8rem !important;
      padding-right: 0.8rem !important;
      max-width: 100% !important;
  }
  header[data-testid="stHeader"] { display: none !important; }
  .stApp { background-color: #0B1F3A !important; color: #E8EFF4; }
  section[data-testid="stSidebar"] { background-color: #0D2640; }
  [data-testid="column"] { padding: 0 3px !important; }

  .kpi {
      background: #1A3550;
      border-radius: 6px;
      padding: 4px 6px 3px 6px;
      text-align: center;
      line-height: 1.15;
  }
  .kv { font-size: 1rem; font-weight: 800; color: #00A8CC; }
  .kl { font-size: 0.60rem; color: #FFFFFF; }

  hr { margin: 2px 0 !important; border-color: #1E3050; }

  h3 {
      margin: 0 0 1px 0 !important;
      padding: 0 !important;
      font-size: 0.72rem !important;
      color: #8FA8BF !important;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
  }

  [data-testid="stImage"] { margin: 0 !important; }
  div[data-testid="stVerticalBlock"] > div { gap: 0 !important; }

  div[data-baseweb="select"] > div {
      min-height: 32px !important;
  }

    .filter-title {
        color: #E8EFF4 !important;
        font-size: 0.68rem;
        font-weight: 700;
        margin: 0 0 0.20rem 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    [data-testid="stCheckbox"] {
        margin-bottom: -0.15rem !important;
    }

    [data-testid="stCheckbox"] label,
    [data-testid="stCheckbox"] label p,
    [data-testid="stCheckbox"] div {
        color: #E8EFF4 !important;
        opacity: 1 !important;
    }

    [data-testid="stCheckbox"] svg {
        fill: #E8EFF4 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Colours ────────────────────────────────────────────────────────────────
BG      = '#0D1B2A'
CARD    = '#1A2E45'
ACC1    = '#00A8CC'
ACC2    = '#F4A261'
ACC3    = '#E63946'
ACC4    = '#2EC4B6'
TEXT    = '#E8EFF4'
MUTED   = '#8FA8BF'
LABEL = '#D7E3EA'
VALUE = '#F3F4F6'
PALETTE = [ACC3, ACC2, ACC1, ACC4, '#FFBE0B', '#8338EC', '#FB5607']

plt.rcParams.update({
    'figure.facecolor': BG,
    'axes.facecolor': CARD,
    'axes.edgecolor': CARD,
    'axes.labelcolor': TEXT,
    'xtick.color': MUTED,
    'ytick.color': MUTED,
    'text.color': TEXT,
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.spines.left': False,
    'axes.spines.bottom': False,
    'grid.color': '#1E3050',
    'grid.linewidth': 0.5,
    'figure.dpi': 110,
})

EXCL = {'Virgin Islands', 'Puerto Rico', 'Guam', 'United States'}

# ── Data ───────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv('U.S._Chronic_Disease_Indicators.csv', low_memory=False)

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ Place `U_S__Chronic_Disease_Indicators.csv` in the same folder and restart.")
    st.stop()

# Keep only 2019–2022
df = df[df['YearStart'].between(2019, 2022)].copy()

years_all = sorted(df['YearStart'].dropna().unique().tolist())

topics_map = {
    'Cardiovascular Disease':                           'Cardiovascular',
    'Nutrition, Physical Activity, and Weight Status': 'Obesity',
    'Arthritis':                                       'Arthritis',
    'Mental Health':                                   'Mental Health',
    'Diabetes':                                        'Diabetes',
    'Asthma':                                          'Asthma',
    'Chronic Obstructive Pulmonary Disease':           'COPD',
}

race_abbr = {
    'American Indian or Alaska Native, non-Hispanic': 'AI/AN',
    'Black, non-Hispanic':                            'Black NH',
    'Hispanic':                                       'Hispanic',
    'Hawaiian or Pacific Islander, non-Hispanic':     'Pacific Isl.',
    'Multiracial, non-Hispanic':                      'Multiracial',
    'White, non-Hispanic':                            'White NH',
    'Asian, non-Hispanic':                            'Asian NH',
    'Asian or Pacific Islander, non-Hispanic':        'Asian/PI NH',
}

# ── Top bar ────────────────────────────────────────────────────────────────
tc, k1, k2, k3, k4, k5, fc = st.columns([3.0, 0.9, 0.9, 0.9, 0.9, 0.9, 1.1])

with tc:
    st.markdown(
        "<div style='line-height:1.15;padding-top:2px'>"
        "<span style='font-size:1.05rem;font-weight:800;color:#E8EFF4'>🏥 U.S. Chronic Disease Indicators</span><br>"
        "</div>",
        unsafe_allow_html=True
    )

with fc:
    selected_year = st.selectbox(
        "Year",
        years_all,
        index=len(years_all)-1,
        label_visibility="collapsed",
        key="yr"
    )
    st.markdown(
        f"<div style='font-size:0.58rem;color:{MUTED};text-align:center;margin-top:-6px'>📅 {selected_year}</div>",
        unsafe_allow_html=True
    )

# ── Core filtered data ─────────────────────────────────────────────────────
overall_yr = df[
    (df['Stratification1'] == 'Overall') &
    (df['DataValueType'] == 'Crude Prevalence') &
    (df['YearStart'] == selected_year)
]

def get_ranked_topics(overall_df):
    by_topic = overall_df.groupby('Topic')['DataValue'].mean().dropna()
    topic_vals = []
    for topic in topics_map.keys():
        if topic in by_topic.index:
            topic_vals.append((topic, float(by_topic[topic])))
    topic_vals = sorted(topic_vals, key=lambda x: x[1], reverse=True)
    return topic_vals

ranked_topics = get_ranked_topics(overall_yr)
top1_topic = ranked_topics[0][0] if len(ranked_topics) > 0 else 'Diabetes'
top2_topic = ranked_topics[1][0] if len(ranked_topics) > 1 else 'Cardiovascular Disease'
top1_label = topics_map.get(top1_topic, top1_topic)
top2_label = topics_map.get(top2_topic, top2_topic)
top1_prev = f"{ranked_topics[0][1]:.1f}%" if len(ranked_topics) > 0 else "—"

# ── Filter options limited to diseases available in selected year ──────────
trend_topics_available = [t for t, _ in ranked_topics]

race_topic_df = df[
    (df['StratificationCategory1'] == 'Race/Ethnicity') &
    (df['DataValueType'] == 'Crude Prevalence') &
    (df['YearStart'] == selected_year)
]
race_topics_available = [t for t in trend_topics_available if t in set(race_topic_df['Topic'].dropna())]

# Trend filter state
default_trend_topics = trend_topics_available[:4] if len(trend_topics_available) >= 4 else trend_topics_available
if (
    'trend_topics_filter' not in st.session_state or
    any(t not in trend_topics_available for t in st.session_state['trend_topics_filter']) or
    len(st.session_state['trend_topics_filter']) == 0
):
    st.session_state['trend_topics_filter'] = default_trend_topics

# Race filter state
default_race_topic = top1_topic if top1_topic in race_topics_available else (race_topics_available[0] if race_topics_available else None)
if (
    'race_topic_filter' not in st.session_state or
    st.session_state['race_topic_filter'] not in race_topics_available
):
    st.session_state['race_topic_filter'] = default_race_topic

selected_race_topic_for_kpi = st.session_state['race_topic_filter']

# ── Checkbox helpers ───────────────────────────────────────────────────────
def topic_label(topic):
    return topics_map.get(topic, topic)

def sync_trend_filters(available_topics):
    st.session_state['trend_topics_filter'] = [
        t for t in available_topics if st.session_state.get(f"trend_chk_{t}", False)
    ]

def set_single_race_filter(chosen_topic, available_topics):
    chosen_key = f"race_chk_{chosen_topic}"

    # enforce exactly one checked topic
    if not st.session_state.get(chosen_key, False):
        st.session_state[chosen_key] = True

    for t in available_topics:
        st.session_state[f"race_chk_{t}"] = (t == chosen_topic)

    st.session_state['race_topic_filter'] = chosen_topic

# sync stored selections with current-year available topics
st.session_state['trend_topics_filter'] = [
    t for t in st.session_state.get('trend_topics_filter', default_trend_topics)
    if t in trend_topics_available
]
if not st.session_state['trend_topics_filter']:
    st.session_state['trend_topics_filter'] = default_trend_topics

if st.session_state.get('race_topic_filter') not in race_topics_available:
    st.session_state['race_topic_filter'] = default_race_topic

# initialize checkbox states
for t in trend_topics_available:
    st.session_state[f"trend_chk_{t}"] = t in st.session_state['trend_topics_filter']

for t in race_topics_available:
    st.session_state[f"race_chk_{t}"] = (t == st.session_state['race_topic_filter'])

# ── KPI calculations ────────────────────────────────────────────────────────
top1_states = df[
    (df['Topic'] == top1_topic) &
    (df['Stratification1'] == 'Overall') &
    (df['DataValueType'] == 'Crude Prevalence') &
    (df['YearStart'] == selected_year)
]
top1_states = (
    top1_states.groupby('LocationDesc')['DataValue']
    .mean()
    .dropna()
    .sort_values(ascending=False)
)
top1_states = top1_states[~top1_states.index.isin(EXCL)]
top_state = top1_states.index[0] if not top1_states.empty else "—"

race_kpi = df[
    (df['Topic'] == selected_race_topic_for_kpi) &
    (df['StratificationCategory1'] == 'Race/Ethnicity') &
    (df['DataValueType'] == 'Crude Prevalence') &
    (df['YearStart'] == selected_year)
]
race_kpi = (
    race_kpi.groupby('Stratification1')['DataValue']
    .mean()
    .dropna()
    .sort_values(ascending=False)
)
highest_burden_group = (
    race_abbr.get(race_kpi.index[0], race_kpi.index[0])
    if not race_kpi.empty else "—"
)

for col, label, val in [
    (k1, "Records", "309K+"),
    (k2, "Top Disease", top1_label),
    (k3, "Prevalence", top1_prev),
    (k4, "Top State", top_state),
    (k5, "Highest Risk Group", highest_burden_group),
]:
    col.markdown(
        f"<div class='kpi'><div class='kv'>{val}</div><div class='kl'>{label}</div></div>",
        unsafe_allow_html=True
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ── Figure helpers ─────────────────────────────────────────────────────────
FW_TOP, FH_TOP = 5.25, 2.75
FW_TOP_BURDEN, FH_TOP_BURDEN = 5.25, 3.05
FW_BOTTOM, FH_BOTTOM = 7.65, 4.80

def new_fig(layout='top'):
    if layout == 'top_burden':
        fig, ax = plt.subplots(figsize=(FW_TOP_BURDEN, FH_TOP_BURDEN))
        fig.subplots_adjust(left=0.17, right=0.97, top=0.89, bottom=0.18)
    elif layout == 'top':
        fig, ax = plt.subplots(figsize=(FW_TOP, FH_TOP))
        fig.subplots_adjust(left=0.12, right=0.97, top=0.88, bottom=0.20)
    else:  # bottom row
        fig, ax = plt.subplots(figsize=(FW_BOTTOM, FH_BOTTOM))
        fig.subplots_adjust(left=0.10, right=0.98, top=0.91, bottom=0.12)
    return fig, ax

def render(fig):
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# ── ROW 1 ──────────────────────────────────────────────────────────────────
la, lb, lc = st.columns(3)
la.markdown("### National Disease Burden")
lb.markdown(f"### Top States — Highest Disease")
lc.markdown(f"### Top States — Second Highest Disease")

col1, col2, col3 = st.columns(3)

# Chart 1 — National Burden
with col1:
    by_topic = overall_yr.groupby('Topic')['DataValue'].mean().dropna()
    labels, vals = [], []
    for k, v in topics_map.items():
        if k in by_topic.index:
            labels.append(v)
            vals.append(round(by_topic[k], 1))

    if vals:
        order = np.argsort(vals)
        labels = [labels[i] for i in order]
        vals = [vals[i] for i in order]
        colors = [ACC3 if v == max(vals) else ACC1 for v in vals]

        fig, ax = new_fig(layout='top_burden')
        ax.barh(labels, vals, color=colors, height=0.55, zorder=2)
        x_pad = max(vals) * 0.12
        label_offset = max(vals) * 0.015
        ax.set_xlim(0, max(vals) + x_pad)
        ax.set_xlabel('Crude Prevalence (%)', color=LABEL, fontsize=7)
        ax.set_ylabel('Disease', color=LABEL, fontsize=7)
        ax.set_title(f'National Burden ({selected_year})', color=TEXT, fontsize=8, fontweight='bold', pad=5)
        ax.tick_params(labelsize=7, colors = LABEL)
        ax.grid(False)
        for bar, val in zip(ax.patches, vals):
            ax.text(val + label_offset, bar.get_y() + bar.get_height()/2,
                    f'{val}%', va='center', color=TEXT, fontsize=6)
        render(fig)

# Chart 2 — Top States for Top Disease 1
with col2:
    d1 = df[
        (df['Topic'] == top1_topic) &
        (df['Stratification1'] == 'Overall') &
        (df['DataValueType'] == 'Crude Prevalence') &
        (df['YearStart'] == selected_year)
    ]
    top_s = (
        d1.groupby('LocationDesc')['DataValue']
        .mean()
        .dropna()
        .sort_values(ascending=False)
    )
    top_s = top_s[~top_s.index.isin(EXCL)].head(8)

    if not top_s.empty:
        fig, ax = new_fig(layout='top')
        clrs = [ACC3 if i == 0 else ACC1 for i in range(len(top_s))]
        ax.bar(top_s.index, top_s.values, color=clrs, width=0.6, zorder=2)
        y_pad = max(top_s.values) * 0.10
        label_offset = max(top_s.values) * 0.02
        ax.set_ylim(0, max(top_s.values) + y_pad)
        ax.set_ylabel('Prevalence (%)', color=LABEL, fontsize=7)
        ax.set_title(f'Top 8 States — {top1_label} ({selected_year})', color=TEXT, fontsize=8, fontweight='bold', pad=5)
        ax.set_xlabel('State', color=LABEL, fontsize=7)
        ax.tick_params(axis='x', labelsize=5.8, colors = LABEL)
        ax.tick_params(axis='y', labelsize=7, colors = LABEL)
        plt.setp(ax.get_xticklabels(), rotation=0, ha='center')
        ax.grid(False)
        for bar, val in zip(ax.patches, top_s.values):
            ax.text(bar.get_x() + bar.get_width()/2, val + label_offset,
                    f'{val:.1f}%', ha='center', color=TEXT, fontsize=6)
        render(fig)

# Chart 3 — Top States for Top Disease 2
with col3:
    d2 = df[
        (df['Topic'] == top2_topic) &
        (df['Stratification1'] == 'Overall') &
        (df['DataValueType'] == 'Crude Prevalence') &
        (df['YearStart'] == selected_year)
    ]
    cs = (
        d2.groupby('LocationDesc')['DataValue']
        .mean()
        .dropna()
        .sort_values(ascending=False)
    )
    cs = cs[~cs.index.isin(EXCL)].head(8)

    if not cs.empty:
        fig, ax = new_fig(layout='top')
        clrs = [ACC3 if i == 0 else ACC1 for i in range(len(cs))]
        ax.bar(cs.index, cs.values, color=clrs, width=0.6, zorder=2)
        y_pad = max(cs.values) * 0.10
        label_offset = max(cs.values) * 0.02
        ax.set_ylim(0, max(cs.values) + y_pad)
        ax.set_ylabel('Prevalence (%)', color=LABEL, fontsize=7)
        ax.set_title(f'Top 8 States — {top2_label} ({selected_year})', color=TEXT, fontsize=8, fontweight='bold', pad=5)
        ax.set_xlabel('State', color=VALUE, fontsize=7)
        ax.tick_params(axis='x', labelsize=5.8, colors = LABEL)
        ax.tick_params(axis='y', labelsize=7, colors = LABEL)
        plt.setp(ax.get_xticklabels(), rotation=0, ha='center')
        ax.grid(False)
        for bar, val in zip(ax.patches, cs.values):
            ax.text(bar.get_x() + bar.get_width()/2, val + label_offset,
                    f'{val:.1f}%', ha='center', color=TEXT, fontsize=6)
        render(fig)

st.markdown("<hr>", unsafe_allow_html=True)

# ── ROW 2 ──────────────────────────────────────────────────────────────────
ld, lf, lg = st.columns([2.5, 2.5, 1.0])
ld.markdown("### Trends 2019–2022")
lf.markdown("### Disease by Race/Ethnicity")
lg.markdown("### Filters")

col6, col4, colf = st.columns([2.5, 2.5, 1.0])

# filter panel on the right
with colf:
    fc1, fc2 = st.columns(2)

    with fc1:
        st.markdown("<div class='filter-title'>Trend Diseases</div>", unsafe_allow_html=True)
        for topic in trend_topics_available:
            st.checkbox(
                topic_label(topic),
                key=f"trend_chk_{topic}",
                on_change=sync_trend_filters,
                args=(trend_topics_available,)
            )

    with fc2:
        st.markdown("<div class='filter-title'>Race/Ethnicity</div>", unsafe_allow_html=True)
        for topic in race_topics_available:
            st.checkbox(
                topic_label(topic),
                key=f"race_chk_{topic}",
                on_change=set_single_race_filter,
                args=(topic, race_topics_available)
            )

selected_trend_topics = st.session_state['trend_topics_filter']
selected_race_topic = st.session_state['race_topic_filter']

# Chart 4 — Trends
with col4:
    fig, ax = new_fig(layout='bottom')
    for i, topic in enumerate(selected_trend_topics):
        td = df[
            (df['Topic'] == topic) &
            (df['Stratification1'] == 'Overall') &
            (df['DataValueType'] == 'Crude Prevalence')
        ]
        yr_d = td.groupby('YearStart')['DataValue'].mean().dropna()
        if not yr_d.empty:
            ax.plot(
                yr_d.index,
                yr_d.values,
                color=PALETTE[i % len(PALETTE)],
                marker='o',
                linewidth=1.8,
                markersize=3.5,
                label=topic_label(topic)
            )

    ax.set_xlabel('Year', color=LABEL, fontsize=7)
    ax.set_ylabel('Crude Prev. (%)', color=LABEL, fontsize=7)
    ax.set_title('Disease Trends (2019–2022)', color=TEXT, fontsize=8, fontweight='bold', pad=5)
    ax.tick_params(labelsize=7)
    ax.tick_params(axis='x', labelsize=7, colors=LABEL)
    ax.tick_params(axis='y', labelsize=7, colors=LABEL)
    ax.grid(False)
    ax.set_xlim(2019, 2022)
    ax.set_xticks([2019, 2020, 2021, 2022])
    if selected_trend_topics:
        ax.legend(
            facecolor=CARD,
            edgecolor=CARD,
            labelcolor=TEXT,
            fontsize=6,
            loc='upper left',
            handlelength=1.0,
            borderpad=0.3
        )
    render(fig)

# Chart 5 — Disease by Race/Ethnicity
with col6:
    race = df[
        (df['Topic'] == selected_race_topic) &
        (df['StratificationCategory1'] == 'Race/Ethnicity') &
        (df['DataValueType'] == 'Crude Prevalence') &
        (df['YearStart'] == selected_year)
    ] if selected_race_topic else pd.DataFrame()

    race_g = (
        race.groupby('Stratification1')['DataValue']
        .mean()
        .dropna()
        .sort_values(ascending=False)
    )

    if not race_g.empty:
        race_g.index = [race_abbr.get(i, i) for i in race_g.index]

        fig, ax = new_fig(layout='bottom')
        y = np.arange(len(race_g))
        vals = race_g.values
        labels = race_g.index.tolist()
        colors = [ACC3 if i == 0 else ACC1 for i in range(len(vals))]

        ax.hlines(y=y, xmin=0, xmax=vals, color=ACC1, linewidth=2.5, zorder=1)
        ax.scatter(vals, y, s=70, color=colors, zorder=2)

        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=7)
        ax.tick_params(axis='x', labelsize=7, colors=LABEL)
        ax.tick_params(axis='y', labelsize=7, colors=LABEL)
        ax.invert_yaxis()
        ax.set_xlabel('Crude Prevalence (%)', color=LABEL, fontsize=7)
        ax.set_ylabel('Race/Ethnicity', color=LABEL, fontsize=7)
        ax.set_title(f'{topic_label(selected_race_topic)} by Race/Ethnicity ({selected_year})', color=TEXT, fontsize=8, fontweight='bold', pad=5)
        ax.grid(False)
        x_pad = max(vals) * 0.14
        label_offset = max(vals) * 0.02
        ax.set_xlim(0, max(vals) + x_pad)

        for x, yy in zip(vals, y):
            ax.text(x + label_offset, yy, f'{x:.1f}%', va='center', color=VALUE, fontsize=6)

        render(fig)

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown(
    "<div style='text-align:center;color:#FFFFFF;font-size:0.58rem;padding:1px 0'>"
    "Data Source: CDC Chronic Disease Indicators (CDI), data.cdc.gov"
    "</div>",
    unsafe_allow_html=True,
)