# ================================================================
# MUTUAL FUND INDUSTRY PERFORMANCE DASHBOARD - INDIA
# Project: Assignment 08
# Run: py -m streamlit run mutual_fund_advanced_dashboard.py
# ================================================================

from pathlib import Path
from io import BytesIO
import re
import math

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------- CONFIG -----------------------------

st.set_page_config(
    page_title="NEXUS 2050 | Mutual Fund Intelligence",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# FUTURE-FORWARD VISUAL SYSTEM — deep-space navy, glass panels, neon accents.
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    :root { --bg0:#050816; --bg1:#0a1025; --panel:rgba(15,25,52,.78); --line:rgba(101,224,255,.22); --cyan:#65e0ff; --mint:#67f5c5; --violet:#a78bfa; --muted:#9fb1d0; }
    html, body, [class*="css"] { font-family:'Space Grotesk',sans-serif; }
    .stApp { background: radial-gradient(ellipse at 12% 0%, rgba(44,91,180,.25), transparent 36%), radial-gradient(ellipse at 92% 8%, rgba(126,58,242,.17), transparent 30%), linear-gradient(145deg,var(--bg0) 0%,var(--bg1) 52%,#080d1d 100%); color:#edf5ff; }
    [data-testid="stHeader"] { background:rgba(5,8,22,.68); backdrop-filter:blur(14px); }
    [data-testid="stSidebar"] { background:linear-gradient(180deg,rgba(9,17,39,.98),rgba(7,12,28,.98)); border-right:1px solid var(--line); }
    [data-testid="stSidebar"] * { color:#dce9ff; }
    .block-container { padding-top:1.7rem; padding-bottom:3rem; max-width:1600px; }
    h1,h2,h3 { letter-spacing:-.035em; color:#f4f8ff; }
    h2, h3 { text-shadow:0 0 24px rgba(101,224,255,.08); }
    p, label, .stCaption { color:var(--muted); }
    [data-testid="stMetric"] { background:linear-gradient(145deg,rgba(19,34,68,.92),rgba(11,20,43,.85)); border:1px solid rgba(101,224,255,.23); border-radius:16px; padding:17px 19px; box-shadow:0 10px 30px rgba(0,0,0,.18), inset 0 1px 0 rgba(255,255,255,.04); min-height:112px; }
    [data-testid="stMetricLabel"] { color:#9fb7d9 !important; font-size:.82rem; }
    [data-testid="stMetricValue"] { color:#f4fbff !important; font-family:'DM Mono',monospace; text-shadow:0 0 18px rgba(101,224,255,.17); }
    [data-testid="stMetricDelta"] { font-family:'DM Mono',monospace; }
    [data-testid="stTabs"] [role="tablist"] { gap:7px; border-bottom:1px solid rgba(101,224,255,.18); }
    [data-testid="stTabs"] button[role="tab"] { border:1px solid transparent; border-radius:10px 10px 0 0; padding:.7rem 1rem; color:#aebfdf; }
    [data-testid="stTabs"] button[aria-selected="true"] { color:var(--cyan); border-color:rgba(101,224,255,.28); background:rgba(101,224,255,.07); }
    div[data-testid="stExpander"] { border:1px solid var(--line); border-radius:14px; background:rgba(12,22,47,.62); }
    [data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid rgba(101,224,255,.16); border-radius:12px; overflow:hidden; }
    .stButton button, .stDownloadButton button { border:1px solid rgba(101,224,255,.45); border-radius:11px; background:linear-gradient(100deg,rgba(39,100,160,.35),rgba(108,72,190,.28)); color:#eafaff; transition:all .2s ease; }
    .stButton button:hover, .stDownloadButton button:hover { border-color:var(--cyan); box-shadow:0 0 22px rgba(101,224,255,.16); transform:translateY(-1px); }
    [data-testid="stAlert"] { border-radius:12px; border:1px solid rgba(101,224,255,.22); background:rgba(12,28,55,.72); }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div { background:rgba(8,15,34,.92); border-color:rgba(101,224,255,.25); }
    hr { border-color:rgba(101,224,255,.17); }
    .nexus-hero { position:relative; overflow:hidden; padding:27px 30px 25px; margin:0 0 18px; border-radius:22px; border:1px solid rgba(101,224,255,.3); background:linear-gradient(115deg,rgba(15,39,77,.96),rgba(26,23,65,.91) 58%,rgba(14,38,59,.92)); box-shadow:0 18px 50px rgba(0,0,0,.22), inset 0 1px 0 rgba(255,255,255,.06); }
    .nexus-hero:after { content:''; position:absolute; width:310px; height:310px; right:-70px; top:-170px; border:1px solid rgba(101,224,255,.24); border-radius:50%; box-shadow:0 0 0 25px rgba(101,224,255,.025),0 0 0 55px rgba(167,139,250,.035),0 0 65px rgba(101,224,255,.14); }
    .nexus-kicker { font-family:'DM Mono',monospace; color:var(--mint); font-size:.73rem; letter-spacing:.18em; text-transform:uppercase; margin-bottom:8px; }
    .nexus-title { font-size:clamp(1.8rem,3.3vw,3.1rem); line-height:1.05; font-weight:700; letter-spacing:-.055em; color:#f4f8ff; margin:0 0 10px; }
    .nexus-title span { color:var(--cyan); text-shadow:0 0 24px rgba(101,224,255,.22); }
    .nexus-sub { color:#b8c9e6; max-width:850px; font-size:.98rem; margin:0; }
    .nexus-tags { display:flex; flex-wrap:wrap; gap:8px; margin-top:18px; }
    .nexus-tag { border:1px solid rgba(101,224,255,.24); border-radius:999px; padding:5px 10px; color:#ccefff; background:rgba(101,224,255,.06); font-family:'DM Mono',monospace; font-size:.69rem; }
    .section-eyebrow { font-family:'DM Mono',monospace; color:var(--cyan); font-size:.72rem; letter-spacing:.14em; text-transform:uppercase; margin:0 0 4px; }
    .kpi-panel { border:1px solid rgba(101,224,255,.19); border-radius:17px; padding:16px 17px 13px; background:linear-gradient(145deg,rgba(14,28,57,.78),rgba(9,17,37,.76)); min-height:154px; box-shadow:inset 0 1px 0 rgba(255,255,255,.035); }
    .kpi-label { font-family:'DM Mono',monospace; color:#9fb7d9; font-size:.70rem; letter-spacing:.09em; text-transform:uppercase; }
    .kpi-value { color:#f4fbff; font-family:'DM Mono',monospace; font-size:clamp(1.15rem,2vw,1.65rem); font-weight:600; line-height:1.35; margin:8px 0 5px; overflow-wrap:anywhere; }
    .kpi-detail { color:#a9bddb; font-size:.79rem; line-height:1.45; min-height:34px; }
    .kpi-status { display:inline-block; border-radius:999px; padding:3px 8px; font-family:'DM Mono',monospace; font-size:.65rem; letter-spacing:.04em; margin-top:9px; border:1px solid rgba(101,224,255,.24); color:#a9efff; background:rgba(101,224,255,.07); }
    .kpi-status.good { color:#8cf7d1; border-color:rgba(103,245,197,.25); background:rgba(103,245,197,.07); }
    .kpi-status.warn { color:#ffd18a; border-color:rgba(255,190,92,.25); background:rgba(255,190,92,.07); }
    @media (max-width: 700px) { .block-container { padding-left:1rem; padding-right:1rem; } .nexus-hero { padding:22px 19px; } }
    </style>
    """,
    unsafe_allow_html=True,
)

# Use a dark plotting canvas so interactive charts match the dashboard's visual system.
import plotly.io as pio
pio.templates.default = "plotly_dark"
px.defaults.template = "plotly_dark"

PROJECT_DIR = Path(r"C:\Users\Ketan Sharma\balaji project")
WORKBOOK_NAME = "Assignment_08_Mutual_Fund_Dashboard.xlsx"
DEFAULT_FILE = PROJECT_DIR / WORKBOOK_NAME
if not DEFAULT_FILE.exists():
    # Also works if the workbook and script are stored together elsewhere.
    DEFAULT_FILE = Path(__file__).resolve().parent / WORKBOOK_NAME

CATEGORY_SHEET = "Category Data"
SCHEME_SHEET = "Scheme Data"
SECTOR_SHEET = "Sector Summary"

MONEY_COLS = [
    "Funds Mobilised (₹ cr)",
    "Redemptions (₹ cr)",
    "Net Flows (₹ cr)",
    "Net AUM (₹ cr)",
    "Avg AUM (₹ cr)",
    "SIP Inflows (₹ cr)",
]
NUMERIC_CANDIDATES = MONEY_COLS + [
    "No. of Schemes", "Folio Count"
]

CATEGORY_SOURCE = (
    "https://www.sebi.gov.in/statistics/mutual-fund/objective/"
    "apr-sep-2026.html"
)
SECTOR_SOURCE = (
    "https://www.sebi.gov.in/statistics/mutual-fund/rmmf-archive/"
    "apr-sep-2026.html"
)
SEBI_LANDING = "https://www.sebi.gov.in/statistics/mutual-fund.html"

# -------------------------- DATA FUNCTIONS ------------------------

def standardize_text_columns(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].map(
            lambda x: x.strip() if isinstance(x, str) else x
        )
        df[col] = df[col].replace("", np.nan)
    return df


def numeric_clean(series):
    """Convert formatted numeric strings to numbers without inventing values."""
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce")
    values = (
        series.astype("string")
        .str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.replace("\u2212", "-", regex=False)
        .str.strip()
    )
    values = values.replace(
        {"": pd.NA, "—": pd.NA, "-": pd.NA, "NA": pd.NA, "N/A": pd.NA}
    )
    return pd.to_numeric(values, errors="coerce")


def clean_financial_table(raw, label_col="Scheme Category"):
    df = standardize_text_columns(raw)
    df = df.dropna(how="all").dropna(axis=1, how="all")
    before_dedup = len(df)
    df = df.drop_duplicates().copy()
    duplicates_removed = before_dedup - len(df)

    if label_col not in df.columns:
        raise ValueError(
            f"Expected label column '{label_col}' was not found. "
            f"Columns found: {list(df.columns)}"
        )

    df[label_col] = df[label_col].astype("string").str.strip()
    invalid_labels = df[label_col].isna() | df[label_col].eq("")
    # Remove only rows with no usable category/scheme label.
    df = df.loc[~invalid_labels].copy()

    for col in df.columns:
        if col != label_col:
            df[col] = numeric_clean(df[col])

    # Do not remove legitimate negative net flows.
    quality = {
        "Rows in source table": len(raw),
        "Rows after cleaning": len(df),
        "Duplicate rows removed": duplicates_removed,
        "Missing cells after cleaning": int(df.isna().sum().sum()),
        "Columns": len(df.columns),
    }
    return df.reset_index(drop=True), quality


def clean_sector_table(raw):
    """
    The source sector sheet has a title row, then column headers,
    then four metric rows and a note. Locate the header robustly.
    """
    data = raw.copy()
    data = data.dropna(how="all").reset_index(drop=True)
    if data.empty:
        return pd.DataFrame(), {
            "Rows in source table": 0,
            "Rows after cleaning": 0,
            "Duplicate rows removed": 0,
            "Missing cells after cleaning": 0,
            "Columns": 0,
        }

    header_idx = None
    for i, row in data.iterrows():
        row_values = [
            str(v).strip().lower() for v in row.tolist() if pd.notna(v)
        ]
        joined = " ".join(row_values)
        if (
            "metric" in row_values
            or (
                "private sector (₹ cr)" in joined
                and "public sector (₹ cr)" in joined
            )
        ):
            header_idx = i
            break

    if header_idx is None:
        # Fallback for sheets already read with headers.
        if "Metric" in [str(c).strip() for c in raw.columns]:
            table = standardize_text_columns(raw)
            return table, {
                "Rows in source table": len(raw),
                "Rows after cleaning": len(table),
                "Duplicate rows removed": 0,
                "Missing cells after cleaning": int(table.isna().sum().sum()),
                "Columns": len(table.columns),
            }
        raise ValueError(
            "Could not identify the sector summary header row. "
            "Expected columns including Metric, Private Sector, Public Sector."
        )

    headers = [
        str(v).strip() if pd.notna(v) else f"Unnamed_{i}"
        for i, v in enumerate(data.iloc[header_idx].tolist())
    ]
    table = data.iloc[header_idx + 1:].copy()
    table.columns = headers
    table = table.dropna(how="all")
    first_col = table.columns[0]
    table[first_col] = table[first_col].astype("string").str.strip()

    # Keep actual metric rows only; remove source footnotes and blank lines.
    table = table[
        table[first_col].notna()
        & table[first_col].ne("")
        & ~table[first_col].str.lower().str.startswith(
            ("important:", "source:", "note:"), na=False
        )
    ].copy()

    for col in table.columns[1:]:
        table[col] = numeric_clean(table[col])

    table = table.drop_duplicates().reset_index(drop=True)
    quality = {
        "Rows in source table": len(raw),
        "Rows after cleaning": len(table),
        "Duplicate rows removed": 0,
        "Missing cells after cleaning": int(table.isna().sum().sum()),
        "Columns": len(table.columns),
    }
    return table, quality


@st.cache_data(show_spinner="Loading and cleaning the Excel workbook…")
def load_workbook_data(file_path_string, file_modified):
    path = Path(file_path_string)
    if not path.exists():
        raise FileNotFoundError(f"Workbook not found: {path}")

    xls = pd.ExcelFile(path)
    required = {CATEGORY_SHEET, SCHEME_SHEET, SECTOR_SHEET}
    missing = required.difference(xls.sheet_names)
    if missing:
        raise ValueError(f"Missing required worksheets: {sorted(missing)}")

    # These two source sheets have a title row above their column headers.
    category_raw = pd.read_excel(path, sheet_name=CATEGORY_SHEET, header=1)
    scheme_raw = pd.read_excel(path, sheet_name=SCHEME_SHEET, header=1)

    # Read without headers so the sector title row does not become a column.
    sector_raw = pd.read_excel(path, sheet_name=SECTOR_SHEET, header=None)

    category, category_quality = clean_financial_table(category_raw)
    scheme, scheme_quality = clean_financial_table(scheme_raw)
    sector, sector_quality = clean_sector_table(sector_raw)

    required_category = [
        "Scheme Category", "No. of Schemes", "Folio Count",
        "Funds Mobilised (₹ cr)", "Redemptions (₹ cr)",
        "Net Flows (₹ cr)", "Net AUM (₹ cr)",
        "Avg AUM (₹ cr)", "SIP Inflows (₹ cr)",
    ]
    missing_cols = [c for c in required_category if c not in category.columns]
    if missing_cols:
        raise ValueError(
            "Category Data is missing expected columns: "
            + ", ".join(missing_cols)
            + f". Columns found: {list(category.columns)}"
        )

    required_scheme = [
        "Scheme Category", "Folio Count", "Funds Mobilised (₹ cr)",
        "Redemptions (₹ cr)", "Net Flows (₹ cr)", "Net AUM (₹ cr)",
        "SIP Inflows (₹ cr)",
    ]
    missing_scheme = [c for c in required_scheme if c not in scheme.columns]
    if missing_scheme:
        raise ValueError(
            "Scheme Data is missing expected columns: "
            + ", ".join(missing_scheme)
            + f". Columns found: {list(scheme.columns)}"
        )

    # Retain records with valid labels and meaningful financial data.
    category = category.dropna(subset=["Net AUM (₹ cr)"]).copy()
    scheme = scheme.dropna(subset=["Net AUM (₹ cr)"]).copy()

    # Derived metrics: retain the original reported fields unchanged.
    for df in (category, scheme):
        df["Redemption Ratio (%)"] = np.where(
            df["Funds Mobilised (₹ cr)"].ne(0),
            df["Redemptions (₹ cr)"] / df["Funds Mobilised (₹ cr)"] * 100,
            np.nan,
        )
        df["Net Flow / AUM (%)"] = np.where(
            df["Net AUM (₹ cr)"].ne(0),
            df["Net Flows (₹ cr)"] / df["Net AUM (₹ cr)"] * 100,
            np.nan,
        )

    total_folios = category["Folio Count"].sum(min_count=1)
    category["Folio Share (%)"] = (
        category["Folio Count"] / total_folios * 100
        if pd.notna(total_folios) and total_folios != 0
        else np.nan
    )

    quality = pd.DataFrame([
        {"Dataset": "Category Data", **category_quality},
        {"Dataset": "Scheme Data", **scheme_quality},
        {"Dataset": "Sector Summary", **sector_quality},
    ])

    return category, scheme, sector, quality, xls.sheet_names


def fmt_money(value, decimals=2):
    if pd.isna(value):
        return "N/A"
    return f"₹{value:,.{decimals}f} cr"


def fmt_number(value, decimals=0):
    if pd.isna(value):
        return "N/A"
    return f"{value:,.{decimals}f}"


def make_excel_download(category, scheme, sector, quality, stats, findings, recs):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        category.to_excel(writer, sheet_name="Category Analysis", index=False)
        scheme.to_excel(writer, sheet_name="Scheme Analysis", index=False)
        sector.to_excel(writer, sheet_name="Sector Summary", index=False)
        quality.to_excel(writer, sheet_name="Data Quality", index=False)
        stats.to_excel(writer, sheet_name="Statistical Analysis", index=False)
        findings.to_excel(writer, sheet_name="Findings", index=False)
        recs.to_excel(writer, sheet_name="Recommendations", index=False)

    output.seek(0)
    return output.getvalue()


# ------------------------------ SIDEBAR ----------------------------

st.sidebar.title("Dashboard Controls")
st.sidebar.caption("Choose a workbook and filter the category charts.")

if DEFAULT_FILE.exists():
    workbook_path = st.sidebar.text_input(
        "Excel workbook path", value=str(DEFAULT_FILE)
    )
else:
    workbook_path = st.sidebar.text_input(
        "Excel workbook path",
        value=str(Path.cwd() / WORKBOOK_NAME),
        help="Enter the full path to your Excel workbook.",
    )

if not Path(workbook_path).exists():
    st.error(
        "Excel workbook not found. Confirm the path and ensure the file is "
        "named Assignment_08_Mutual_Fund_Dashboard.xlsx."
    )
    st.stop()

try:
    modified_time = Path(workbook_path).stat().st_mtime
    category_df, scheme_df, sector_df, quality_df, sheet_names = (
        load_workbook_data(str(Path(workbook_path).resolve()), modified_time)
    )
except Exception as exc:
    st.error(f"Could not load the workbook: {exc}")
    st.info(
        "Check that the workbook is closed in Excel, the sheet names match, "
        "and the column headings have not been changed."
    )
    st.stop()

all_categories = category_df["Scheme Category"].dropna().astype(str).tolist()
selected_categories = st.sidebar.multiselect(
    "Scheme categories",
    options=all_categories,
    default=all_categories,
)
if not selected_categories:
    st.warning("Select at least one category to display the dashboard.")
    st.stop()

filtered = category_df[
    category_df["Scheme Category"].astype(str).isin(selected_categories)
].copy()

st.sidebar.divider()
st.sidebar.markdown("**Reporting periods**")
st.sidebar.caption("Category data: as of 31 Aug 2026; cumulative flows from 1 Apr–31 Aug 2026.")
st.sidebar.caption("Sector summary: cumulative flows from 1 Apr–30 Sep 2026; assets as of 30 Sep 2026.")

# ------------------------------ HEADER -----------------------------

st.markdown(
    """
    <section class="nexus-hero">
      <div class="nexus-kicker">◈ NEXUS INTELLIGENCE SYSTEM / INDIA</div>
      <div class="nexus-title">Mutual Fund <span>Command Center</span></div>
      <p class="nexus-sub">A future-facing financial intelligence cockpit for exploring assets, investor activity, flows and category-level signals — built from the supplied SEBI dataset.</p>
      <div class="nexus-tags">
        <span class="nexus-tag">● LIVE INTERACTIVE FILTERS</span>
        <span class="nexus-tag">FINANCIAL SIGNALS</span>
        <span class="nexus-tag">DATA QUALITY MONITOR</span>
        <span class="nexus-tag">ASSIGNMENT 08 · 2050 UI CONCEPT</span>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)
st.markdown('<p class="section-eyebrow">01 / reporting integrity</p>', unsafe_allow_html=True)
st.info(
    "Reporting-date caution: category data are through 31 August 2026, "
    "while the sector summary is through 30 September 2026. These are "
    "shown separately and must not be treated as a same-date comparison."
)

with st.expander("Dataset description and cleaning summary"):
    c1, c2, c3 = st.columns(3)
    c1.metric("Category rows", f"{len(category_df):,}")
    c2.metric("Selected scheme rows", f"{len(scheme_df):,}")
    c3.metric("Sector metrics", f"{len(sector_df):,}")
    st.dataframe(quality_df, width="stretch", hide_index=True)
    st.markdown(
        """
        **Preparation performed**
        - Removed completely empty rows/columns and duplicate records.
        - Trimmed whitespace from category labels and column names.
        - Converted financial fields to numeric values while preserving missing values.
        - Kept negative net flows, because they can represent outflows.
        - Retained category, selected-scheme and sector datasets separately.
        - Derived redemption ratio, net-flow-to-AUM ratio and folio share.
        """
    )

# ------------------------------- KPIs ------------------------------

def safe_sum(df, col):
    return df[col].sum(min_count=1) if col in df.columns else np.nan

def safe_div(numerator, denominator, multiplier=1.0):
    if pd.isna(numerator) or pd.isna(denominator) or denominator == 0:
        return np.nan
    return numerator / denominator * multiplier

def kpi_card(label, value, detail, status=None, status_class=""):
    status_html = (
        f'<span class="kpi-status {status_class}">{status}</span>'
        if status else ""
    )
    st.markdown(
        f"""
        <div class="kpi-panel">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-detail">{detail}</div>
          {status_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

total_aum = safe_sum(filtered, "Net AUM (₹ cr)")
total_flows = safe_sum(filtered, "Net Flows (₹ cr)")
total_folios = safe_sum(filtered, "Folio Count")
total_sip = safe_sum(filtered, "SIP Inflows (₹ cr)")
total_mobilised = safe_sum(filtered, "Funds Mobilised (₹ cr)")
total_redemptions = safe_sum(filtered, "Redemptions (₹ cr)")
total_schemes = safe_sum(filtered, "No. of Schemes")
total_avg_aum = safe_sum(filtered, "Avg AUM (₹ cr)")

redemption_ratio = safe_div(total_redemptions, total_mobilised, 100)
net_flow_aum_ratio = safe_div(total_flows, total_aum, 100)
sip_to_mobilised = safe_div(total_sip, total_mobilised, 100)
net_flow_to_mobilised = safe_div(total_flows, total_mobilised, 100)
gross_activity = (
    total_mobilised + total_redemptions
    if pd.notna(total_mobilised) and pd.notna(total_redemptions)
    else np.nan
)
aum_per_scheme = safe_div(total_aum, total_schemes)
folios_per_scheme = safe_div(total_folios, total_schemes)
aum_per_folio_lakh = safe_div(total_aum * 100, total_folios)
net_flow_per_folio_lakh = safe_div(total_flows * 100, total_folios)

positive_flow_count = int((filtered["Net Flows (₹ cr)"] > 0).sum())
negative_flow_count = int((filtered["Net Flows (₹ cr)"] < 0).sum())
zero_flow_count = int((filtered["Net Flows (₹ cr)"] == 0).sum())
valid_flow_count = int(filtered["Net Flows (₹ cr)"].notna().sum())

aum_sorted = filtered.dropna(subset=["Net AUM (₹ cr)"]).sort_values(
    "Net AUM (₹ cr)", ascending=False
)
top_aum_category = (
    str(aum_sorted.iloc[0]["Scheme Category"]) if not aum_sorted.empty else "N/A"
)
top_aum_value = (
    float(aum_sorted.iloc[0]["Net AUM (₹ cr)"]) if not aum_sorted.empty else np.nan
)
top_aum_share = safe_div(top_aum_value, total_aum, 100)
top3_aum_share = safe_div(
    aum_sorted.head(3)["Net AUM (₹ cr)"].sum(min_count=1), total_aum, 100
)
flow_sorted = filtered.dropna(subset=["Net Flows (₹ cr)"]).sort_values(
    "Net Flows (₹ cr)", ascending=False
)
top_flow_category = (
    str(flow_sorted.iloc[0]["Scheme Category"]) if not flow_sorted.empty else "N/A"
)
top_flow_value = (
    float(flow_sorted.iloc[0]["Net Flows (₹ cr)"]) if not flow_sorted.empty else np.nan
)
worst_flow = (
    float(flow_sorted.iloc[-1]["Net Flows (₹ cr)"]) if not flow_sorted.empty else np.nan
)
worst_flow_category = (
    str(flow_sorted.iloc[-1]["Scheme Category"]) if not flow_sorted.empty else "N/A"
)

def pct_text(value):
    return f"{value:,.2f}%" if pd.notna(value) else "N/A"

def number_text(value, decimals=2):
    return f"{value:,.{decimals}f}" if pd.notna(value) else "N/A"

st.markdown('<p class="section-eyebrow">02 / market telemetry</p>', unsafe_allow_html=True)
st.subheader("Advanced financial intelligence KPIs")
st.caption(
    f"Scope: {len(selected_categories)} selected categories · "
    f"{len(filtered):,} category rows · category reporting cut-off: 31 Aug 2026. "
    "All aggregates below respond to the sidebar category filter."
)

# Main dashboard: keep only the 8 decision-useful KPIs.
# Detailed ratios remain available in the KPI dictionary and analysis tabs.
st.markdown("#### Executive snapshot")
st.caption(
    "Eight high-value indicators for the selected categories. "
    "Detailed ratios and supporting metrics remain available in the analysis tabs."
)

kpi_row_1 = st.columns(4)
with kpi_row_1[0]:
    kpi_card(
        "Net assets under management (AUM)",
        fmt_money(total_aum),
        "Current reported assets across the selected categories."
    )
with kpi_row_1[1]:
    flow_status = (
        "NET INFLOW" if pd.notna(total_flows) and total_flows > 0
        else "NET OUTFLOW" if pd.notna(total_flows) and total_flows < 0
        else "FLAT / N.A."
    )
    flow_class = (
        "good" if pd.notna(total_flows) and total_flows > 0
        else "warn" if pd.notna(total_flows) and total_flows < 0
        else ""
    )
    kpi_card(
        "Net flows",
        fmt_money(total_flows),
        "Mobilised funds minus redemptions for the reported period.",
        flow_status,
        flow_class
    )
with kpi_row_1[2]:
    kpi_card(
        "SIP inflows",
        fmt_money(total_sip),
        "Reported systematic investment plan inflows for the period."
    )
with kpi_row_1[3]:
    kpi_card(
        "Investor folios",
        fmt_number(total_folios),
        "Account/folio count; not a count of unique individual investors."
    )

kpi_row_2 = st.columns(4)
with kpi_row_2[0]:
    kpi_card(
        "Funds mobilised",
        fmt_money(total_mobilised),
        "Gross funds mobilised during the reporting period."
    )
with kpi_row_2[1]:
    kpi_card(
        "Redemptions",
        fmt_money(total_redemptions),
        "Reported redemption amount during the reporting period."
    )
with kpi_row_2[2]:
    kpi_card(
        "Schemes represented",
        fmt_number(total_schemes),
        "Sum of reported scheme counts across the selected categories."
    )
with kpi_row_2[3]:
    kpi_card(
        "Top AUM category",
        top_aum_category,
        f"{fmt_money(top_aum_value)} in reported AUM · "
        f"{pct_text(top_aum_share)} of selected-category AUM."
    )

st.caption(
    "Category data are through 31 August 2026. These indicators describe the "
    "reported snapshot and are not investment returns or investment advice."
)

with st.expander("KPI dictionary — definitions, formulas and interpretation"):
    kpi_dictionary = pd.DataFrame([
        ["Net AUM", "Sum of Net AUM (₹ cr)", "Snapshot of assets; not a return measure."],
        ["Cumulative net flows", "Sum of Net Flows (₹ cr)", "Negative values are retained and indicate net outflows."],
        ["Gross flow activity", "Funds mobilised + redemptions", "Activity measure; not net inflows or asset growth."],
        ["Redemption / mobilisation", "Redemptions ÷ funds mobilised × 100", "Can exceed 100% if redemptions are higher."],
        ["SIP / mobilisation", "SIP inflows ÷ funds mobilised × 100", "Interpret cautiously; field definitions and reporting coverage matter."],
        ["Net flows / AUM", "Net flows ÷ point-in-time AUM × 100", "Descriptive ratio, not a return or forecast."],
        ["AUM per scheme", "Net AUM ÷ reported scheme count", "Simple average; schemes may differ substantially in size."],
        ["Folios per scheme", "Folio count ÷ reported scheme count", "Folios are accounts, not unique investors."],
        ["AUM per folio", "Net AUM (₹ cr) × 100 ÷ folio count", "Approximation; a folio may not equal one person."],
        ["Top 3 AUM share", "AUM of three largest selected categories ÷ selected AUM × 100", "Measures concentration within the current selection only."],
        ["Flow data coverage", "Non-missing net-flow rows ÷ selected category rows × 100", "Data availability indicator, not a quality guarantee."],
    ], columns=["KPI", "Formula", "How to interpret"])
    st.dataframe(kpi_dictionary, width="stretch", hide_index=True)
    st.warning(
        "Period alignment: category metrics are through 31 Aug 2026, while the sector summary is through 30 Sep 2026. "
        "Do not compare them as if they share the same cut-off date. These KPIs are descriptive and are not investment advice."
    )

st.caption(
    "KPI values are recalculated from the selected category rows. Ratios with a zero or missing denominator are shown as N/A. "
    "No performance trend, forecast, or investment return is inferred from this single-period snapshot."
)

# --------------------------- CHARTS & TABLES ------------------------

st.markdown(
    f"""<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;padding:11px 15px;margin:6px 0 17px;border:1px solid rgba(103,245,197,.2);border-radius:12px;background:rgba(13,29,47,.55);">
    <span style="font-family:'DM Mono',monospace;color:#67f5c5;font-size:.75rem;letter-spacing:.08em;">● ANALYTICS ENGINE READY</span>
    <span style="color:#a8bbd8;font-size:.8rem;">{len(selected_categories)} categories selected · {len(filtered):,} category records in view · Values in ₹ crore unless noted</span>
    </div>""",
    unsafe_allow_html=True,
)

st.markdown('<p class="section-eyebrow">03 / explore the data universe</p>', unsafe_allow_html=True)
tab_overview, tab_category, tab_scheme, tab_cagr, tab_sector, tab_statistics, tab_actions, tab_references = st.tabs([
    "Overview",
    "Category Analysis",
    "Scheme Analysis",
    "CAGR Intelligence",
    "Sector Summary",
    "Statistical Analysis",
    "Findings & Actions",
    "References",
])

with tab_overview:
    left, right = st.columns(2)
    with left:
        aum_plot = filtered.sort_values("Net AUM (₹ cr)", ascending=True)
        fig = px.bar(
            aum_plot,
            x="Net AUM (₹ cr)",
            y="Scheme Category",
            orientation="h",
            title="Net AUM by category",
            text="Net AUM (₹ cr)",
            color="Net AUM (₹ cr)",
            color_continuous_scale="Blues",
            hover_data=["No. of Schemes", "Folio Count"],
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
        fig.update_layout(coloraxis_showscale=False, height=500, margin=dict(l=10, r=45, t=60, b=20))
        st.plotly_chart(fig, width="stretch")

    with right:
        flow_plot = filtered.sort_values("Net Flows (₹ cr)", ascending=True)
        fig = px.bar(
            flow_plot,
            x="Net Flows (₹ cr)",
            y="Scheme Category",
            orientation="h",
            title="Net flows by category (negative values indicate outflows)",
            text="Net Flows (₹ cr)",
            color="Net Flows (₹ cr)",
            color_continuous_scale="RdYlGn",
            color_continuous_midpoint=0,
            hover_data=["Funds Mobilised (₹ cr)", "Redemptions (₹ cr)"],
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
        fig.update_layout(height=500, margin=dict(l=10, r=45, t=60, b=20), coloraxis_showscale=False)
        st.plotly_chart(fig, width="stretch")

    left, right = st.columns(2)
    with left:
        fig = px.bar(
            filtered.sort_values("Folio Count", ascending=False),
            x="Scheme Category", y="Folio Count",
            title="Investor folios by category",
            text="Folio Count",
            hover_data=["Net AUM (₹ cr)"],
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
        fig.update_layout(height=430, xaxis_tickangle=-35, margin=dict(l=10, r=10, t=60, b=100))
        st.plotly_chart(fig, width="stretch")

    with right:
        fig = px.bar(
            filtered.sort_values("SIP Inflows (₹ cr)", ascending=False),
            x="Scheme Category", y="SIP Inflows (₹ cr)",
            title="SIP inflows by category",
            text="SIP Inflows (₹ cr)",
            hover_data=["Folio Count", "Net Flows (₹ cr)"],
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
        fig.update_layout(height=430, xaxis_tickangle=-35, margin=dict(l=10, r=10, t=60, b=100))
        st.plotly_chart(fig, width="stretch")

    st.markdown("#### Category snapshot")
    st.dataframe(
        filtered.sort_values("Net AUM (₹ cr)", ascending=False),
        width="stretch",
        hide_index=True,
    )

with tab_category:
    st.subheader("Category-level comparison")
    show_cols = [
        "Scheme Category", "No. of Schemes", "Folio Count",
        "Funds Mobilised (₹ cr)", "Redemptions (₹ cr)",
        "Net Flows (₹ cr)", "Net AUM (₹ cr)", "Avg AUM (₹ cr)",
        "SIP Inflows (₹ cr)", "Redemption Ratio (%)",
        "Net Flow / AUM (%)", "Folio Share (%)",
    ]
    st.dataframe(
        filtered[[c for c in show_cols if c in filtered.columns]].sort_values(
            "Net Flows (₹ cr)", ascending=False
        ),
        width="stretch",
        hide_index=True,
    )

    st.markdown("#### Mobilisation versus redemptions")
    flow_long = filtered.melt(
        id_vars=["Scheme Category"],
        value_vars=["Funds Mobilised (₹ cr)", "Redemptions (₹ cr)"],
        var_name="Flow type",
        value_name="Amount (₹ cr)",
    )
    fig = px.bar(
        flow_long, x="Scheme Category", y="Amount (₹ cr)",
        color="Flow type", barmode="group",
        title="Funds mobilised versus redemptions",
        hover_data=["Amount (₹ cr)"],
    )
    fig.update_layout(height=500, xaxis_tickangle=-35)
    st.plotly_chart(fig, width="stretch")

    st.markdown("#### Folio share")
    folio_share = filtered[["Scheme Category", "Folio Count"]].copy()
    folio_share = folio_share[folio_share["Folio Count"].fillna(0) > 0]
    if not folio_share.empty:
        fig = px.pie(
            folio_share, names="Scheme Category", values="Folio Count",
            hole=0.45, title="Share of selected category folios",
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, width="stretch")

with tab_scheme:
    st.subheader("Selected scheme-level examples")
    scheme_view = scheme_df.copy()
    scheme_categories = sorted(scheme_view["Scheme Category"].dropna().astype(str).unique())
    selected_scheme_categories = st.multiselect(
        "Filter scheme examples",
        options=scheme_categories,
        default=scheme_categories,
        key="scheme_filter",
    )
    scheme_view = scheme_view[
        scheme_view["Scheme Category"].astype(str).isin(selected_scheme_categories)
    ]

    scheme_metric = st.selectbox(
        "Rank selected schemes by",
        options=[
            "Net Flows (₹ cr)", "Net AUM (₹ cr)",
            "Folio Count", "SIP Inflows (₹ cr)",
            "Redemption Ratio (%)",
        ],
    )
    scheme_view = scheme_view.sort_values(scheme_metric, ascending=False, na_position="last")
    st.dataframe(scheme_view, width="stretch", hide_index=True)

    fig = px.bar(
        scheme_view.sort_values(scheme_metric, ascending=True),
        x=scheme_metric, y="Scheme Category", orientation="h",
        title=f"Selected scheme examples ranked by {scheme_metric}",
        color=scheme_metric, color_continuous_scale="Teal",
        hover_data=[
            c for c in [
                "Net Flows (₹ cr)", "Net AUM (₹ cr)",
                "Folio Count", "SIP Inflows (₹ cr)"
            ] if c in scheme_view.columns
        ],
    )
    fig.update_layout(height=max(450, 35 * len(scheme_view)), coloraxis_showscale=False)
    st.plotly_chart(fig, width="stretch")

    if not scheme_view.empty:
        negative = scheme_view[scheme_view["Net Flows (₹ cr)"] < 0]
        positive = scheme_view[scheme_view["Net Flows (₹ cr)"] > 0]
        a, b = st.columns(2)
        a.metric("Selected examples with positive net flows", f"{len(positive):,}")
        b.metric("Selected examples with negative net flows", f"{len(negative):,}")
        if not negative.empty:
            st.warning(
                "Outflow examples in the selected scheme table: "
                + ", ".join(negative["Scheme Category"].astype(str).tolist())
            )

with tab_cagr:
    st.markdown('<p class="section-eyebrow">04 / long-horizon growth analytics</p>', unsafe_allow_html=True)
    st.subheader("CAGR intelligence module")
    st.write(
        "Calculate annualised historical NAV growth for mutual fund schemes using a dated NAV history file. "
        "The current workbook contains category/scheme snapshots, not historical NAV series, so CAGR cannot be validly calculated from the workbook alone."
    )
    st.latex(r"\text{CAGR}=\left(\frac{\text{Ending NAV}}{\text{Beginning NAV}}\right)^{1/n}-1")
    st.caption("Required CSV columns: Scheme, Date, NAV. One row per scheme per valuation date. NAV must be positive; use actual historical NAV observations.")

    template = pd.DataFrame({
        "Scheme": ["Example scheme — replace with real data", "Example scheme — replace with real data"],
        "Date": ["2023-10-22", "2026-10-22"],
        "NAV": [100.0, 125.0],
    })
    st.download_button(
        "Download CSV format template",
        data=template.to_csv(index=False).encode("utf-8"),
        file_name="mutual_fund_nav_history_template.csv",
        mime="text/csv",
        help="Illustrative rows only. Replace them with verified historical NAV data before using results.",
    )
    nav_file = st.file_uploader("Upload historical NAV data (CSV)", type=["csv"], key="cagr_nav_upload")
    if nav_file is None:
        st.info("Upload a CSV containing real historical NAV values to activate the 1-year, 3-year and 5-year CAGR calculations. The template is illustrative and must not be used as real fund data.")
    else:
        try:
            nav_df = pd.read_csv(nav_file)
            nav_df.columns = [str(c).strip() for c in nav_df.columns]
            lower_to_original = {c.lower(): c for c in nav_df.columns}
            required_aliases = {"scheme": ["scheme", "scheme name", "fund", "fund name"],
                                "date": ["date", "nav date", "valuation date"],
                                "nav": ["nav", "net asset value"]}
            resolved = {}
            for target, aliases in required_aliases.items():
                match = next((lower_to_original[a] for a in aliases if a in lower_to_original), None)
                if match is None:
                    raise ValueError("Required columns not found. Please provide Scheme, Date and NAV columns.")
                resolved[target] = match
            nav_df = nav_df.rename(columns={resolved["scheme"]: "Scheme", resolved["date"]: "Date", resolved["nav"]: "NAV"})
            nav_df["Scheme"] = nav_df["Scheme"].astype("string").str.strip()
            nav_df["Date"] = pd.to_datetime(nav_df["Date"], errors="coerce")
            nav_df["NAV"] = pd.to_numeric(nav_df["NAV"].astype(str).str.replace(",", "", regex=False), errors="coerce")
            nav_df = nav_df.dropna(subset=["Scheme", "Date", "NAV"])
            nav_df = nav_df[(nav_df["Scheme"] != "") & (nav_df["NAV"] > 0)]
            nav_df = nav_df.sort_values(["Scheme", "Date"]).drop_duplicates(["Scheme", "Date"], keep="last")
            if nav_df.empty:
                raise ValueError("No valid rows remain. Check that dates parse correctly and NAV values are positive numbers.")

            latest_date = nav_df["Date"].max()
            st.caption(f"Data coverage: {nav_df['Scheme'].nunique():,} schemes · {len(nav_df):,} valid observations · latest date: {latest_date:%d %b %Y}.")
            periods = st.multiselect("CAGR horizons", [1, 3, 5], default=[1, 3, 5], format_func=lambda n: f"{n}-year CAGR")
            cagr_rows = []
            for scheme_name, group in nav_df.groupby("Scheme", sort=True):
                group = group.sort_values("Date")
                end_row = group.iloc[-1]
                for years in periods:
                    target_date = end_row["Date"] - pd.DateOffset(years=years)
                    candidates = group[group["Date"] <= target_date]
                    if candidates.empty:
                        continue
                    start_row = candidates.iloc[-1]
                    elapsed_years = (end_row["Date"] - start_row["Date"]).days / 365.2425
                    if elapsed_years <= 0 or start_row["NAV"] <= 0:
                        continue
                    cagr = ((end_row["NAV"] / start_row["NAV"]) ** (1 / elapsed_years) - 1) * 100
                    cagr_rows.append({
                        "Scheme": scheme_name,
                        "Horizon": f"{years}-year",
                        "Start date": start_row["Date"].date(),
                        "Start NAV": start_row["NAV"],
                        "End date": end_row["Date"].date(),
                        "End NAV": end_row["NAV"],
                        "Elapsed years": elapsed_years,
                        "CAGR (%)": cagr,
                    })
            cagr_result = pd.DataFrame(cagr_rows)
            if cagr_result.empty:
                st.warning("No scheme has sufficient historical coverage for the selected horizons. Add older NAV observations or choose a shorter horizon.")
            else:
                available_horizons = sorted(cagr_result["Horizon"].unique())
                c1, c2, c3 = st.columns(3)
                c1.metric("Schemes analysed", f"{cagr_result['Scheme'].nunique():,}")
                c2.metric("CAGR results", f"{len(cagr_result):,}")
                c3.metric("Latest NAV date", latest_date.strftime("%d %b %Y"))
                selected_horizon = st.selectbox("Compare schemes by horizon", available_horizons)
                horizon_df = cagr_result[cagr_result["Horizon"] == selected_horizon].sort_values("CAGR (%)", ascending=False)
                st.dataframe(horizon_df, width="stretch", hide_index=True, column_config={
                    "Start NAV": st.column_config.NumberColumn(format="%.4f"),
                    "End NAV": st.column_config.NumberColumn(format="%.4f"),
                    "Elapsed years": st.column_config.NumberColumn(format="%.2f"),
                    "CAGR (%)": st.column_config.NumberColumn(format="%.2f%%"),
                })
                fig_cagr = px.bar(horizon_df, x="CAGR (%)", y="Scheme", orientation="h", color="CAGR (%)",
                                  color_continuous_scale="Tealgrn", title=f"Historical {selected_horizon} CAGR by scheme")
                fig_cagr.update_layout(height=max(400, 32 * len(horizon_df)), coloraxis_showscale=False)
                st.plotly_chart(fig_cagr, width="stretch")
                st.download_button("Download calculated CAGR results", data=cagr_result.to_csv(index=False).encode("utf-8"),
                                   file_name="mutual_fund_cagr_results.csv", mime="text/csv")
            st.warning("CAGR is based on NAV-only growth and does not account for investor cash-flow timing. For dividend/IDCW plans, use an appropriate total-return series or adjusted NAV. Past performance does not guarantee future results.")
        except Exception as exc:
            st.error(f"Could not process the NAV file: {exc}")

with tab_sector:
    st.subheader("Sector summary — separate reporting period")
    st.caption(
        "This table covers 1 April–30 September 2026; net assets are as of "
        "30 September 2026. Do not compare its values directly with category "
        "data ending 31 August 2026."
    )
    st.dataframe(sector_df, width="stretch", hide_index=True)

    if not sector_df.empty and "Metric" in sector_df.columns:
        numeric_sector_cols = [
            c for c in sector_df.columns
            if c != "Metric" and pd.api.types.is_numeric_dtype(sector_df[c])
        ]
        if numeric_sector_cols:
            metric_options = sector_df["Metric"].dropna().astype(str).tolist()
            selected_metric = st.selectbox(
                "Select sector metric",
                options=metric_options,
            )
            row = sector_df[sector_df["Metric"].astype(str) == selected_metric]
            if not row.empty:
                values = row.iloc[0]
                plot_data = pd.DataFrame({
                    "Sector": ["Private Sector", "Public Sector"],
                    "Amount (₹ cr)": [
                        values.get("Private Sector (₹ cr)", np.nan),
                        values.get("Public Sector (₹ cr)", np.nan),
                    ],
                }).dropna()
                if not plot_data.empty:
                    fig = px.bar(
                        plot_data, x="Sector", y="Amount (₹ cr)",
                        title=f"{selected_metric}: Private vs Public sector",
                        text="Amount (₹ cr)",
                    )
                    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
                    fig.update_layout(height=420)
                    st.plotly_chart(fig, width="stretch")

with tab_statistics:
    st.subheader("Statistical analysis")
    numeric = filtered.select_dtypes(include="number")
    if not numeric.empty:
        stats = numeric.describe().T.reset_index().rename(columns={"index": "Metric"})
        stats = stats.rename(columns={
            "count": "Count", "mean": "Mean", "std": "Std. Deviation",
            "min": "Minimum", "25%": "25th Percentile",
            "50%": "Median", "75%": "75th Percentile", "max": "Maximum",
        })
        st.markdown("#### Descriptive statistics")
        st.dataframe(stats, width="stretch", hide_index=True)

        st.markdown("#### Correlation matrix")
        corr_cols = [
            c for c in [
                "Funds Mobilised (₹ cr)", "Redemptions (₹ cr)",
                "Net Flows (₹ cr)", "Net AUM (₹ cr)",
                "Folio Count", "SIP Inflows (₹ cr)",
            ] if c in filtered.columns
        ]
        corr = filtered[corr_cols].corr(numeric_only=True)
        fig = px.imshow(
            corr, text_auto=".2f", aspect="auto",
            color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
            title="Correlation between category-level measures",
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, width="stretch")
        st.caption(
            "There are only eight category observations. Correlations are "
            "descriptive, sensitive to category size, and do not imply causation."
        )

        st.markdown("#### Net-flow and AUM rankings")
        rank_df = filtered[
            ["Scheme Category", "Net Flows (₹ cr)", "Net AUM (₹ cr)", "Folio Count"]
        ].copy()
        rank_df["Net-flow rank"] = rank_df["Net Flows (₹ cr)"].rank(
            ascending=False, method="min"
        ).astype("Int64")
        rank_df["AUM rank"] = rank_df["Net AUM (₹ cr)"].rank(
            ascending=False, method="min"
        ).astype("Int64")
        st.dataframe(
            rank_df.sort_values("Net-flow rank"),
            width="stretch", hide_index=True
        )
    else:
        st.warning("No numeric columns are available for statistical analysis.")

with tab_actions:
    st.subheader("Interpretation of findings")
    if not filtered.empty:
        top_aum = filtered.loc[filtered["Net AUM (₹ cr)"].idxmax()]
        top_flow = filtered.loc[filtered["Net Flows (₹ cr)"].idxmax()]
        top_folios = filtered.loc[filtered["Folio Count"].idxmax()]
        top_sip = filtered.loc[filtered["SIP Inflows (₹ cr)"].idxmax()]
        negative_categories = filtered[filtered["Net Flows (₹ cr)"] < 0]

        findings = [
            (
                "Largest AUM category",
                f"{top_aum['Scheme Category']} has the largest net AUM "
                f"among the selected categories ({fmt_money(top_aum['Net AUM (₹ cr)'])})."
            ),
            (
                "Highest net-flow category",
                f"{top_flow['Scheme Category']} has the highest reported net flows "
                f"({fmt_money(top_flow['Net Flows (₹ cr)'])})."
            ),
            (
                "Largest folio base",
                f"{top_folios['Scheme Category']} has the most folios "
                f"({fmt_number(top_folios['Folio Count'])}). Folios represent "
                "accounts, not necessarily unique investors."
            ),
            (
                "Highest SIP inflows",
                f"{top_sip['Scheme Category']} has the highest SIP inflows "
                f"({fmt_money(top_sip['SIP Inflows (₹ cr)'])}) in this dataset."
            ),
            (
                "Negative net flows",
                (
                    "Categories with negative reported net flows: "
                    + ", ".join(negative_categories["Scheme Category"].astype(str))
                    if not negative_categories.empty
                    else "No selected categories have negative reported net flows."
                )
            ),
        ]
        for title, detail in findings:
            st.markdown(f"**{title}:** {detail}")

    st.markdown("#### Actionable recommendations")
    recs = pd.DataFrame([
        {
            "Recommendation": "1. Investigate persistent outflows",
            "Action": (
                "Review monthly flows, performance relative to the relevant benchmark, "
                "fees, liquidity and investor segments for categories or schemes with "
                "repeated outflows. Do not react to one snapshot alone."
            ),
            "Monitoring KPI": (
                "Monthly net flows; redemption ratio; number of consecutive "
                "periods with negative flows."
            ),
        },
        {
            "Recommendation": "2. Improve investor education",
            "Action": (
                "Explain the differences between equity, debt, hybrid, ETF and "
                "tax-saving products using goal, risk, time horizon, costs and "
                "liquidity. Keep communication factual and suitability-led."
            ),
            "Monitoring KPI": (
                "Folio additions, investor education participation, investor "
                "queries and complaint themes."
            ),
        },
        {
            "Recommendation": "3. Evaluate ETF education and access",
            "Action": (
                "Study ETF demand, liquidity, tracking difference and expense ratios. "
                "Expand education only where the product fits the investor's needs "
                "and risk tolerance."
            ),
            "Monitoring KPI": (
                "ETF net flows, folio additions, trading liquidity and tracking difference."
            ),
        },
        {
            "Recommendation": "4. Standardise monthly reporting",
            "Action": (
                "Refresh the dashboard on a consistent schedule, record each data "
                "cut-off date and compare like-for-like periods. Separate market "
                "valuation effects from investor flows where time-series data exist."
            ),
            "Monitoring KPI": (
                "On-time refresh, validation errors, monthly AUM and net-flow changes."
            ),
        },
        {
            "Recommendation": "5. Validate SIP fields",
            "Action": (
                "Confirm whether zero SIP values mean genuinely zero contributions "
                "or not reported before drawing conclusions."
            ),
            "Monitoring KPI": (
                "SIP inflows by category and period; missing-versus-zero audit."
            ),
        },
    ])
    st.dataframe(recs, width="stretch", hide_index=True)

    st.markdown("#### Limitations")
    st.markdown(
        """
        - This is a snapshot, not a time series; it cannot establish trends or forecast returns.
        - AUM can change because of market valuation as well as investor flows.
        - Category and sector figures use different reporting cut-off dates.
        - Correlations from a small number of categories are descriptive, not causal.
        - Folio counts are accounts and should not be interpreted as unique individuals.
        - This dashboard is for educational analysis and is not investment advice.
        """
    )

    # The table is also included in the downloadable workbook.
    st.session_state["recommendations_df"] = recs

with tab_references:
    st.subheader("References")
    references = pd.DataFrame([
        {
            "Source": "SEBI — Status of Mutual Fund Industry, Apr–Sep 2026",
            "URL": CATEGORY_SOURCE,
            "Use in this project": (
                "Detailed scheme-category figures; the supplied workbook says "
                "category data are as of 31 August 2026."
            ),
        },
        {
            "Source": "SEBI — Status of Mutual Funds, Apr–Sep 2026",
            "URL": SECTOR_SOURCE,
            "Use in this project": (
                "Sector-level cumulative figures through 30 September 2026."
            ),
        },
        {
            "Source": "SEBI — Mutual Fund Statistics",
            "URL": SEBI_LANDING,
            "Use in this project": "Official mutual fund statistics landing page.",
        },
        {
            "Source": "pandas documentation",
            "URL": "https://pandas.pydata.org/docs/",
            "Use in this project": "Excel data loading, cleaning and statistics.",
        },
        {
            "Source": "Plotly Python documentation",
            "URL": "https://plotly.com/python/",
            "Use in this project": "Interactive charts and visualisations.",
        },
        {
            "Source": "Streamlit documentation",
            "URL": "https://docs.streamlit.io/",
            "Use in this project": "Dashboard interface and filters.",
        },
    ])
    st.dataframe(references, width="stretch", hide_index=True)
    for _, row in references.iterrows():
        st.markdown(f"- [{row['Source']}]({row['URL']}) — {row['Use in this project']}")

# -------------------------- DOWNLOADS ------------------------------

st.divider()
st.subheader("Export cleaned data and analysis")

# Make downloadable summary tables from the full cleaned data.
full_stats = category_df.select_dtypes(include="number").describe().T.reset_index()
full_stats = full_stats.rename(columns={"index": "Metric"})
full_findings = pd.DataFrame([
    ["Reporting period", "Category data through 31 Aug 2026; sector summary through 30 Sep 2026."],
    ["Interpretation", "Descriptive snapshot only; no return series or causal analysis."],
    ["Data caution", "Negative net flows are retained; missing values are not replaced with zero."],
], columns=["Topic", "Details"])

full_recommendations = pd.DataFrame([
    ["Investigate persistent outflows", "Review repeated negative flows with performance, fees, liquidity and investor-segment data.", "Monthly net flows and redemption ratio"],
    ["Improve investor education", "Explain product types, costs, liquidity, risk and investment horizon.", "Folio additions and education engagement"],
    ["Evaluate ETF education/access", "Assess suitability, liquidity, tracking difference and expense ratios.", "ETF flows, folios and tracking difference"],
    ["Standardise monthly reporting", "Use consistent reporting cut-offs and separate valuation changes from investor flows.", "Refresh timeliness and validation checks"],
    ["Validate SIP values", "Confirm whether zero SIP values mean no contributions or unavailable reporting.", "SIP inflows and missing-versus-zero audit"],
], columns=["Recommendation", "Action", "Monitoring KPI"])

excel_bytes = make_excel_download(
    category_df, scheme_df, sector_df, quality_df,
    full_stats, full_findings, full_recommendations
)
st.download_button(
    label="⬇️ Download cleaned data and analysis (Excel)",
    data=excel_bytes,
    file_name="Mutual_Fund_Dashboard_Analysis.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

st.caption(
    "NEXUS 2050 interface concept. Source workbook is read-only in this app. Export creates a separate "
    "analysis workbook; it does not overwrite the original file."
)
