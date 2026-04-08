import json
import os

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from axes import ALL_SECTIONS, HOW_JOURNEY_AXES, HOW_MECHANISM_AXES
from prompt import build_system_prompt
from schema import AxisMapping, CrossMapping, Confidence, MessageRequest, MessageResponse
from session import create_session, get_session, Session

load_dotenv()

app = FastAPI(title="stratmap AI Interview")

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-20250514"


def call_claude(session: Session, user_message: str) -> dict:
    system_prompt = build_system_prompt(session.get_state_summary())

    messages = []
    for msg in session.conversation:
        messages.append(msg)
    messages.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=system_prompt,
        messages=messages,
    )

    raw = response.content[0].text.strip()

    # Parse JSON from response (handle markdown code blocks)
    if raw.startswith("```"):
        lines = raw.split("\n")
        json_lines = []
        in_block = False
        for line in lines:
            if line.startswith("```") and not in_block:
                in_block = True
                continue
            elif line.startswith("```") and in_block:
                break
            elif in_block:
                json_lines.append(line)
        raw = "\n".join(json_lines)

    return json.loads(raw)


@app.post("/session")
async def new_session():
    session = create_session()

    # Generate initial greeting
    initial_message = "こんにちは。ビジネス戦略の仮説を一緒に整理しましょう。\n\nどんな事業やサービスについて考えていますか？自由にお話しください。"

    session.conversation.append({
        "role": "assistant",
        "content": json.dumps({
            "response": initial_message,
            "mappings": [],
            "cross_mappings": [],
            "is_complete": False,
        }, ensure_ascii=False),
    })

    return {
        "session_id": session.id,
        "response": initial_message,
        "mappings_updated": [],
        "cross_updated": [],
        "completion": session.get_completion(),
        "is_complete": False,
    }


@app.post("/session/{session_id}/message")
async def send_message(session_id: str, req: MessageRequest):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Add user message to conversation
    session.conversation.append({"role": "user", "content": req.message})

    try:
        result = call_claude(session, req.message)
    except (json.JSONDecodeError, Exception) as e:
        # On parse failure, return error but keep conversation intact
        session.conversation.pop()  # Remove the user message
        raise HTTPException(status_code=502, detail=f"AI response parse error: {str(e)}")

    # Store raw AI response in conversation
    session.conversation.append({"role": "assistant", "content": json.dumps(result, ensure_ascii=False)})

    # Parse and apply mappings
    mappings_updated = []
    for m in result.get("mappings", []):
        try:
            mapping = AxisMapping(
                section=m["section"],
                axis=m["axis"],
                value=max(1, min(10, int(m["value"]))),
                confidence=Confidence(m["confidence"]),
                reason=m.get("reason", ""),
            )
            mappings_updated.append(mapping)
        except (KeyError, ValueError):
            continue

    cross_updated = []
    for c in result.get("cross_mappings", []):
        try:
            cross = CrossMapping(
                journey_axis=c["journey_axis"],
                mechanism_axis=c["mechanism_axis"],
                level=max(0, min(3, int(c["level"]))),
                confidence=Confidence(c["confidence"]),
                reason=c.get("reason", ""),
            )
            cross_updated.append(cross)
        except (KeyError, ValueError):
            continue

    session.update_mappings(mappings_updated)
    session.update_cross(cross_updated)

    return MessageResponse(
        response=result.get("response", ""),
        mappings_updated=mappings_updated,
        cross_updated=cross_updated,
        completion=session.get_completion(),
        is_complete=result.get("is_complete", False) or session.is_complete(),
    )


