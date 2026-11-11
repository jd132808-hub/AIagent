"""Run with: python -m streamlit run app.py."""

import logging
import time
from datetime import datetime
from pathlib import Path

import streamlit as st


st.set_page_config(page_title="智扫通 · 智能客服", page_icon=":material/smart_toy:",
                   layout="centered", initial_sidebar_state="auto")
stylesheet = Path(__file__).with_name("assets") / "app.css"
st.markdown(f"<style>{stylesheet.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

SUGGESTIONS = (
    ("选购建议", "小户型，有宠物，应该怎样选择扫地机器人？", ":material/shopping_bag:"),
    ("故障排查", "扫地机器人找不到充电座，应该如何排查？", ":material/build:"),
    ("日常养护", "滚刷、滤网和拖布应该多久清洁或更换？", ":material/cleaning_services:"),
    ("使用报告", "请帮我生成一份我的扫地机器人使用报告。", ":material/description:"),
)
st.session_state.setdefault("message", [])
st.session_state.setdefault("pending_prompt", None)
st.session_state.setdefault("failed_prompt", None)


def new_conversation():
    st.session_state["message"] = []
    st.session_state["pending_prompt"] = None
    st.session_state["failed_prompt"] = None
    st.session_state.pop("agent", None)


def select_question(question):
    st.session_state["pending_prompt"] = question
    st.session_state["failed_prompt"] = None


def export_conversation():
    lines = ["# 智扫通 · 客服对话", ""]
    for message in st.session_state["message"]:
        role = "我" if message["role"] == "user" else "智扫通"
        lines.extend([f"## {role}", "", message["content"], ""])
    return "\n".join(lines)


def typewriter_stream(chunks):
    """Display incoming answer chunks character by character."""
    for chunk in chunks:
        for character in chunk:
            yield character
            time.sleep(0.01)


with st.sidebar:
    st.markdown('<div class="brand">智扫通<span>SMART CLEAN, SIMPLE LIFE</span></div>', unsafe_allow_html=True)
    st.button("开启新对话", icon=":material/add:", type="primary", use_container_width=True, on_click=new_conversation)
    st.markdown("### 服务指南")
    st.caption("从挑选到养护，陪你解决清洁小事。")
    for title, question, icon in SUGGESTIONS:
        st.button(title, icon=icon, key=f"sidebar_{title}", use_container_width=True,
                  on_click=select_question, args=(question,))
    st.divider()
    st.markdown("### 对话记录")
    count = sum(message["role"] == "user" for message in st.session_state["message"])
    st.caption(f"当前对话 · {count} 次提问")
    st.download_button("导出对话", data=export_conversation(),
                       file_name=f"智扫通对话_{datetime.now():%Y%m%d_%H%M}.md",
                       mime="text/markdown", icon=":material/download:",
                       use_container_width=True, disabled=not st.session_state["message"])
    with st.expander("使用小贴士", icon=":material/help_outline:"):
        st.write("描述设备型号、具体表现和已经尝试的操作，可以让建议更有针对性。")
        st.write("每次提问请补充必要背景；当前客服按单次问题处理。")
        st.caption("使用报告基于演示记录；天气、位置等信息为演示数据。")
    st.caption("智扫通 · 让清洁生活更简单")

st.markdown('<div class="page-label">智扫通 / 智能服务中心</div>', unsafe_allow_html=True)
if not st.session_state["message"]:
    st.markdown('''
    <section class="welcome">
        <div class="welcome-mark" aria-hidden="true">
            <svg width="36" height="36" viewBox="0 0 32 32" fill="none">
                <rect x="5" y="9" width="22" height="17" rx="6" stroke="currentColor" stroke-width="2"/>
                <path d="M16 5v4M3 16v5m26-5v5M12 21h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="16" r="1.5" fill="currentColor"/>
                <circle cx="20" cy="16" r="1.5" fill="currentColor"/>
            </svg>
        </div>
        <p class="eyebrow">你的智能清洁顾问</p>
        <h1>清洁小难题，<br>我们一起解决。</h1>
        <p class="welcome-description">选一台合适的机器人，或让手边这台更好用。<br>关于选购、故障与养护，随时向我提问。</p>
    </section>
    ''', unsafe_allow_html=True)
    st.markdown("### 从一个问题开始")
    for row in (SUGGESTIONS[:2], SUGGESTIONS[2:]):
        for column, (title, question, icon) in zip(st.columns(2), row):
            with column:
                with st.container(border=True):
                    st.markdown(f"**{title}**")
                    st.caption(question)
                    st.button("聊聊这个", icon=icon, key=f"welcome_{title}", use_container_width=True,
                              on_click=select_question, args=(question,))
else:
    st.title("每一个问题，都值得认真解答。")
    st.caption("选购 · 排障 · 养护 · 使用报告")

for message in st.session_state["message"]:
    avatar = ":material/person:" if message["role"] == "user" else ":material/smart_toy:"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

retry = False
if st.session_state["failed_prompt"]:
    st.error("这次回答暂时没有完成。请稍后重试；如果仍未成功，请检查模型服务与网络连接。")
    retry = st.button("重新回答", icon=":material/refresh:")

typed_prompt = st.chat_input("描述你的清洁问题，例如：机器人总是漏扫怎么办？")
prompt = st.session_state.pop("pending_prompt", None) or typed_prompt
if retry:
    prompt = st.session_state["failed_prompt"]

if prompt and prompt.strip():
    prompt = prompt.strip()
    st.session_state["failed_prompt"] = None
    if not retry:
        st.session_state["message"].append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=":material/person:"):
            st.markdown(prompt)
    try:
        with st.chat_message("assistant", avatar=":material/smart_toy:"):
            with st.spinner("正在整理建议，请稍候…"):
                if "agent" not in st.session_state:
                    from agent.react_agent import ReactAgent

                    st.session_state["agent"] = ReactAgent()
                response = st.write_stream(
                    typewriter_stream(st.session_state["agent"].execute_stream(prompt))
                )
                if not isinstance(response, str) or not response.strip():
                    raise ValueError("The agent returned an empty response")
        st.session_state["message"].append({"role": "assistant", "content": response})
    except Exception:
        logging.getLogger(__name__).exception("Customer service response failed")
        st.session_state["failed_prompt"] = prompt
        st.session_state.pop("agent", None)
    st.rerun()

st.caption("回答由 AI 生成，请结合设备说明书核实；涉及拆机或电气故障时，请联系售后。")
