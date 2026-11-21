# formats.py
# সব ফরম্যাট একত্র করে, template / word bank / check list / prompt বানায়
import re
import importlib

FILL_OPEN = "{{"
FILL_CLOSE = "}}"
BLANK_RE = re.compile(r"\[([^\[\]]+)\]")

# ------------------------------------------------------------ লোড
FORMATS = {}
LOAD_ERRORS = {}


def _collect(mod):
    """module-এর ভেতরের সব 'ফরম্যাট dict' (CORE, FOCUS1, FOCUS2, FOCUS3 ...) খুঁজে আনে"""
    out = {}
    for name in dir(mod):
        if name.startswith("_"):
            continue
        v = getattr(mod, name)
        if (isinstance(v, dict) and v
                and all(isinstance(x, dict) and "sentences" in x for x in v.values())):
            out.update(v)
    return out


for _m in ("formats_core", "formats_focus1", "formats_focus2", "formats_focus3"):
    try:
        _mod = importlib.import_module(_m)
        _found = _collect(_mod)
        if not _found:
            LOAD_ERRORS[_m] = "এই ফাইলে কোনো ফরম্যাট dict পাওয়া যায়নি"
        FORMATS.update(_found)
    except ModuleNotFoundError as e:
        LOAD_ERRORS[_m] = "ফাইল নেই" if e.name == _m else str(e)
    except Exception as e:
        LOAD_ERRORS[_m] = repr(e)

if LOAD_ERRORS:
    print("formats.py সতর্কতা:", LOAD_ERRORS)

if not FORMATS:
    raise RuntimeError("কোনো format লোড হয়নি। কারণ: " + str(LOAD_ERRORS))


# ------------------------------------------------------------ helper
def keys():
    return list(FORMATS.keys())


def label(key):
    return key + " — " + FORMATS[key]["name"]


def blank_names(text):
    seen = []
    for m in BLANK_RE.findall(text):
        if m not in seen:
            seen.append(m)
    return seen


def _as_list(x):
    if x is None:
        return []
    if isinstance(x, str):
        return [x]
    return [str(i) for i in x if i is not None]


def _lines(x):
    """string বা list যাই হোক, অর্থপূর্ণ লাইনের তালিকা বানায়"""
    if x is None:
        return []
    if isinstance(x, str):
        return [ln.strip() for ln in x.split("\n") if ln.strip()]
    return [str(i).strip() for i in x if str(i).strip()]


def _opt_lines(v, cols, col_index):
    """(column নাম, option তালিকা) জোড়ার তালিকা ফেরত দেয়।"""
    if isinstance(v, tuple):
        if col_index is not None and cols and 0 <= col_index < len(cols):
            return [("", _as_list(v[col_index] if col_index < len(v) else None))]
        out = []
        for i, x in enumerate(v):
            name = cols[i] if cols and i < len(cols) else str(i + 1)
            out.append((name, _as_list(x)))
        return out
    return [("", _as_list(v))]


# ------------------------------------------------------------ template
def template_text(key):
    f = FORMATS[key]
    lines = [label(key), "ব্যবহার: " + f["use_for"], ""]
    for s in f["sentences"]:
        tag = "   (fixed)" if s["fixed"] else ""
        lines.append("(" + s["id"] + ") " + s["role"] + ": " + s["text"] + tag)
    if f["title_rule"]:
        lines += ["", "TITLE RULE: " + f["title_rule"]]
    if f["words"]:
        lines += ["WORDS: " + f["words"]]
    return "\n".join(lines)


# ------------------------------------------------------------ word bank
def _bank_block(opts, cols, col_index):
    block = []
    for name, v in opts.items():
        for col, items in _opt_lines(v, cols, col_index):
            if not items:
                continue
            head = "  [" + name + "]"
            if col:
                head += " (" + col + ")"
            block.append(head + ": " + " / ".join(items))
    return block


def bank_text(key, col_index=None):
    f = FORMATS[key]
    cols = f["cols"]
    lines = []
    shared = f.get("shared") or {}
    if shared:
        sb = _bank_block(shared, cols, col_index)
        if sb:
            lines.append("(সব বাক্যে ব্যবহৃত blank)")
            lines += sb
    for s in f["sentences"]:
        if s["fixed"] or not s["opts"]:
            continue
        block = _bank_block(s["opts"], cols, col_index)
        if block:
            lines.append("(" + s["id"] + ") " + s["role"])
            lines += block
    if not lines:
        return "(এই ফরম্যাটে নির্দিষ্ট word bank নেই; প্রশ্নের শব্দ দিয়ে blank পূরণ করো)"
    return "\n".join(lines)


