import os
import re
import io
import json
import html
import hashlib
import traceback

import streamlit as st
from google import genai
from google.genai import types
from streamlit_paste_button import paste_image_button

import formats
from formats import FORMATS

st.set_page_config(page_title="Exam Writer", page_icon="✍️", layout="wide")

DEFAULT_MODEL = "gemini-3.5-flash-lite"
DEFAULT_N = 20
ARG_MIN, ARG_MAX = 110, 140
MAX_TOTAL_MB = 19
RED = "#e11d1d"
BLUE = "#1a56db"
AUTO = "AUTO"
NEW = "NEW"

QUESTION_START = re.compile(r"^\s*(should|do|does|is|are|can|will|would|could|has|have|was|were)\b", re.I)
FILL_RE = re.compile(r"\{\{(.+?)\}\}", re.S)
FMT_BLANK_RE = re.compile(r"\{\{(.+?)\}\}|\[([^\[\]\n]+)\]", re.S)
VERIFY_RE = re.compile(r"\{\{(\[VERIFY[^\]]*\])\}\}")
SECTION_RE = re.compile(r"^===\s*(FORMAT|ANSWER|WORD BANK|CHECK|VERIFY)\s*===\s*$", re.M)

# ---------------- PROMPTS ----------------

BASE_RULES = """# BASE RULES (সব format-এ প্রযোজ্য)
১. উত্তর English ও exam-style হবে। ভূমিকা, ব্যাখ্যা বা মন্তব্য লিখবে না।
২. Format-এর skeleton (fixed শব্দ, বাক্যের ক্রম, role) অপরিবর্তিত রাখো। Skeleton সংক্ষিপ্ত করবে না।
৩. Blank শুধু এক শব্দ নয়। প্রতিটি blank-এ ৪–১০ শব্দের পূর্ণ phrase বসাও। Word bank থেকে নিতে পারো, কিন্তু প্রশ্ন ও বাক্যের সাথে মিলিয়ে বদলাও।
৪. বাক্য ছোট রাখবে না: প্রতিটি বাক্য কমপক্ষে {n} শব্দ। প্রয়োজনে skeleton-এর ভেতরে because / which / as a result দিয়ে বিশ্লেষণমূলক clause যোগ করো।
৫. যে অংশ তুমি ভরেছো বা বদলেছো, সেটি {{ }} এর ভেতরে দাও। Skeleton-এর fixed শব্দ {{ }} ছাড়া থাকবে।
৬. অতিরিক্ত নির্দেশনা সবচেয়ে বেশি মানবে। তবু কোনো তথ্য, সংখ্যা, নাম বা উৎস বানাবে না। জানা না থাকলে {{[VERIFY: source + figure]}} বসাও।
৭. Connector ও শব্দের নির্দিষ্ট ক্রম ভাঙবে না।"""

ARG_RULES = """# ARGUMENT RULES
- ঠিক ৬টি বাক্য। মোট শব্দ ১১০–১৪০।
- Connector ক্রম: Although → Firstly, although → However → Secondly, even though → Nevertheless → Therefore, although।
- S1: প্রতিপক্ষের মত স্বীকার + আমার মত।
- S2 ও S4: একটি মূল যুক্তি (Firstly / Secondly) + একটি counter-argument।
- S3 ও S5: counter খণ্ডন; একটি explanation বা example দাও। S5-এ "making ..." ফলাফল।
- S6: judgment; "should ... to ensure ..." কাঠামো।
- Argument-এ Focus-এর Intro, Conclusion বা PEEL ব্যবহার করবে না।"""

