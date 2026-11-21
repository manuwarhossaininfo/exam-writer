# formats_focus1.py  -- UNIVERSAL, PROGRAM, POLICY
import re

from fmt_base import S, F, FMT

FOCUS1 = {}

_BLANK = re.compile(r"\[([^\]]+)\]")


def _op(text, o):
    """বাক্যের blank-এর নামের সঙ্গে মিলিয়ে column অনুযায়ী মান তুলে আনে"""
    return {k: o[k] for k in _BLANK.findall(text) if k in o}


def _s(sid, role, text, o, check=None):
    return S(sid, role, text, opts=_op(text, o), check=check)


TITLE_RULE = ("Title Case ব্যবহার করো: প্রতিটি মূল শব্দের প্রথম অক্ষর বড় হাতের, "
              "ছোট শব্দ (of, in, and, the, for) ছোট হাতের। শিরোনামের শেষে full stop বসবে না।")

# ---------------------------------------------------------------- UNIVERSAL
FOCUS1["FOCUS-UNIVERSAL"] = FMT(
    "Universal Focus (Policy / Program / Scheme)", "FOCUS",
    "যে policy, program বা scheme-এর জন্য নির্দিষ্ট format নেই (fallback)",
    [
        S("S1", "Background", "[Subject] has emerged as a significant [type] initiative aimed at addressing [problem] in [context].",
          opts={"type": ["social protection", "agricultural support", "economic development", "financial inclusion"]}),
        S("S2", "Thesis", "By targeting [target group], [Subject] seeks to enhance both [goal 1] and [goal 2], leading to [outcome 1] and [outcome 2]."),
        F("S3", "Outline", "This essay critically examines its key impacts, underlying challenges, and policy recommendations."),
        S("S4", "Point", "A fundamental impact of [Subject] lies in its contribution to [economic/social benefit]."),
        S("S5", "Explain", "This is particularly evident in the context of [context], where beneficiaries experience [effect] because [mechanism] operates through [how it works]."),
        S("S6", "Example", "According to [Ministry/Report/Year], [data or fact] shows that [result].",
          check="সঠিক report, বছর ও সংখ্যা যাচাই করে বসান। বানানো সংখ্যা নয়।"),
        S("S7", "Link", "This not only enhances [immediate benefit] but also stabilizes [broader system] at the [household / national] level."),
        S("S8", "Point", "Beyond [impact 1], [Subject] also generates significant [social / other] impacts."),
        S("S9", "Explain", "For instance, it directly influences [cause], which in turn improves [effect]."),
        S("S10", "Interpret", "This interconnected effect highlights that [key factor] plays a crucial role in promoting [social equity / inclusion / resilience].",
          check="চাইলে এখানে একটি data point যোগ করতে পারেন (source সহ)।"),
        S("S11", "Link", "Therefore, [Subject] contributes to broader development goals by strengthening [final link]."),
        S("S12", "Point", "However, the effectiveness of [Subject] is constrained by several structural and administrative challenges."),
        S("S13", "Challenge 1", "A key issue lies in [challenge 1], resulting in [impact] and reducing overall efficiency."),
        S("S14", "Challenge 2", "Additionally, problems such as [challenge 2] further limit its potential impact."),
        S("S15", "Recommend", "To address these challenges, the government should [recommendation 1] and [recommendation 2], ensuring [intended result]."),
        S("S16", "Conclusion", "In conclusion, [Subject] can contribute meaningfully to [broader goal] if [condition for success]."),
        S("S17", "Conclusion", "Thus, a well-designed and carefully monitored [Subject] can help build [final vision]."),
    ],
    title_rule=TITLE_RULE,
    notes=[
        "S15-S17 এবং title rule পুনর্গঠিত। আসল Focus Writing Session 1 slide-এর সঙ্গে মিলিয়ে নাও।",
        "Intro 3 বাক্য, কোনো quote নয়। Conclusion 2 বাক্য। Firstly/Secondly/Lastly এড়াতে হবে।",
    ],
)

# ---------------------------------------------------------------- shared skeleton (PROGRAM / POLICY)


def _skeleton(o):
    return [
        _s("S1", "Background", "[Subject] has emerged as a significant [type] initiative aimed at addressing [problem] in [context].", o),
        _s("S2", "Thesis", "By targeting [target group], [Subject] seeks to enhance both [goal 1] and [goal 2], leading to [outcome 1] and [outcome 2].", o),
        F("S3", "Outline", "This essay critically examines its key impacts, underlying challenges, and policy recommendations."),
        _s("S4", "Point", "A fundamental impact of [Subject] lies in its contribution to [economic/social benefit].", o),
        _s("S5", "Explain", "This is particularly evident in the context of [context], where beneficiaries experience [effect] because [mechanism] operates through [how it works].", o),
        _s("S6", "Example", "According to [Ministry/Report/Year], [data or fact] shows that [result].", o,
           check="সঠিক report, বছর ও সংখ্যা যাচাই করে বসান। বানানো সংখ্যা নয়।"),
        _s("S7", "Link", "This not only enhances [immediate benefit] but also stabilizes [broader system] at the [household / national] level.", o),
        _s("S8", "Point", "Beyond [impact 1], [Subject] also generates significant [social / other] impacts.", o),
        _s("S9", "Explain", "For instance, it directly influences [cause], which in turn improves [effect].", o),
        _s("S10", "Interpret", "This interconnected effect highlights that [key factor] plays a crucial role in promoting [social equity / inclusion / resilience].", o,
           check="চাইলে এখানে একটি data point যোগ করতে পারেন (source সহ)।"),
        _s("S11", "Link", "Therefore, [Subject] contributes to broader development goals by strengthening [final link].", o),
        _s("S12", "Point", "However, the effectiveness of [Subject] is constrained by several structural and administrative challenges.", o),
        _s("S13", "Challenge 1", "A key issue lies in [challenge 1], resulting in [impact] and reducing overall efficiency.", o),
        _s("S14", "Challenge 2", "Additionally, problems such as [challenge 2] further limit its potential impact.", o),
        _s("S15", "Recommend", "To address these challenges, the government should [recommendation 1] and [recommendation 2], ensuring [intended result].", o),
        _s("S16", "Conclusion", "In conclusion, [Subject] can contribute meaningfully to [broader goal] if [condition for success].", o),
        _s("S17", "Conclusion", "Thus, a well-designed and carefully monitored [Subject] can help build [final vision].", o),
    ]