@app.get("/session/{session_id}")
async def get_session_state(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    all_mappings = []
    for section_key, section in ALL_SECTIONS.items():
        for ax in section["axes"]:
            key = f"{section_key}.{ax['id']}"
            if key in session.mappings:
                all_mappings.append(session.mappings[key].model_dump())
            else:
                all_mappings.append({
                    "section": section_key,
                    "axis": ax["id"],
                    "value": 5,
                    "confidence": "unknown",
                    "reason": "",
                })

    return {
        "session_id": session.id,
        "mappings": all_mappings,
        "cross_mappings": [c.model_dump() for c in session.cross_mappings.values()],
        "completion": session.get_completion(),
        "is_complete": session.is_complete(),
        "message_count": len([m for m in session.conversation if m["role"] == "user"]),
    }


@app.get("/session/{session_id}/export")
async def export_session(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return JSONResponse(content=session.to_stratmap_json())


@app.get("/session/{session_id}/report")
async def get_report(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Build conversation log
    conv_html = ""
    for msg in session.conversation:
        role = msg["role"]
        content = msg["content"]
        if role == "assistant":
            try:
                parsed = json.loads(content)
                content = parsed.get("response", content)
            except (json.JSONDecodeError, TypeError):
                pass
        cls = "ai" if role == "assistant" else "user"
        label = "AI" if role == "assistant" else "あなた"
        conv_html += f'<div class="msg {cls}"><span class="msg-role">{label}</span><p>{content}</p></div>\n'

    # Build mappings table
    mappings_html = ""
    for section_key, section in ALL_SECTIONS.items():
        mappings_html += f'<h3>{section["label"]}</h3><table><tr><th>軸</th><th>値</th><th>確信度</th><th>根拠</th></tr>'
        for ax in section["axes"]:
            key = f"{section_key}.{ax['id']}"
            if key in session.mappings:
                m = session.mappings[key]
                conf_cls = m.confidence.value
                mappings_html += f'<tr class="{conf_cls}"><td>{ax["label"]}</td><td>{m.value}</td><td>{m.confidence.value}</td><td>{m.reason}</td></tr>'
            else:
                mappings_html += f'<tr class="unknown"><td>{ax["label"]}</td><td>—</td><td>unknown</td><td></td></tr>'
        mappings_html += '</table>'

    completion = session.get_completion()
    comp_html = ""
    labels = {"who": "Who", "what": "What", "howJourney": "How(ジャーニー)", "howMechanism": "How(メカニズム)", "howCross": "How(クロス)"}
    for k, v in completion.items():
        pct = int(v * 100)
        comp_html += f'<div class="comp-row"><span>{labels.get(k, k)}</span><div class="comp-bar"><div class="comp-fill" style="width:{pct}%"></div></div><span>{pct}%</span></div>'

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>stratmap レポート</title>
<style>
:root {{ --bg:#fff; --bg2:#f5f5f3; --text:#1a1a18; --text2:#6b6b66; --text3:#9e9d98; --border:rgba(0,0,0,0.1); --good:#1D9E75; --mid:#C4873B; --warn:#D85A30; --font:'Noto Sans JP','Hiragino Sans',system-ui,sans-serif; }}
@media(prefers-color-scheme:dark){{ :root {{ --bg:#1c1c1a; --bg2:#252522; --text:#e8e7e1; --text2:#9e9d98; --text3:#5f5e5a; --border:rgba(255,255,255,0.1); }} }}
*{{ box-sizing:border-box; margin:0; padding:0; }}
body {{ font-family:var(--font); background:var(--bg); color:var(--text); max-width:800px; margin:0 auto; padding:2rem 1.5rem; }}
h1 {{ font-size:18px; font-weight:500; margin-bottom:4px; }}
.sub {{ font-size:13px; color:var(--text2); margin-bottom:2rem; }}
h2 {{ font-size:14px; font-weight:500; color:var(--text2); margin:2rem 0 1rem; padding-bottom:6px; border-bottom:0.5px solid var(--border); }}
h3 {{ font-size:12px; font-weight:500; color:var(--text2); margin:1rem 0 0.5rem; }}
table {{ width:100%; border-collapse:collapse; font-size:12px; margin-bottom:1rem; }}
th {{ text-align:left; padding:6px 8px; border-bottom:1px solid var(--border); color:var(--text3); font-weight:500; }}
td {{ padding:6px 8px; border-bottom:0.5px solid var(--border); }}
tr.confident td:first-child {{ border-left:3px solid var(--good); }}
tr.inferred td:first-child {{ border-left:3px solid var(--mid); }}
tr.unknown td {{ color:var(--text3); }}
.comp-row {{ display:flex; align-items:center; gap:8px; margin-bottom:6px; font-size:12px; }}
.comp-row span:first-child {{ min-width:120px; color:var(--text2); }}
.comp-bar {{ flex:1; height:8px; background:var(--bg2); border-radius:4px; overflow:hidden; }}
.comp-fill {{ height:100%; background:var(--good); border-radius:4px; }}
.comp-row span:last-child {{ min-width:36px; text-align:right; font-weight:500; }}
.msg {{ padding:10px 14px; margin-bottom:8px; border-radius:8px; }}
.msg.ai {{ background:var(--bg2); }}
.msg.user {{ background:transparent; border:0.5px solid var(--border); }}
.msg-role {{ font-size:10px; font-weight:500; color:var(--text3); display:block; margin-bottom:4px; }}
.msg p {{ font-size:13px; line-height:1.7; white-space:pre-wrap; }}
</style>
</head>
<body>
<h1>戦略仮説レポート</h1>
<p class="sub">生成日時: {session.created_at}</p>

<h2>完了度</h2>
{comp_html}

<h2>マッピング結果</h2>
{mappings_html}

<h2>対話ログ</h2>
{conv_html}
</body></html>"""

    return HTMLResponse(content=html)


# Serve static files (chat UI)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
