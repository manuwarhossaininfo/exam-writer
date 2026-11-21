# formats_core.py  -- Critical Thinking (৯টি) + ARG + FOCUS (general)
from fmt_base import S, F, FMT

CORE = {}

CORE["SRI"] = FMT(
    "Strengthen the Reasoning", "CT",
    "কোন তথ্য conclusion-কে শক্তিশালী করবে, এমন প্রশ্ন",
    [
        S("S1", "Evidence", "The conclusion would be strengthened if evidence showed that [A], [B], and [C].",
          hints={"A": "প্রথম supporting evidence", "B": "দ্বিতীয় evidence", "C": "তৃতীয় evidence"}),
        S("S2", "Explain", "This information would support the conclusion because it demonstrates that [D] and reduces uncertainty regarding [E].",
          hints={"D": "evidence কী প্রমাণ করে", "E": "কোন অনিশ্চয়তা কমে"}),
        S("S3", "Result", "Therefore, the conclusion becomes more convincing, and confidence in [F] increases.",
          hints={"F": "conclusion-এর মূল দাবি"}),
    ])

CORE["CBI"] = FMT(
    "Critique / Weaken", "CT",
    "argument-এর দুর্বলতা বা critique চাওয়া হলে",
    [
        S("S1", "Weakness", "The [argument/plan] appears [weak/questionable] because it is primarily based on [A] while assuming that [B] without sufficient supporting evidence.",
          opts={"argument/plan": ["argument", "plan", "proposal"], "weak/questionable": ["weak", "questionable"]},
          hints={"A": "argument যার ওপর দাঁড়িয়ে", "B": "প্রমাণ ছাড়া ধরে নেওয়া অনুমান"}),
        S("S2", "Overlooked", "It overlooks factors such as [C], [D], [E], [F], which may significantly influence [G] and could lead to a different conclusion.",
          hints={"C": "বাদ পড়া factor ১", "D": "factor ২", "E": "factor ৩", "F": "factor ৪", "G": "যে outcome প্রভাবিত হবে"}),
        S("S3", "Recommend", "Therefore, before [H], a more comprehensive evaluation incorporating [I], [J], [K] is required to ensure the conclusion is objective, reliable, and well justified.",
          hints={"H": "কোন সিদ্ধান্ত নেওয়ার আগে", "I": "মূল্যায়নের বিষয় ১", "J": "বিষয় ২", "K": "বিষয় ৩"}),
    ])

CORE["RME"] = FMT(
    "Resolve the Paradox", "CT",
    "দুটি বিপরীত observation মিলিয়ে ব্যাখ্যা চাওয়া হলে",
    [
        S("S1", "Paradox", "The two observations appear contradictory because [A], while at the same time [B].",
          hints={"A": "প্রথম observation", "B": "বিপরীত observation"}),
        S("S2", "Reconcile", "However, this apparent contradiction can be explained if [C], since [D].",
          hints={"C": "মেলানোর ব্যাখ্যা", "D": "ব্যাখ্যার কারণ"}),
        S("S3", "Result", "Therefore, both statements can be true because [E], resolving the apparent contradiction logically.",
          hints={"E": "দুটিই সত্য হওয়ার কারণ"}),
    ])

CORE["TRJ"] = FMT(
    "Conclusion (Reasoned Judgement)", "CT",
    "তথ্য থেকে কী সিদ্ধান্তে আসা যায়, এমন প্রশ্ন",
    [
        S("S1", "Conclusion", "It can reasonably be concluded that [A].", hints={"A": "মূল সিদ্ধান্ত"}),
        S("S2", "Reason", "This conclusion is reasonable because [B], which indicates that [C].",
          hints={"B": "প্রদত্ত তথ্য", "C": "তথ্য কী নির্দেশ করে"}),
        S("S3", "Implication", "Therefore, [D] is likely to [E], provided that [F].",
          hints={"D": "বিষয়", "E": "সম্ভাব্য ফল", "F": "শর্ত"}),
    ])

CORE["IEI"] = FMT(
    "Inference", "CT",
    "'কী inference করা যায়' ধরনের প্রশ্ন",
    [
        S("S1", "Inference", "It can reasonably be inferred that [A].", hints={"A": "inference"}),
        S("S2", "Support", "This inference is supported because [B], which suggests that [C].",
          hints={"B": "সমর্থনকারী তথ্য", "C": "কী ইঙ্গিত দেয়"}),
        S("S3", "Implication", "Therefore, [D] is likely to [E], although [F].",
          hints={"D": "বিষয়", "E": "সম্ভাব্য ফল", "F": "সীমাবদ্ধতা"}),
    ])