# ---------------------------------------------------------------- PROGRAM
_PROGRAM_O = {
    "Subject": ("Family Card", "Farmer's Card"),
    "type": ("social protection", "agricultural support"),
    "problem": ("targeting errors and leakage in welfare delivery",
                "high input costs and unequal access to subsidies and credit"),
    "context": ("household-level welfare delivery in Bangladesh",
                "Bangladesh's agrarian economy"),
    "target group": ("low-income households", "small and marginal farmers"),
    "goal 1": ("income security", "farm productivity"),
    "goal 2": ("food security", "farmers' income stability"),
    "outcome 1": ("reduced vulnerability", "higher agricultural output"),
    "outcome 2": ("better targeting of benefits", "stable rural livelihoods"),
    "economic/social benefit": ("household income security", "farm productivity and farmers' income"),
    "challenge 1": ("inaccurate beneficiary identification and weak data systems",
                    "the lack of a reliable farmer database, which excludes tenant farmers"),
    "challenge 2": ("limited administrative capacity and the risk of political influence",
                    "middlemen interference and delayed disbursement"),
    "recommendation 1": ("build a verified digital household database",
                         "build a verified digital farmer database including tenant farmers"),
    "recommendation 2": ("strengthen monitoring and grievance redress",
                         "pay benefits directly through digital channels"),
}

FOCUS1["FOCUS-PROGRAM"] = FMT(
    "Program Focus (Family Card / Farmer's Card)", "FOCUS",
    "কোনো সরকারি program বা card (Family Card, Farmer's Card ইত্যাদি) নিয়ে Focus Writing",
    _skeleton(_PROGRAM_O),
    title_rule=TITLE_RULE,
    cols=["Family Card", "Farmer's Card"],
    notes=[
        "Column-এর শব্দ সাধারণ ধারণা। Skeleton Version - 02.pdf-এর সঙ্গে মিলিয়ে নাও।",
        "Example (S6)-তে সঠিক source ও সংখ্যা তুমি বসাবে, AI বানাবে না।",
    ],
)

# ---------------------------------------------------------------- POLICY
_POLICY_O = {
    "Subject": ("The Social Safety Net (SSN) policy",
                "Women-centric policy",
                "The targeted versus universal approach"),
    "type": ("social protection", "gender-inclusive development", "social protection design"),
    "problem": ("poverty, vulnerability and income shocks",
                "gender gaps in income, education and workforce participation",
                "the efficient use of limited welfare resources"),
    "context": ("Bangladesh", "Bangladesh's households and labour market",
                "Bangladesh's social protection system"),
    "target group": ("the poor and vulnerable groups", "women",
                     "poor households (targeted) or all citizens (universal)"),
    "goal 1": ("income security", "women's economic empowerment", "equity"),
    "goal 2": ("food security", "social inclusion", "administrative efficiency"),
    "outcome 1": ("reduced poverty", "higher female workforce participation",
                  "better coverage of the needy"),
    "outcome 2": ("greater resilience", "stronger household welfare",
                  "lower leakage and cost"),
    "economic/social benefit": ("income stability of vulnerable households",
                                "women's economic participation",
                                "efficient and fair welfare spending"),
    "challenge 1": ("exclusion and inclusion errors in beneficiary selection",
                    "social norms and unequal access to resources and services",
                    "exclusion errors under targeting and high fiscal cost under universal coverage"),
    "challenge 2": ("weak monitoring and leakage",
                    "limited access to credit, skills and safe workplaces",
                    "weak data systems for identifying beneficiaries"),
    "recommendation 1": ("digitise beneficiary databases",
                         "expand skills training and access to finance for women",
                         "combine targeting with a basic universal floor"),
    "recommendation 2": ("strengthen monitoring and grievance redress",
                         "ensure safe and supportive workplaces",
                         "strengthen data and delivery systems"),
}

FOCUS1["FOCUS-POLICY"] = FMT(
    "Policy Focus (SSN / Women-Centric / Targeted vs Universal)", "FOCUS",
    "কোনো policy (SSN, Women-Centric policy, Targeted vs Universal ইত্যাদি) নিয়ে Focus Writing",
    _skeleton(_POLICY_O),
    title_rule=TITLE_RULE,
    cols=["SSN", "Women-Centric", "Targeted vs Universal"],
    notes=[
        "Column-এর শব্দ সাধারণ ধারণা। Skeleton Version - 02.pdf-এর সঙ্গে মিলিয়ে নাও।",
        "Targeted vs Universal column-এ Subject বাক্যটি কিছুটা আলগা শোনাতে পারে, চাইলে নিজে বদলাও।",
        "Example (S6)-তে সঠিক source ও সংখ্যা তুমি বসাবে, AI বানাবে না।",
    ],
)