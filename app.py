import streamlit as st

TOTAL = 108
PER_ROW = 12

st.set_page_config(page_title="108 Rounds Counter", page_icon="🙏", layout="centered")


def read_saved_count() -> int:
    # The count lives in the URL (?rounds=N) so a refresh or reconnect keeps it.
    # Session state alone would reset, and a server-side file would be shared by every visitor.
    try:
        return min(max(int(st.query_params.get("rounds", 0)), 0), TOTAL)
    except ValueError:
        return 0


def set_count(n: int) -> None:
    st.session_state.count = n
    st.session_state.confirm_reset = False
    st.query_params["rounds"] = str(n)


if "count" not in st.session_state:
    st.session_state.count = read_saved_count()
    st.session_state.confirm_reset = False

count = st.session_state.count
finished = count >= TOTAL

st.title("Rounds walked")
st.metric("Completed", f"{count} / {TOTAL}")
st.progress(count / TOTAL)

if finished:
    st.success("108 rounds complete 🙏")

st.button(
    "All 108 done" if finished else "Round completed",
    type="primary",
    use_container_width=True,
    disabled=finished,
    on_click=set_count,
    args=(count + 1,),
)

undo_col, reset_col = st.columns(2)
undo_col.button(
    "Undo",
    use_container_width=True,
    disabled=count == 0,
    on_click=set_count,
    args=(count - 1,),
)

if st.session_state.confirm_reset:
    reset_col.button("Yes, reset to 0", use_container_width=True, on_click=set_count, args=(0,))
    reset_col.button(
        "Cancel",
        use_container_width=True,
        on_click=lambda: st.session_state.update(confirm_reset=False),
    )
else:
    reset_col.button(
        "Reset",
        use_container_width=True,
        disabled=count == 0,
        on_click=lambda: st.session_state.update(confirm_reset=True),
    )

beads = ["🟠"] * count + ["⚪"] * (TOTAL - count)
rows = ["".join(beads[i : i + PER_ROW]) for i in range(0, TOTAL, PER_ROW)]
st.markdown("  \n".join(rows))

st.caption("Progress is saved in this page's URL. Bookmark or reopen the same link to keep your count.")
