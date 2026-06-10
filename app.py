import streamlit as st
import uuid
import sys
import os
from langgraph.types import Command
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from workflow import graph


st.set_page_config(page_title="News Magazine",layout="wide")
st.title("Multi-Agent News Magazine")



if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "review_mode" not in st.session_state:
    st.session_state.review_mode = False

if "generated" not in st.session_state:
    st.session_state.generated = False



config = {"configurable": {"thread_id": st.session_state.thread_id}}
query = st.text_area("What news do you want?",placeholder="Latest AI, Business and Sports news",key="query_input")
if st.button("Generate Magazine"):
    if not query.strip():
        st.warning("Please enter a query.")
        st.stop()
    initial_state = {
        "query": query,
        "target_email": "",
        "is_exam_prep": False,
        "categories_required": [],
        "sports_news": [],
        "business_news": [],
        "national_news": [],
        "international_news": [],
        "logs": []
    }
    log_placeholder = st.empty()
    try:
        with st.spinner("Generating magazine..."):
            for event in graph.stream(initial_state,config=config,stream_mode="values"):
                logs = event.get("logs", [])
                log_placeholder.code("\n".join(logs),language="text")

        st.session_state.generated = True
        state = graph.get_state(config)
        if state.next and "human_review" in state.next:
            st.session_state.review_mode = True
        st.rerun()
    except Exception as e:
        st.error(f"Error: {str(e)}")


if st.session_state.review_mode:
    st.divider()
    st.subheader("Human Review")
    state = graph.get_state(config)
    values = state.values
    report = values.get("magazine_report","No report generated.")
    critique = values.get("critique","")
    st.markdown("### Generated Magazine")
    st.markdown(report)
    if critique:
        st.markdown("### Critique")
        st.info(critique)


    col1, col2 = st.columns(2)

    with col1:
        if st.button("Approve",key="approve_btn"):
            try:
                graph.invoke(Command(resume={"status": "approve",}),config=config)
                st.success("Magazine Approved")
                st.session_state.review_mode = False
                st.rerun()
            except Exception as e:
                st.error(str(e))

    with col2:
        if st.button("Reject",key="reject_btn"):
            try:
                graph.invoke(Command(resume={"status": "reject",}),config=config)
                st.error("Magazine Rejected")
                st.session_state.review_mode = False
                st.rerun()
            except Exception as e:
                st.error(str(e))



try:
    state = graph.get_state(config)
    values = state.values
    report = values.get("magazine_report")
    if report:
        st.divider()
        st.subheader("Final Magazine")
        st.markdown(report)
        email_status = values.get("email_status","Not Sent")
        human_approved = values.get("human_approved",None)
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Email Status",str(email_status))
        with col2:
            st.metric("Approved",str(human_approved))

except Exception:
    pass