CORE["HLC"] = FMT(
    "Assumption (Hidden Logical Component)", "CT",
    "'author/mayor/management কী assume করছেন' প্রশ্ন",
    [
        S("S1", "Assume", "The [author/mayor/management/expert] assumes that [A], and that [B].",
          opts={"author/mayor/management/expert": ["author", "mayor", "management", "expert", "government"]},
          hints={"A": "প্রথম assumption", "B": "দ্বিতীয় assumption"}),
        S("S2", "Necessary", "This assumption is necessary because [C] can [D] only if [E], which logically supports the [author's] conclusion.",
          hints={"C": "plan/প্রস্তাব", "D": "ফল দেবে", "E": "শর্ত"}),
        S("S3", "If false", "If this assumption does not hold true, the conclusion may not remain valid, and [F] may [G].",
          hints={"F": "বিষয়", "G": "ব্যর্থ হবে / ক্ষতি হবে"}),
    ],
    notes="চারটি সাধারণ assumption pattern: (১) অতীত ধারা ভবিষ্যতেও চলবে, (২) এক জায়গায় যা সত্য সর্বত্র সত্য, (৩) X-ই মূল কারণ ছিল, (৪) technology/মানুষ নির্ভরযোগ্যভাবে কাজ করবে।")

CORE["DJO"] = FMT(
    "Decision (Ethical / Judgement)", "CT",
    "কী করা উচিত বা নৈতিক সিদ্ধান্তের প্রশ্ন",
    [
        S("S1", "Decision", "The most appropriate course of action is to [A] while ensuring [B].",
          hints={"A": "সিদ্ধান্ত", "B": "নিশ্চিত করার বিষয়"}),
        S("S2", "Justify", "This decision is appropriate because [C], which helps [D] and maintains [E].",
          hints={"C": "কারণ", "D": "কী সাহায্য করে", "E": "কী বজায় থাকে"}),
        S("S3", "Outcome", "Therefore, this approach is likely to [F] while minimizing [G] and promoting [H].",
          hints={"F": "ফল", "G": "ঝুঁকি কমে", "H": "ভালো কিছু বাড়ে"}),
    ])

CORE["CEE"] = FMT(
    "Cause & Effect", "CT",
    "কারণ ও ফল বিশ্লেষণের প্রশ্ন",
    [
        S("S1", "Cause", "The primary cause of [A] is [B].", hints={"A": "ঘটনা", "B": "মূল কারণ"}),
        S("S2", "Effect", "This occurred because [C], which resulted in [D].", hints={"C": "পেছনের কারণ", "D": "ফল"}),
        S("S3", "Outlook", "Therefore, [E] is likely to [F], unless [G].", hints={"E": "বিষয়", "F": "সম্ভাব্য পরিণতি", "G": "ব্যতিক্রম শর্ত"}),
    ],
    notes="বিকল্প (একাধিক কারণ): 'The primary causes of [A] are [B], [C] and [D]. / As a result, [E], [F]. / Therefore, [measures] are essential to [purpose].'")

CORE["PIS"] = FMT(
    "Problem & Solution", "CT",
    "সমস্যা চিহ্নিত করে সমাধান চাওয়া হলে",
    [
        S("S1", "Problem", "The major problem is [A], which has arisen due to [B], [C], and [D].",
          hints={"A": "সমস্যা", "B": "কারণ ১", "C": "কারণ ২", "D": "কারণ ৩"}),
        S("S2", "Impact", "This problem has adversely affected [E], resulting in [F], [G], and [H].",
          hints={"E": "ক্ষতিগ্রস্ত খাত", "F": "ফল ১", "G": "ফল ২", "H": "ফল ৩"}),
        S("S3", "Solution", "Therefore, effective measures such as [I], [J], and [K] are necessary to address the problem and ensure [L].",
          hints={"I": "সমাধান ১", "J": "সমাধান ২", "K": "সমাধান ৩", "L": "লক্ষ্য"}),
    ])

