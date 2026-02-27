"""Streamlit web UI for the Garden Store Email Agent."""
from __future__ import annotations

import streamlit as st
from pathlib import Path

from agent.config import settings
from agent.graph import build_graph
from agent.state import EmailState
from agent.utils.file_io import list_txt_files, write_text_file

st.set_page_config(page_title="🌿 Garden Store Email Agent", layout="wide")
st.title("🌿 Garden Store Email Agent")

# ── Sidebar: pick an email ───────────────────────────────────────────────────
st.sidebar.header("📧 Select an Email")
email_files = list_txt_files(settings.emails_folder)

if not email_files:
    st.warning(f"No .txt files found in `{settings.emails_folder}/`. Add some and refresh.")
    st.stop()

file_names = [f.name for f in email_files]
chosen_name = st.sidebar.selectbox("Email file", file_names)
chosen_path = settings.emails_folder / chosen_name

# ── Show raw email ───────────────────────────────────────────────────────────
with open(chosen_path, encoding="utf-8") as fh:
    raw_email = fh.read()

st.subheader("📄 Email Content")
st.text_area("Raw email", value=raw_email, height=200, disabled=True)

# ── Run agent ────────────────────────────────────────────────────────────────
if st.button("▶️  Run Agent"):
    graph = build_graph(interrupt_before_approval=True)
    initial_state = EmailState(file_path=str(chosen_path))

    with st.spinner("Classifying and generating answer…"):
        # Run until the human_approval interrupt (or END for 'other')
        result = graph.invoke(initial_state)

    if result.get("error"):
        st.error(result["error"])
        st.stop()

    st.session_state["result"] = result
    st.session_state["graph"] = graph
    st.session_state["file_path"] = str(chosen_path)
    st.rerun()

# ─�� Human-in-the-loop approval panel ────────────────────────────────────────
if "result" in st.session_state:
    result: dict = st.session_state["result"]
    intent = result.get("intent", "unknown")
    topic = result.get("topic", "")

    col1, col2 = st.columns(2)
    col1.metric("Intent", intent)
    col2.metric("Topic", topic)

    st.subheader("✏️  Draft Answer")
    draft = result.get("draft_answer", "")

    # For 'other' intent the answer is already final — just show it
    if intent == "other":
        st.info("This email was classified as **other**. A holding reply was generated automatically.")
        st.text_area("Final answer (no approval needed)", value=draft, height=200, disabled=True)
        if result.get("output_file_path"):
            st.success(f"✅ Answer saved to `{result['output_file_path']}`")

    else:
        # Plant instructions path — show approval UI
        edited = st.text_area("Edit before approving (optional)", value=draft, height=250)

        col_a, col_r = st.columns(2)
        if col_a.button("✅ Approve & Save"):
            final = edited.strip()
            stem = Path(result["file_path"]).stem
            out_path = settings.answers_folder / f"{stem}_answer.txt"
            write_text_file(out_path, final)
            st.success(f"✅ Answer saved to `{out_path}`")
            del st.session_state["result"]

        if col_r.button("❌ Reject"):
            st.warning("Answer rejected. No file was saved.")
            del st.session_state["result"]