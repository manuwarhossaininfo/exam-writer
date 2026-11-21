
# formats_focus3.py  -- DFI, BANKRES, IR
from fmt_base import S, F, FMT

FOCUS3 = {}

# ================================================================ DFI
FOCUS3["FOCUS-DFI"] = FMT(
    "Digital Financial Inclusion (Bangla QR, Cashless BD)", "FOCUS",
    "Bangla QR, Cashless Bangladesh, Digital Payment, Financial Inclusion, Cybersecurity in payments",
    [
        S("S1", "Background", "[Subject] refers to a modern digital payment system that enables secure, fast and interoperable financial transactions across different payment platforms."),
        S("S2", "Thesis", "In Bangladesh, [Subject] has become an effective tool for promoting financial inclusion, payment efficiency and transparency in everyday transactions."),
        S("S3", "Outline", "This essay discusses the importance, challenges and future prospects of [Subject] in strengthening Bangladesh's digital financial ecosystem."),
        S("S4", "Point", "To begin with, [Subject] has simplified retail payments by creating a unified and interoperable payment network."),
        S("S5", "Explain", "As a result, customers can make [Customer Benefit] payments while merchants benefit from [Merchant Benefit].",
          opts={"Customer Benefit": ["instant", "secure"], "Merchant Benefit": ["faster settlement", "lower transaction costs"]}),
        S("S6", "Example", "According to Bangladesh Bank, the rapid growth of digital [Data] and merchant participation reflects the increasing acceptance of this payment system.",
          opts={"Data": ["transaction volume", "transaction value"]},
          check="Bangladesh Bank Payment Systems Department-এর সর্বশেষ সংখ্যা ও বছর যাচাই করে বসান। বানানো সংখ্যা নয়।"),
        S("S7", "Link", "Therefore, this [Initiative] initiative has significantly strengthened Bangladesh's journey towards a modern [Goal].",
          opts={"Initiative": ["Bangla QR", "digital payment"], "Goal": ["Cashless Bangladesh", "digital economy"]}),
        S("S8", "Point", "Furthermore, [Subject] has expanded financial inclusion by connecting unbanked people with formal financial services."),
        F("S9", "Explain", "Every digital transaction creates a financial record, making it easier for banks to evaluate customers and provide financial services."),
        F("S10", "Example", "According to the World Bank Global Findex, digital financial services have substantially increased account ownership in developing economies.",
          check="Global Findex-এর সর্বশেষ সংস্করণ ও বছর যাচাই করুন।"),
        F("S11", "Link", "Consequently, digital payments are supporting inclusive and sustainable economic growth."),
        S("S12", "Point", "However, several technological and institutional challenges still hinder the successful expansion of [Subject]."),
        F("S13", "Explain", "Cybersecurity risks, limited digital literacy and unequal internet access remain major concerns across the country."),
        F("S14", "Example", "Recognising these risks, Bangladesh Bank has introduced stronger cybersecurity guidelines and digital payment regulations.",
          check="Bangladesh Bank ICT Security Guidelines-এর সঠিক নাম/বছর যাচাই করুন।"),
        F("S15", "Link", "Therefore, continuous investment in technology and public awareness is essential for long-term success."),
        S("S16", "Nutshell", "In conclusion, [Subject] has become a key driver of Bangladesh's digital financial transformation."),
        F("S17", "Opinion", "In my opinion, stronger digital infrastructure and effective regulation will ensure the sustainable growth of this initiative."),
    ],
    shared={"Subject": ["Bangla QR", "Cashless Bangladesh", "Digital Payment"]},
    title_rule="'Bangla QR: Transforming Digital Payments in Bangladesh' / 'Cashless Bangladesh: Towards a Digital Payment Economy'",
    words="Intro ~60 | প্রতি body 110–140 | Conclusion ~45",
    knowledge=(
        "BANGLA QR: জাতীয় interoperable QR payment system, Bangladesh Bank চালু করেছে। Slogan: One Country, One QR। Regulator: Bangladesh Bank; infrastructure: NPSB। "
        "Timeline: concept 2020–2021; pilot (Motijheel) 18 January 2023; nationwide 2023 onwards। "
        "Objectives: cashless economy, interoperability, digital commerce, financial inclusion, transparency, lower cash cost। "
        "Steps: merchant QR দেখায় → customer app খোলে → scan → amount → PIN/biometric → NPSB-এর মাধ্যমে instant transfer। "
        "Customer benefit: এক QR সব ব্যাংক/MFS, cash বহন নেই, accurate amount, digital history, better credit profile। "
        "Merchant benefit: এক QR, দামি POS লাগে না, instant settlement, cash ঝুঁকি কম, সহজ হিসাব। "
        "Importance: cashless economy, inclusion, কম transaction cost, transparency, digital commerce, tax compliance। "
        "Limitations: smartphone ও internet নির্ভরতা, MDR, low digital literacy, fake QR sticker, power/network সমস্যা। "
        "Bangla QR vs Binimoy: Bangla QR = merchant payment, QR code, active; Binimoy = P2P transfer, payment ID, failed/discontinued। "
        "Binimoy ব্যর্থতার কারণ: operational irregularities, poor user experience, কম অংশগ্রহণকারী প্রতিষ্ঠান, high interoperability cost, regulatory concerns।\n"
        "CASHLESS BANGLADESH: Bangladesh Bank-led উদ্যোগ, cash-dependent থেকে digital payment economy। Tools: mobile banking, internet banking, card, Bangla QR। "
        "Objectives: cash নির্ভরতা কমানো, digital service বাড়ানো, inclusion, transparency, digital economy, cash management cost কমানো, Smart Bangladesh। "
        "Benefits: কম currency cost, দ্রুত লেনদেন, tax collection, কম corruption ও laundering, business efficiency, innovation, কম cash theft। "
        "Challenges: digital divide, limited internet, low literacy, cybersecurity, power outage, smartphone dependency, informal sector exclusion। "
        "Recommended approach = Cash-lite Economy। Vision vs Tool: Cashless Bangladesh = Vision; Bangla QR = Implementation Tool। "
        "Inclusion: unbanked-দের formal system-এ আনা, transaction history, loan access, G2P transfer, microfinance ও insurance।"),
    notes=("Topic Cashless Bangladesh হলে Subject বদলান এবং Vision vs Tool, Cash-lite যোগ করুন। Financial Inclusion হলে 'digital financial inclusion', Cybersecurity হলে 'digital payment security' ব্যবহার করে S12 জোরালো করুন। "
           "S5-এর PDF ভাঙা grammar মেরামত (adapted)। 'Bangla QR vs Binimoy' বা 'Why did Binimoy fail?' প্রশ্নে knowledge bank থেকে body সাজান।"),
    verify="S6 (Bangladesh Bank data), S10 (Findex), S14 (guideline নাম)।")