FOCUS_RULES = """# FOCUS RULES
- Format-এর প্রতিটি sentence (S1 থেকে শেষ পর্যন্ত) উত্তরে একটি পূর্ণ, দীর্ঘ বাক্য হবে। মোট {count}টি বাক্য।
- Role অনুযায়ী paragraph ভাগ করো। প্রতি paragraph নতুন লাইনে শুরু হবে।
- Intro: Background, Thesis, Outline। Intro-তে quote নয়।
- Body: PEEL (Point, Explain, Example, Link)। Example বাক্যে source নাম ও data থাকবে। Data জানা না থাকলে {{[VERIFY: source + figure]}}।
- Conclusion: format-এর role অনুযায়ী।
- Firstly / Secondly / Lastly ব্যবহার করবে না।
- Graph, chart বা table উল্লেখ করবে না।
- Title লাগলে format-এর TITLE RULE মানো।"""

CT_RULES = """# CRITICAL THOUGHTS RULES
- Format-এর প্রতিটি অংশ (Topic / Reason / Judgment ইত্যাদি) একটি পূর্ণ বাক্য।
- প্রতিটি বাক্য কমপক্ষে {n} শব্দ।
- অনুচ্ছেদের বাইরের তথ্য যোগ করবে না।
- Firstly / Secondly ব্যবহার করবে না।"""

KNOWN_OUTPUT = """# OUTPUT (শুধু এই কাঠামোয়; অন্য কোনো ভূমিকা নয়)
===ANSWER===
<পূর্ণ উত্তর (English)। বদলানো বা ভরা অংশ {{ }} এর ভেতরে।>
===VERIFY===
<বাংলায় bullet দিয়ে: কোন অংশের data যাচাই করতে হবে। না থাকলে "—">"""

NEW_OUTPUT = """# OUTPUT (শুধু এই কাঠামোয়)
===FORMAT===
<নতুন format, blank দিয়ে, একই শৈলীতে>
===ANSWER===
<পূর্ণ উত্তর (English), blank ও বদলানো অংশ {{ }} এর ভেতরে>
===WORD BANK===
<প্রতি blank-এর alternative options, English, সাথে বাংলায় ছোট ব্যাখ্যা>
===CHECK===
<বাংলায় bullet: কোন data যাচাই করতে হবে>"""

DETECT_OUTPUT = """শুধু একটি JSON object দাও, অন্য কিছু নয়:
{"format": "<KEY বা NEW>", "column": "<column নাম বা খালি>", "reason": "<এক লাইন বাংলায়>"}
- Argument-ধর্মী প্রশ্ন (Should / Is / Do ...) হলে ARG।
- Focus topic হলে সংশ্লিষ্ট FOCUS-* key।
- Critical Thoughts হলে SRI / CBI / RME / TRJ / IEI / HLC / DJO / CEE / PIS।
- কোনো format না মিললে এবং PDF দিয়ে নতুন format দরকার হলে NEW।"""

EXPAND_TEXT = """নিচের উত্তরটি ছোট হয়েছে। একই skeleton, একই বাক্যসংখ্যা ও একই connector রেখে প্রতিটি বাক্য লম্বা করো।
প্রতিটি বাক্য কমপক্ষে {n} শব্দ। নতুন তথ্য, সংখ্যা বা উৎস বানাবে না; জানা না থাকলে {{[VERIFY: source + figure]}} বসাও।
যে অংশ নতুন ভরেছো বা বাড়িয়েছো, সেগুলো {{ }} এর ভেতরে দাও। শুধু উত্তরটি দাও, কোনো মন্তব্য নয়।

উত্তর:
{answer}"""

# ---------------- HELPERS ----------------


def secret(name, default=""):
    try:
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    return os.environ.get(name, default)


@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)


def run_model(api_key, model, contents, system, placeholder=None, temperature=0.3):
    last_err = None
    for _ in range(2):
        try:
            client = get_client(api_key)
            cfg = types.GenerateContentConfig(system_instruction=system, temperature=temperature)
            if placeholder is None:
                resp = client.models.generate_content(model=model, contents=contents, config=cfg)
                return resp.text or ""
            text = ""
            for chunk in client.models.generate_content_stream(model=model, contents=contents, config=cfg):
                if chunk.text:
                    text += chunk.text
                    placeholder.markdown(text)
            return text
        except Exception as e:
            last_err = e
            if "closed" in str(e).lower():
                get_client.clear()
                continue
            raise
    raise last_err


