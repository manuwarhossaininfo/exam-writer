# fmt_base.py
# ফরম্যাট বানানোর তিনটি helper: S (blank বাক্য), F (fixed বাক্য), FMT (পুরো ফরম্যাট)

GROUPS = ("CT", "ARG", "FOCUS")


def _text(v):
    """None, list বা tuple যাই আসুক, একটি string বানিয়ে দেয়"""
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        return "\n".join(str(x) for x in v)
    return str(v)


def S(id, role, text, opts=None, check=None, hints=None):
    """Blank সহ বাক্য।
    opts = {"A": [...], "B": ("col1 মান", "col2 মান")}
      list  = যেকোনো একটি option
      tuple = column অনুযায়ী আলাদা মান (cols-এর ক্রমে)
    check = এই বাক্যের data যাচাইয়ের নোট
    """
    return {
        "id": str(id),
        "role": role,
        "text": text,
        "opts": opts or {},
        "fixed": False,
        "check": check,
        "hints": hints,
    }


def F(id, role, text, check=None):
    """Fixed বাক্য (কোনো blank নেই, হুবহু লিখতে হবে)।
    check = চাইলে data যাচাইয়ের নোট দেওয়া যায়।
    """
    return {
        "id": str(id),
        "role": role,
        "text": text,
        "opts": {},
        "fixed": True,
        "check": check,
        "hints": None,
    }


def FMT(name, group, use_for, sentences, title_rule="", words="",
        cols=None, shared=None, notes=None, knowledge=None, verify=None):
    """একটি পূর্ণ ফরম্যাট।"""
    if group not in GROUPS:
        raise ValueError("group অবশ্যই CT, ARG বা FOCUS হতে হবে: " + str(group))
    return {
        "name": name,
        "group": group,
        "use_for": use_for,
        "sentences": sentences,
        "title_rule": title_rule or "",
        "words": words or "",
        "cols": list(cols) if cols else [],
        "shared": shared or {},
        "notes": _text(notes),
        "knowledge": _text(knowledge),
        "verify": _text(verify),
    }