CORE["ARG"] = FMT(
    "Short Compact Argument (6 sentences)", "ARG",
    "'Should...?', for-and-against, বা মত দিয়ে যুক্তি চাওয়া হলে",
    [
        S("S1", "Opinion", "Although [A], I believe that [B].",
          hints={"A": "বিপরীত মত", "B": "আমার মত"}),
        S("S2", "Argument 1", "Firstly, [A], although [B].",
          hints={"A": "প্রধান যুক্তি ১", "B": "counter-argument ১"}),
        S("S3", "Rebuttal 1", "However, [A] is less convincing because [B].",
          hints={"A": "counter-argument ১", "B": "কেন দুর্বল"}),
        S("S4", "Argument 2", "Secondly, [A], even though [B].",
          hints={"A": "প্রধান যুক্তি ২", "B": "counter-argument ২"}),
        S("S5", "Rebuttal 2", "Nevertheless, this viewpoint is less compelling because [A], making [B].",
          hints={"A": "কারণ", "B": "ফল"}),
        S("S6", "Conclusion", "Therefore, although [A], [B] should [C] to [D].",
          hints={"A": "বিপরীত মত", "B": "বিষয়", "C": "কাজ", "D": "উদ্দেশ্য"}),
    ],
    words="মোট 110–140 words, 6টি sentence, (1)–(6) নম্বর দিয়ে।",
    notes="ARG-তে Firstly/Secondly ব্যবহার হয়। Focus Writing-এ নয়, দুটি format মেশাবেন না। প্রশ্নের পক্ষ (For/Against) অনুযায়ী মত বেছে নিন।",
    verify="যুক্তির পক্ষে কোনো সংখ্যা দিলে source যাচাই করুন।")

CORE["FOCUS"] = FMT(
    "Focus Writing (general)", "FOCUS",
    "যে Focus Writing topic-এর জন্য নির্দিষ্ট format নেই",
    [
        S("S1", "Background", "[Topic] has become an important issue in [context] in recent years.",
          hints={"Topic": "বিষয়", "context": "দেশ/খাত"}),
        S("S2", "Thesis", "While [Topic] plays a vital role in [A], it also faces [B] that require urgent attention.",
          hints={"A": "ভূমিকা", "B": "সমস্যা"}),
        S("S3", "Outline", "This essay examines its [importance / causes], major challenges and possible solutions."),
        S("S4", "Point", "To begin with, [Topic] contributes significantly to [A].", hints={"A": "প্রধান অবদান/কারণ"}),
        S("S5", "Explain", "This is because [B], which [C].", hints={"B": "কারণ", "C": "ফল"}),
        S("S6", "Example", "According to [Source], [data point].",
          check="নির্ভরযোগ্য source ও সংখ্যা যাচাই করে বসান। না পেলে hedged wording (around, nearly)।"),
        S("S7", "Link", "Thus, [Topic] strengthens [D].", hints={"D": "বৃহত্তর লক্ষ্য"}),
        S("S8", "Point", "Moreover, [Topic] is closely linked with [E].", hints={"E": "সম্পর্কিত বিষয়"}),
        S("S9", "Explain", "[Explain how E works].", hints={}),
        S("S10", "Example", "For instance, [example with source].", check="উদাহরণের source/বছর যাচাই করুন।"),
        S("S11", "Link", "Therefore, [link to the broader goal]."),
        S("S12", "Point", "However, [Topic] faces several challenges."),
        S("S13", "Challenge", "A key problem is [F], resulting in [G].", hints={"F": "সমস্যা", "G": "প্রভাব"}),
        S("S14", "Challenge", "Additionally, [H] further limits its potential."),
        S("S15", "Solution", "To overcome these barriers, it is essential to [I] and [J].", hints={"I": "সমাধান ১", "J": "সমাধান ২"}),
        S("S16", "Nutshell", "In a nutshell, [Topic] is [key role] for Bangladesh."),
        S("S17", "Hope", "Hopefully, with [K] and [L], it can contribute to sustainable development."),
    ],
    title_rule="Title: প্রথম শব্দ capital; article, preposition, auxiliary verb, conjunction বাদে সব শব্দ capital। কলমে লিখলে underline।",
    words="Intro 60–70 | প্রতি body 110–150 | Conclusion 40–50 | মোট 350–450",
    notes="১৭ sentence: Intro 3 (Background, Thesis, Outline; quote নয়) + Body 3x4 (PEEL) + Conclusion 2 (Nutshell, Hope)। Para 1 শুরু 'To begin with'; Para 2 Moreover/In addition/Furthermore; Para 3 'However'। Firstly/Secondly/Lastly নয়। Example-এ source ও data sentence-এর ভেতরে। Graph/chart নয়।",
    verify="প্রতিটি body paragraph-এর data ও source যাচাই করুন।")