def key_test(api_key, model):
    if not api_key:
        return False, "API key নেই"
    try:
        out = run_model(
            api_key, model,
            [types.Content(role="user", parts=[types.Part.from_text(text="Reply with exactly: OK")])],
            "Reply briefly.", None, 0.0,
        )
        return True, out.strip()[:80]
    except Exception as e:
        return False, repr(e)


def esc(s):
    return html.escape(str(s), quote=False)


def plain(text):
    return FILL_RE.sub(r"\1", text)


def wc(text):
    return len(plain(text).split())


def render_answer(text):
    out, pos = [], 0
    for m in FILL_RE.finditer(text):
        out.append(esc(text[pos:m.start()]))
        out.append(f'<span style="color:{RED};font-weight:600">{esc(m.group(1))}</span>')
        pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out).replace("\n", "<br>")


def render_format(text):
    out, pos = [], 0
    for m in FMT_BLANK_RE.finditer(text):
        out.append(esc(text[pos:m.start()]))
        inner = m.group(1) if m.group(1) is not None else m.group(2)
        out.append(f'<span style="color:{BLUE};font-weight:600">[{esc(inner)}]</span>')
        pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out).replace("\n", "<br>")


def render_plain(text):
    return esc(text).replace("\n", "<br>")


def fmt_copy(text):
    return FILL_RE.sub(r"[\1]", text)


def parse_json(raw):
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {}


def split_sections(raw):
    out = {}
    parts = SECTION_RE.split(raw)
    for i in range(1, len(parts) - 1, 2):
        out[parts[i]] = parts[i + 1].strip()
    return out


def pick_default(q):
    t = q.strip()
    if "ARG" in FORMATS and ("?" in t or QUESTION_START.match(t) or "argument" in t.lower()):
        return "ARG"
    for k in ("FOCUS", "FOCUS-UNIVERSAL"):
        if k in FORMATS:
            return k
    return next(iter(FORMATS))


def column_for(key, data):
    cols = FORMATS[key].get("cols") or []
    if not cols:
        return None, None, ""
    want = str(data.get("column", "")).strip().lower()
    for i, c in enumerate(cols):
        cl = str(c).lower()
        if want and (want == cl or want in cl or cl in want):
            return i, c, ""
    return 0, cols[0], "⚠️ column AI ঠিক করতে পারেনি, প্রথমটি ধরা হয়েছে"


def plan_count(key):
    return len(FORMATS[key]["sentences"])


def rules_text(group, count, n):
    specific = {"ARG": ARG_RULES, "CT": CT_RULES, "FOCUS": FOCUS_RULES}.get(group, "")
    text = BASE_RULES + "\n\n" + specific
    return text.replace("{n}", str(n)).replace("{count}", str(count or 0))


def system_known(key, col_index, n):
    f = FORMATS[key]
    return "\n\n".join([
        rules_text(f["group"], len(f["sentences"]), n),
        "# FORMAT (এটি skeleton; বাক্যের ক্রম ও role অপরিবর্তিত)\n" + formats.prompt_block(key, col_index),
        KNOWN_OUTPUT,
    ])


def system_new(n):
    example = formats.template_text("FOCUS-UNIVERSAL") if "FOCUS-UNIVERSAL" in FORMATS else ""
    return "\n\n".join([
        BASE_RULES.replace("{n}", str(n)),
        formats.FORMAT_FROM_PDF_GUIDE,
        "# STYLE EXAMPLE (এই ধরনের format বানাও)\n" + example,
        NEW_OUTPUT,
    ])


def user_text(q, extra, n):
    return (
        f"প্রশ্ন / topic:\n{q.strip() or '(শুধু সংযুক্ত ফাইল/ছবি দেখো)'}\n\n"
        f"অতিরিক্ত নির্দেশনা (সর্বোচ্চ অগ্রাধিকার; তবু তথ্য বানাবে না):\n{extra.strip() or '—'}\n\n"
        f"শর্ত: প্রতি বাক্য কমপক্ষে {n} শব্দ।"
    )