# ================================================================ BANKRES
FOCUS3["FOCUS-BANKRES"] = FMT(
    "Bank Reconstruction & Merger Framework", "FOCUS",
    "Bank Reconstruction, Bank Merger, Role of Bangladesh Bank in Resolution, Challenges of Merger, Too Big to Fail",
    [
        S("S1", "Background", "[A] refers to a [B] framework designed to [C] financially distressed banks while protecting [D] and maintaining [E].",
          opts={"A": ["Reconstruction and Merger Framework", "Bank Resolution Framework", "Bank Reconstruction"],
                "B": ["comprehensive", "modern", "legal", "regulatory"],
                "C": ["reconstruct", "resolve", "rehabilitate", "reorganise"],
                "D": ["depositors", "public confidence", "financial institutions"],
                "E": ["financial stability", "banking stability", "systemic stability"]}),
        S("S2", "Thesis", "In Bangladesh, [A] has become an [B] policy instrument for strengthening [C], reducing [D] and restoring [E] across the banking industry.",
          opts={"A": ["this framework", "Bangladesh Bank's resolution mechanism", "the new banking law"],
                "B": ["effective", "strategic", "important"],
                "C": ["banking discipline", "corporate governance", "financial resilience"],
                "D": ["systemic risk", "banking instability", "financial distress"],
                "E": ["public confidence", "depositor trust", "financial stability"]}),
        S("S3", "Outline", "This essay discusses the [A], [B] and [C] of [D] in Bangladesh.",
          opts={"A": ["importance", "significance"], "B": ["challenges", "limitations"],
                "C": ["future prospects", "policy implications"],
                "D": ["bank reconstruction", "bank merger", "the Reconstruction and Merger Framework"]}),
        S("S4", "Point", "To begin with, the primary objective of [A] is to [B] financially distressed banks instead of [C] them, thereby minimising disruptions to the financial system.",
          opts={"A": ["the framework", "bank reconstruction", "bank resolution"],
                "B": ["restore", "rehabilitate", "stabilise"],
                "C": ["liquidating", "closing", "dissolving"]}),
        S("S5", "Explain", "Instead of allowing a troubled bank to fail, Bangladesh Bank may [A] the existing board, [B] an administrator and [C] the bank's financial structure for long-term sustainability.",
          opts={"A": ["dissolve", "remove", "replace"], "B": ["appoint", "nominate"],
                "C": ["restructure", "recapitalise", "reorganise"]}),
        S("S6", "Example", "For example, according to Bangladesh Bank, recent [A] initiatives have been introduced to strengthen weak banks and improve overall financial stability in Bangladesh.",
          opts={"A": ["reconstruction", "merger", "supervisory", "resolution"]},
          check="Source: Bangladesh Bank Financial Stability Report। সঠিক সংস্করণ/বছর যাচাই করুন।"),
        S("S7", "Link", "Therefore, this framework significantly [A] systemic risk while [B] public confidence in the country's banking system.",
          opts={"A": ["reduces", "minimizes", "mitigates"], "B": ["preserving", "strengthening", "restoring"]}),
        S("S8", "Point", "Furthermore, [A] promotes sound corporate governance by ensuring greater transparency, accountability and [B] throughout the restructuring process.",
          opts={"A": ["the framework", "Bangladesh Bank", "bank reconstruction"],
                "B": ["regulatory compliance", "institutional discipline"]}),
        S("S9", "Explain", "During reconstruction or merger, Bangladesh Bank can [A] directors, [B] qualified administrators and [C] the financial position of the affected bank before taking final decisions.",
          opts={"A": ["remove", "replace"], "B": ["appoint", "assign"], "C": ["assess", "evaluate", "audit"]}),
        S("S10", "Example", "According to the IMF and the World Bank, timely bank resolution and effective supervision are essential for maintaining a stable and resilient financial sector.",
          check="Source: IMF FSAP; World Bank Financial Sector Report। সঠিক report/বছর যাচাই করুন।"),
        S("S11", "Link", "Consequently, stronger [A] and more effective [B] contribute to sustainable banking development and long-term financial resilience.",
          opts={"A": ["governance", "supervision"], "B": ["regulation", "oversight", "policy implementation"]}),
        S("S12", "Point", "However, the successful implementation of [A] still faces several [B] and [C] challenges in Bangladesh.",
          opts={"A": ["bank merger", "the reconstruction framework", "bank resolution"],
                "B": ["institutional", "regulatory"], "C": ["operational", "governance", "legal"]}),
        S("S13", "Explain", "High non-performing loans (NPLs), weak corporate governance, lengthy legal procedures and occasional [A] may slow down the implementation of banking reforms.",
          opts={"A": ["political interference", "administrative delays"]}),
        S("S14", "Example", "Recognising these challenges, Bangladesh Bank has introduced [A] guidelines, strengthened regulatory oversight and expanded [B] supervision to improve the effectiveness of bank resolution.",
          opts={"A": ["merger", "reconstruction"], "B": ["risk-based", "prudential"]},
          check="Source: Bangladesh Bank Merger Guidelines। সঠিক নাম/বছর যাচাই করুন; আইনের নাম না জানলে বানাবেন না।"),
        S("S15", "Link", "Therefore, consistent policy implementation, stronger institutional independence and effective [A] will determine the long-term success of banking sector reforms.",
          opts={"A": ["regulatory enforcement", "governance"]}),
        S("S16", "Nutshell", "In conclusion, [A] has become an essential [B] for protecting [C] and strengthening [D] in Bangladesh.",
          opts={"A": ["the Reconstruction and Merger Framework", "bank resolution"],
                "B": ["regulatory mechanism", "policy instrument"],
                "C": ["depositors", "public confidence"],
                "D": ["financial stability", "banking resilience"]}),
        S("S17", "Opinion", "In my opinion, if Bangladesh ensures transparent governance, effective supervision and [A], this framework will play a crucial role in building a stronger, more resilient and internationally competitive banking sector.",
          opts={"A": ["timely policy implementation", "regulatory independence", "institutional accountability"]}),
    ],
    title_rule="'Bank Merger in Bangladesh: Prospects and Challenges' / 'Role of Bangladesh Bank in Bank Resolution'",
    words="Intro ~65 | প্রতি body 110–150 | Conclusion ~50",
    knowledge=(
        "Core philosophy: Too Big to Fail; liquidation = last resort। "
        "Objectives: financial stability ও depositor protection, bank failure ঠেকানো, systemic risk কমানো, confidence ফেরানো, service-এর ধারাবাহিকতা। "
        "Trigger points: low CRAR, high NPL, liquidity crisis, persistent loss, governance failure, fraud। "
        "Reconstruction steps: board removal → BB-নিযুক্ত administrator → capital restructuring → NPL recovery → operational restructuring; bank-এর identity বজায় থাকে। "
        "Capital restructuring: new investor, rights issue, share value adjustment, government support। Special Loan Recovery Cell: willful defaulter-দের কাছ থেকে বড় ঋণ আদায়। "
        "Merger types: Voluntary (mutual decision + BB approval) ও Compulsory (BB-র আদেশ, জনস্বার্থে)। "
        "Safeguards: independent asset/liability valuation, depositors = highest priority, willful defaulter-দের relief নেই, employee job protection, BB supervision। "
        "Macro impact: stability, stronger banks, confidence, better resource utilisation। "
        "Reconstruction vs Merger: revive existing bank / identity বজায় / internal rehabilitation বনাম combine with another bank / identity হারায় / legal amalgamation। "
        "8 Challenges of merger: weak asset quality, inaccurate valuation, governance problems, employee integration, technology (CBS) integration, public confidence, legal complexity, moral hazard। "
        "Rushed কি না: Supporters = কিছু ব্যাংক টিকত না, দেরিতে systemic risk বাড়ত। Critics = deep asset-quality review-এর আগে merger, দুর্বল communication, governance reform দরকার। "
        "Verdict: merger = resolution tool, magic solution নয়; সাফল্য post-merger reform-এর ওপর।"),
    notes=("S1-এ B-তে 'regulatory' বাছলে 'regulatory regulatory' হয় না, তবে 'framework' আগে থাকলে অন্য option ভালো। S5 ও S9 কাছাকাছি, S5-এ structure (board, administrator), S9-এ assessment ও final decision জোর দিন। "
           "প্রশ্ন 'merger কি rushed?' হলে ARG-ও ব্যবহার করা যায়। S8 PDF-এ B, C একক option ছিল, তাই fixed রাখা।"),
    verify="S6, S10, S14-এর source; আইনের সঠিক নাম; সাম্প্রতিক merger-এর খবর।")