# ------------------------------------------------------------ check list
def check_list(key):
    """[(বাক্য নম্বর, যাচাইয়ের নোট), ...]"""
    out = []
    for s in FORMATS[key]["sentences"]:
        if s.get("check"):
            out.append((s["id"], s["check"]))
    return out


def verify_list(key):
    return _lines(FORMATS[key].get("verify"))


# ------------------------------------------------------------ prompt
def prompt_block(key, col_index=None):
    f = FORMATS[key]
    parts = ["=== FORMAT " + key + " ===", template_text(key), ""]
    if f["cols"]:
        parts.append("TOPIC COLUMNS: " + " | ".join(f["cols"]))
        if col_index is not None and 0 <= col_index < len(f["cols"]):
            parts.append("SELECTED COLUMN: " + f["cols"][col_index])
        parts.append("")
    parts += ["WORD BANK:", bank_text(key, col_index), ""]
    chk = check_list(key)
    if chk:
        parts.append("CHECK (data যাচাইয়ের বিষয়):")
        parts += ["  (" + i + ") " + t for i, t in chk]
        parts.append("")
    notes = _lines(f.get("notes"))
    if notes:
        parts.append("NOTES:")
        parts += ["  - " + n for n in notes]
        parts.append("")
    know = _lines(f.get("knowledge"))
    if know:
        parts.append("KNOWLEDGE:")
        parts += ["  - " + k for k in know]
        parts.append("")
    ver = _lines(f.get("verify"))
    if ver:
        parts.append("VERIFY:")
        parts += ["  - " + v for v in ver]
    return "\n".join(parts)


# ------------------------------------------------------------ AI-এর জন্য নির্দেশ
IDENTIFY_GUIDE = """
FORMAT SELECTION RULES: choose exactly ONE format key for the question or topic.
Critical Thoughts (CT):
- strengthen the conclusion -> SRI
- weaken / critique -> CBI
- paradox -> RME
- conclusion -> TRJ
- inference -> IEI
- assumption -> HLC
- decision -> DJO
- cause-effect -> CEE
- problem-solution -> PIS
Argument:
- "Should...?", agree/disagree, for-and-against, "China or India?" -> ARG
Focus:
- Family Card / Farmer's Card -> FOCUS-PROGRAM
- SSN / Women-Centric / Targeted vs Universal -> FOCUS-POLICY
- climate, disaster, flood, cyclone, COP -> FOCUS-CLIMATE
- inflation, unemployment, depreciation, tax aversion -> FOCUS-MACRO-I
- export, RMG, labor, governance, external sector -> FOCUS-MACRO-II
- Iran-war economic effect, energy crisis, Hormuz -> FOCUS-GLOBAL-III
- Bangla QR, Cashless, Binimoy, digital payment -> FOCUS-DFI
- bank merger, reconstruction, resolution -> FOCUS-BANKRES
- US-Iran diplomacy, China, CMBEC, Teesta, Ganges, foreign policy -> FOCUS-IR
- any other policy / program / scheme -> FOCUS-UNIVERSAL
- other title-style topics -> FOCUS
Priority:
1. An explicitly named key always wins.
2. Iran war economic effect -> GLOBAL-III; diplomacy or foreign policy -> IR.
3. Family/Farmer -> PROGRAM before UNIVERSAL; SSN/Women/Targeted -> POLICY before UNIVERSAL.
4. RMG as a sector essay -> MACRO-II; RMG as a shock victim -> GLOBAL-III.
5. Digital payment topics -> DFI.
6. If no stored format fits and a PDF is given, build a NEW format from the PDF.
Never mix Argument rules (Firstly/Secondly) with Focus rules (avoid Firstly/Secondly).
"""

FORMAT_FROM_PDF_GUIDE = """
BUILD A FORMAT FROM THE PDF:
1. Extract the exact sentence skeleton (Intro 3, Body PEEL blocks, Conclusion 2).
   Write blanks as [A], [B] or [Name].
2. Mark sentences that have no blank as (fixed).
3. Extract every option table into a WORD BANK per blank. Use topic columns if the PDF has them.
4. List sentences that need data or a source as CHECK items. Never invent numbers.
5. Repair blanks that break grammar, and say which sentences were adapted.
6. Add the title rule, a word guide and a short knowledge list from the slides.
Output with the same layout as stored formats: TEMPLATE, WORD BANK, CHECK, NOTES.
"""