def build_file_parts(pdfs, imgs):
    parts, size = [], 0
    for f in pdfs or []:
        data = f.getvalue()
        size += len(data)
        parts.append(types.Part.from_bytes(data=data, mime_type="application/pdf"))
    for f in imgs or []:
        data = f.getvalue()
        size += len(data)
        parts.append(types.Part.from_bytes(data=data, mime_type=f.type or "image/png"))
    for b in st.session_state.pasted:
        size += len(b)
        parts.append(types.Part.from_bytes(data=b, mime_type="image/png"))
    return parts, size


def detect_format(api_key, model, file_parts, q, extra):
    catalog = "\n".join(
        f"- {k} | group={f['group']} | use_for: {f.get('use_for', '')} | columns: "
        f"{', '.join(str(c) for c in (f.get('cols') or [])) or 'none'}"
        for k, f in FORMATS.items()
    )
    system = formats.IDENTIFY_GUIDE + "\n\n# FORMAT CATALOG\n" + catalog + "\n\n" + DETECT_OUTPUT
    text = f"প্রশ্ন/topic:\n{q}\n\nঅতিরিক্ত নির্দেশনা:\n{extra}"
    contents = [types.Content(role="user", parts=file_parts + [types.Part.from_text(text=text)])]
    raw = run_model(api_key, model, contents, system, None, 0.0)
    return parse_json(raw)


def build_result(raw, key, col_index, col_name, note, n):
    sec = split_sections(raw)
    if key is None:
        return {
            "key": None, "label": "NEW format (PDF থেকে তৈরি)", "col": "", "note": note,
            "format_text": sec.get("FORMAT", ""), "bank": sec.get("WORD BANK", ""),
            "ai_verify": sec.get("CHECK", ""), "check_items": [], "verify_fmt": "",
            "answer": sec.get("ANSWER") or raw, "group": None, "count": None, "n": n,
        }
    f = FORMATS[key]
    checks = [str(item) for item in formats.check_list(key)]
    return {
        "key": key, "label": formats.label(key), "col": col_name or "", "note": note,
        "format_text": formats.template_text(key),
        "bank": formats.bank_text(key, col_index),
        "ai_verify": sec.get("VERIFY", ""), "check_items": checks,
        "verify_fmt": str(f.get("verify", "") or ""),
        "answer": sec.get("ANSWER") or raw, "group": f["group"],
        "count": len(f["sentences"]), "n": n,
    }


def target_info(r, words):
    if r["group"] == "ARG":
        return f"লক্ষ্য {ARG_MIN}–{ARG_MAX}", words < ARG_MIN
    if r["count"]:
        goal = r["count"] * r["n"]
        return f"লক্ষ্য ≈ {goal} (বাক্য {r['count']} × {r['n']})", words < goal * 0.9
    return "", False


def password_gate():
    pw = secret("APP_PASSWORD")
    if not pw or st.session_state.get("authed"):
        return
    p = st.text_input("Password", type="password")
    if p and p == pw:
        st.session_state["authed"] = True
        st.rerun()
    elif p:
        st.error("ভুল password")
    st.stop()