# ================================================================ IR
FOCUS3["FOCUS-IR"] = FMT(
    "Contemporary International Relations", "FOCUS",
    "US–Iran Conflict (কূটনৈতিক/ভূরাজনৈতিক), Bangladesh–China, CMBEC, Water Diplomacy (Ganges, Teesta), Foreign Policy",
    [
        S("S1", "Background", "[A] refers to a [B] issue that significantly influences Bangladesh's economy, diplomacy and [C] in an increasingly interconnected world.",
          opts={"A": ("the US–Iran conflict", "Bangladesh–China relations", "the China–Myanmar–Bangladesh Economic Corridor (CMBEC)", "Bangladesh–India water diplomacy", "Bangladesh's foreign policy"),
                "B": ["geopolitical", "strategic", "international"],
                "C": ["national security", "foreign trade"]}),
        S("S2", "Thesis", "As a strategically located country, Bangladesh has adopted a [A] foreign policy to protect its [B], strengthen [C] and maintain [D] with major global powers.",
          opts={"A": ["balanced", "pragmatic", "independent"], "B": ["national interests", "economic interests"],
                "C": ["regional cooperation", "international partnerships"], "D": ["diplomatic neutrality", "strategic balance"]}),
        S("S3", "Outline", "This essay discusses the [A], [B] and [C] of [Topic] from Bangladesh's perspective.",
          opts={"A": ["opportunities", "significance"], "B": ["challenges", "geopolitical implications"], "C": ["future prospects", "policy responses"]}),
        S("S4", "Point", "To begin with, [Topic] has a profound impact on Bangladesh's economy, foreign trade and [A].",
          opts={"A": ("energy security", "diplomatic relations", "regional stability", "regional stability", "diplomatic relations")}),
        S("S5", "Explain", "As Bangladesh remains highly dependent on [A], any major geopolitical development may disrupt [B], increase [C] and create uncertainty in the national economy.",
          opts={"A": ["international trade", "imported energy", "export markets"],
                "B": ["global supply chains", "trade routes"], "C": ["import costs", "inflation", "logistics expenses"]}),
        S("S6", "Example", "For example, according to the [A], geopolitical conflicts frequently increase energy prices, disrupt global trade and weaken economic growth in many developing countries.",
          opts={"A": ["World Bank", "IMF", "International Energy Agency (IEA)", "World Trade Organization (WTO)"]},
          check="Report-এর নাম ও বছর যাচাই করে বসান।"),
        S("S7", "Link", "Therefore, Bangladesh must continuously monitor global developments and adopt timely policies to [A] [B].",
          opts={"A": ["minimize", "reduce", "manage"], "B": ["economic shocks", "geopolitical risks"]}),
        S("S8", "Point", "Furthermore, [A] creates significant opportunities for Bangladesh by expanding trade opportunities, attracting foreign investment and strengthening [B].",
          opts={"A": ("trade diversification", "strategic diplomacy", "regional cooperation", "regional cooperation", "international partnerships"),
                "B": ["economic resilience", "diplomatic influence"]}),
        F("S9", "Explain", "Through balanced diplomacy, Bangladesh can diversify its export markets, strengthen regional connectivity and enhance cooperation with both regional and global partners."),
        S("S10", "Example", "According to the [A], Bangladesh's strategic location and growing economy have increased its importance in regional trade and connectivity initiatives.",
          opts={"A": ["Asian Development Bank (ADB)", "World Bank", "UNESCAP"]},
          check="Report-এর নাম ও বছর যাচাই করুন।"),
        F("S11", "Link", "Consequently, effective diplomacy can transform geopolitical challenges into long-term economic opportunities."),
        S("S12", "Point", "However, Bangladesh also faces several geopolitical and [A] challenges while maintaining balanced relations with major global powers.",
          opts={"A": ("economic", "strategic", "strategic", "diplomatic", "diplomatic")}),
        F("S13", "Explain", "Great-power competition, regional conflicts, climate-related risks and supply-chain disruptions continue to increase uncertainty in Bangladesh's foreign and economic policies."),
        F("S14", "Example", "Recognising these challenges, Bangladesh has continued to promote regional cooperation, economic diplomacy and the principle of “Friendship to All, Malice Towards None.”",
          check="Source: Ministry of Foreign Affairs; Perspective Plan। সঠিক নথি যাচাই করুন।"),
        F("S15", "Link", "Therefore, a balanced, pragmatic and forward-looking foreign policy will remain essential for protecting Bangladesh's national interests in a rapidly changing world."),
        S("S16", "Nutshell", "In conclusion, [Topic] presents both significant opportunities and challenges for Bangladesh in the contemporary global environment."),
        S("S17", "Opinion", "It is hoped that, by strengthening strategic diplomacy, promoting [A] and safeguarding [B], Bangladesh can successfully navigate future geopolitical uncertainties and achieve sustainable national development.",
          opts={"A": ["international cooperation", "economic diversification"],
                "B": ["national interests", "economic security", "regional stability"]}),
    ],
    cols=("US–Iran Conflict", "Bangladesh–China", "CMBEC", "Water Diplomacy", "Foreign Policy"),
    shared={"Topic": ("the US–Iran conflict", "Bangladesh–China relations", "CMBEC", "Bangladesh–India water diplomacy", "Bangladesh's foreign policy")},
    title_rule="'Bangladesh–China Relations: Opportunities and Challenges' / 'Impact of the US–Iran Conflict on Bangladesh'",
    words="Intro ~65 | প্রতি body 110–150 | Conclusion ~50",
    knowledge=(
        "US–IRAN: Geopolitics → Energy → Inflation। Bangladesh নির্ভর: imported fuel, remittance, shipping, RMG। "
        "তেলের দাম বাড়লে বিদ্যুৎ, পরিবহন ও উৎপাদন ব্যয় বাড়ে → cost-push inflation। Remittance কমার ঝুঁকি; freight, marine insurance, delay বাড়ে; export competitiveness কমে। "
        "Opportunities: sourcing diversification, নিরাপদ hub হিসেবে extra RMG order, labour market, diplomatic importance। "
        "BB response: import compression, managed float, currency swap, forex reserve protection, LC margin increase, remittance incentive; primary objective = dollar reserve রক্ষা। "
        "Critical view: economic preparedness > political prediction; উপায়: energy ও trade diversification, forex management, neutral diplomacy।\n"
        "CHINA (2026): Enhanced Strategic Partnership। পাঁচ pillar: CEIZ, Mongla Port, Teesta Cooperation, GDI, 2+2 Dialogue। "
        "Benefits: FDI, employment, infrastructure, export opportunity, zero tariff access। Risks: debt sustainability, trade deficit, project implementation, strategic dependency। Policy: Strategic Balancing Diplomacy।\n"
        "CMBEC: China-র BRI-এর অংশ, Yunnan থেকে Myanmar-Bangladesh হয়ে Bay of Bengal। Benefits: faster logistics, কম transport cost, port development, transit revenue। "
        "5 obstacles: Myanmar civil war, Rohingya crisis, security risk (সবচেয়ে বড়), India's concern, US competition। Verdict: economically attractive, কিন্তু Myanmar-এর স্থিতিশীলতার ওপর নির্ভরশীল।\n"
        "WATER DIPLOMACY: transboundary river sharing; food security, energy, agriculture, national security। Ganges Treaty 2026 expected: renewal, minimum guaranteed flow, environmental protection। "
        "Teesta: Chinese investment বনাম Indian cooperation। Best strategy: Water Sharing আগে, Project Financing পরে।\n"
        "FOREIGN POLICY: 'Friendship to All, Malice Towards None'। Strategic autonomy, economic diplomacy, multi-vector, balanced relations (China, India, US, Japan, EU, Middle East)। "
        "Examiner's Q: China না India? উত্তর: কোনো একপক্ষ নয়, interest-based balance। China = economic cooperation, India = history ও geography, Europe = trade, US = security, Middle East = labour market।"),
    notes=("Topic-wise column (S1, S4, S8, S12) PDF-তে ছিল না; PDF option ও slide knowledge থেকে আমার সংযোজন। Body-III (S13–S15) fixed ও generic; CMBEC/Water হলে S13-এ topic-specific challenge (যেমন Myanmar civil war) বসানো যাবে। "
           "Iran war শুধু অর্থনৈতিক প্রভাব হলে FOCUS-GLOBAL-III। 'China না India?' ধরনের প্রশ্নে ARG-ও বিকল্প।"),
    verify=("সব 2026 তথ্য (চীন চুক্তি, Ganges Treaty) এবং US–Iran পরিস্থিতি সময়-সংবেদনশীল। 'as of [month, year]' লিখুন, চুক্তির বিস্তারিত বানাবেন না। S6, S10 report যাচাই করুন।"))