def show_result(r, api_key, model, n):
    if not r:
        return
    st.divider()
    if st.button("🗑️ Result মুছো", key="clear_btn"):
        st.session_state.result = None
        st.rerun()

    st.subheader(r["label"] + (f"  |  column: {r['col']}" if r["col"] else ""))
    if r["note"]:
        if r["note"].startswith("⚠️"):
            st.warning(r["note"])
        else:
            st.caption(r["note"])

    st.markdown("### ১) Format (blank সহ)")
    st.markdown(render_format(r["format_text"]), unsafe_allow_html=True)
    with st.expander("📋 Format copy করো"):
        st.code(fmt_copy(r["format_text"]), language=None)

    st.markdown("### ২) Answer")
    st.markdown(render_answer(r["answer"]), unsafe_allow_html=True)
    words = wc(r["answer"])
    target_txt, low = target_info(r, words)
    st.caption(f"শব্দ সংখ্যা: {words}  |  {target_txt}")
    if low:
        st.warning("উত্তর লক্ষ্যের চেয়ে ছোট। নিচের 'আরও বিস্তারিত করো' চাপুন।")

    if st.button("➕ আরও বিস্তারিত করো (বাক্য লম্বা করো)", key="expand_btn"):
        ok = False
        try:
            system = rules_text(r["group"], r["count"], n) + "\n\n# OUTPUT: শুধু উত্তরটি দাও।"
            prompt = EXPAND_TEXT.replace("{n}", str(n)).replace("{answer}", r["answer"])
            with st.spinner("বাক্যগুলো লম্বা করা হচ্ছে..."):
                new = run_model(
                    api_key, model,
                    [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])],
                    system, None, 0.3,
                )
            if new.strip():
                r["answer"] = new.strip()
                st.session_state.result = r
                ok = True
        except Exception as e:
            st.error(f"ত্রুটি: {e!r}")
            st.code(traceback.format_exc())
        if ok:
            st.rerun()

    with st.expander("📋 Answer copy করো (plain text)"):
        st.code(plain(r["answer"]), language=None)

    with st.expander("🔤 শব্দভান্ডার (blank অনুযায়ী alternative words)", expanded=True):
        st.markdown(render_plain(r["bank"]), unsafe_allow_html=True)

    items = []
    if r["ai_verify"]:
        items.append(r["ai_verify"])
    for m in VERIFY_RE.finditer(r["answer"]):
        items.append("উত্তরে চিহ্নিত: " + m.group(1))
    items += r["check_items"]
    if r["verify_fmt"]:
        items.append(r["verify_fmt"])
    if items:
        st.warning("⚠️ **এই অংশের data যাচাই করে বসান**\n\n" + "\n".join(f"- {x}" for x in items))
    else:
        st.info("⚠️ এই অংশের data যাচাই করে বসান। উত্তরে আলাদা চিহ্ন নেই, তবু নিজে একবার দেখুন।")


# ---------------- APP ----------------

st.session_state.setdefault("pasted", [])
st.session_state.setdefault("pasted_hashes", set())
st.session_state.setdefault("result", None)

password_gate()

st.title("✍️ Exam Writer")

with st.sidebar:
    st.header("⚙️ Setting")
    typed = st.text_input("Gemini API Key", type="password")
    api_key = typed.strip() or secret("GEMINI_API_KEY")
    if typed.strip():
        st.caption("✅ Sidebar-এর key ব্যবহার হচ্ছে।")
    elif api_key:
        st.caption("✅ Secrets-এর key ব্যবহার হচ্ছে।")
    else:
        st.caption("⚠️ Key নেই।")

    model = st.text_input("Model name", value=secret("MODEL_NAME", DEFAULT_MODEL)).strip()
    st.caption("Model ID Google AI Studio থেকে হুবহু copy করো।")
    if st.button("🔑 Key test"):
        ok, msg = key_test(api_key, model)
        if ok:
            st.success(f"Key ঠিক আছে। উত্তর: {msg}")
        else:
            st.error(msg)

    n = st.number_input("প্রতি বাক্যে কমপক্ষে শব্দ", min_value=8, max_value=40, value=DEFAULT_N)
    st.caption("ARG: ৬ বাক্য × ২০ ≈ ১২০ শব্দ। Focus: বাক্য সংখ্যা × এই সংখ্যা।")

options = [AUTO] + list(FORMATS.keys()) + [NEW]


def fmt_label(x):
    if x == AUTO:
        return "AUTO — নিজে চিনবে (ARG / Focus / CT)"
    if x == NEW:
        return "NEW — PDF থেকে নতুন format বানাও"
    return formats.label(x)


choice = st.selectbox("Format", options, format_func=fmt_label)

manual_col = None
if choice not in (AUTO, NEW):
    cols = FORMATS[choice].get("cols") or []
    if cols:
        pick = st.selectbox("Topic column", ["AUTO"] + [str(c) for c in cols])
        manual_col = None if pick == "AUTO" else cols.index(pick)

q = st.text_area("প্রশ্ন / Focus name / topic", height=110,
                 placeholder="যেমন: Should Bangladesh adopt a cashless economy?  বা  Bangla QR")
extra = st.text_area("অতিরিক্ত নির্দেশনা (এটি সবচেয়ে বেশি মানা হবে)", height=80)
pdfs = st.file_uploader("PDF (একাধিক)", type=["pdf"], accept_multiple_files=True)
imgs = st.file_uploader("ছবি (একাধিক)", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True)

st.markdown("**📋 Clipboard থেকে screenshot**")
pb = paste_image_button(label="📋 Paste from clipboard", key="paste_btn", errors="ignore")
img = getattr(pb, "image_data", None) if pb is not None else None
if img is not None:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    data = buf.getvalue()
    h = hashlib.md5(data).hexdigest()
    if h not in st.session_state.pasted_hashes:
        st.session_state.pasted_hashes.add(h)
        st.session_state.pasted.append(data)
if st.session_state.pasted:
    cols_ui = st.columns(min(4, len(st.session_state.pasted)))
    for i, b in enumerate(st.session_state.pasted):
        with cols_ui[i % len(cols_ui)]:
            st.image(b, width=150)
    if st.button("🗑️ Paste ছবি মুছো"):
        st.session_state.pasted = []
        st.session_state.pasted_hashes = set()
        st.rerun()

write = st.button("✍️ লেখো", type="primary")

if write:
    if not api_key:
        st.error("API key দিন (sidebar অথবা Secrets)।")
        st.stop()
    file_parts, size = build_file_parts(pdfs, imgs)
    if size > MAX_TOTAL_MB * 1024 * 1024:
        st.error(f"ফাইল বেশি বড় ({MAX_TOTAL_MB} MB-এর বেশি)। কিছু ফাইল কমান।")
        st.stop()
    if not q.strip() and not file_parts:
        st.warning("প্রশ্ন লিখুন, অথবা PDF/ছবি দিন।")
        st.stop()

    n_int = int(n)
    try:
        if choice == AUTO:
            with st.spinner("Format চিনছি..."):
                data = detect_format(api_key, model, file_parts, q, extra)
            keymap = {k.upper(): k for k in FORMATS}
            raw_key = str(data.get("format", "")).strip().upper()
            if raw_key == NEW:
                key = None
                note = "নতুন format (PDF থেকে বানানো হবে)"
            elif raw_key in keymap:
                key = keymap[raw_key]
                note = str(data.get("reason", ""))
            else:
                key = pick_default(q)
                note = "⚠️ AI format চিনতে পারেনি, local guess: " + key
            col_index = col_name = None
            if key:
                col_index, col_name, cnote = column_for(key, data)
                if cnote:
                    note += " | " + cnote
        else:
            key = None if choice == NEW else choice
            col_index, col_name, note = manual_col, None, "Manual format"
            if key and FORMATS[key].get("cols"):
                if manual_col is None:
                    with st.spinner("Column চিনছি..."):
                        data = detect_format(api_key, model, file_parts, q, extra)
                    col_index, col_name, cnote = column_for(key, data)
                    if cnote:
                        note += " | " + cnote
                else:
                    col_name = str(FORMATS[key]["cols"][manual_col])

        system = system_new(n_int) if key is None else system_known(key, col_index, n_int)
        contents = [types.Content(
            role="user",
            parts=file_parts + [types.Part.from_text(text=user_text(q, extra, n_int))],
        )]
        ph = st.empty()
        raw = run_model(api_key, model, contents, system, ph, 0.3)
        ph.empty()
        st.session_state.result = build_result(raw, key, col_index, col_name, note, n_int)
    except Exception as e:
        st.error(f"ত্রুটি: {e!r}")
        st.code(traceback.format_exc())
        st.stop()

show_result(st.session_state.result, api_key, model, int(n))