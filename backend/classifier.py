"""
Rules-based document classifier for real estate transaction files.
Uses filename patterns (high weight) + content keyword scoring.
"""

DOC_TYPES: dict[str, dict] = {
    "Purchase_Agreement": {
        "display": "Purchase Agreement",
        "keywords": [
            "california residential purchase agreement",
            "residential purchase agreement",
            "purchase agreement",
            "purchase contract",
            "real estate purchase",
            "offer to purchase",
            "agreement to purchase",
        ],
        "filename_patterns": ["purchase", "contract", "rpa", "crpa"],
        "folder": "01_Contract",
        "required": True,
        "priority": 10,
    },
    "Addendum": {
        "display": "Addendum",
        "keywords": ["addendum", "amendment to", "modification to contract", "addendum no."],
        "filename_patterns": ["addend", "amend"],
        "folder": "01_Contract",
        "required": False,
        "priority": 5,
    },
    "Counter_Offer": {
        "display": "Counter Offer",
        "keywords": [
            "counter offer",
            "counter-offer",
            "counteroffer",
            "buyer's counter offer",
            "seller's counter offer",
        ],
        "filename_patterns": ["counter", "bco", "sco"],
        "folder": "01_Contract",
        "required": False,
        "priority": 8,
    },
    "Transfer_Disclosure": {
        "display": "Transfer Disclosure Statement (TDS)",
        "keywords": [
            "transfer disclosure statement",
            "real estate transfer disclosure",
            "seller's disclosures",
        ],
        "filename_patterns": ["tds", "transfer disc", "transfer_disc"],
        "folder": "02_Disclosures",
        "required": True,
        "priority": 10,
    },
    "Seller_Property_Questionnaire": {
        "display": "Seller Property Questionnaire (SPQ)",
        "keywords": ["seller property questionnaire", "property questionnaire"],
        "filename_patterns": ["spq", "seller property"],
        "folder": "02_Disclosures",
        "required": False,
        "priority": 9,
    },
    "Agency_Disclosure": {
        "display": "Agency Disclosure",
        "keywords": [
            "disclosure regarding real estate agency",
            "agency disclosure",
            "agency relationship",
            "agency confirmation",
            "real estate agency relationships",
        ],
        "filename_patterns": ["agency", "avid"],
        "folder": "02_Disclosures",
        "required": True,
        "priority": 9,
    },
    "Natural_Hazard_Disclosure": {
        "display": "Natural Hazard Disclosure (NHD)",
        "keywords": [
            "natural hazard disclosure",
            "natural hazard zone",
            "seismic hazard",
            "flood zone disclosure",
            "natural hazard report",
            "nhd report",
        ],
        "filename_patterns": ["nhd", "natural hazard", "hazard disc"],
        "folder": "02_Disclosures",
        "required": True,
        "priority": 9,
    },
    "Lead_Paint_Disclosure": {
        "display": "Lead Paint Disclosure",
        "keywords": [
            "lead-based paint",
            "lead paint disclosure",
            "lead warning statement",
            "pre-1978",
        ],
        "filename_patterns": ["lead", "lead_paint", "leadpaint"],
        "folder": "02_Disclosures",
        "required": False,
        "priority": 9,
    },
    "Statewide_Buyer_Seller_Advisory": {
        "display": "Statewide Buyer/Seller Advisory (SBSA)",
        "keywords": [
            "statewide buyer",
            "statewide seller",
            "buyer and seller advisory",
            "sbsa",
        ],
        "filename_patterns": ["sbsa", "buyer seller advisory"],
        "folder": "02_Disclosures",
        "required": False,
        "priority": 7,
    },
    "Inspection_Report": {
        "display": "Inspection Report",
        "keywords": [
            "inspection report",
            "home inspection",
            "property inspection",
            "general inspection",
            "whole house inspection",
            "inspector's report",
        ],
        "filename_patterns": ["inspection", "home_insp", "insp_report"],
        "folder": "03_Inspections",
        "required": False,
        "priority": 8,
    },
    "Pest_Inspection": {
        "display": "Pest / Termite Report",
        "keywords": [
            "termite",
            "pest inspection",
            "wood destroying",
            "wood destroying pest",
            "fumigation report",
            "structural pest",
        ],
        "filename_patterns": ["termite", "pest", "wdo"],
        "folder": "03_Inspections",
        "required": False,
        "priority": 9,
    },
    "Appraisal": {
        "display": "Appraisal Report",
        "keywords": [
            "appraisal report",
            "uniform residential appraisal",
            "urar",
            "appraised value",
            "market value opinion",
            "appraiser certification",
        ],
        "filename_patterns": ["appraisal", "apprai", "urar"],
        "folder": "04_Financing",
        "required": False,
        "priority": 9,
    },
    "Loan_Approval": {
        "display": "Loan Approval / Commitment",
        "keywords": [
            "loan commitment",
            "mortgage commitment",
            "loan approval",
            "conditional approval",
            "final approval",
            "clear to close",
            "underwriting approval",
        ],
        "filename_patterns": ["loan_approval", "loanapproval", "commitment", "approval_letter"],
        "folder": "04_Financing",
        "required": False,
        "priority": 8,
    },
    "Loan_Estimate": {
        "display": "Loan Estimate",
        "keywords": ["loan estimate", "good faith estimate", "gfe"],
        "filename_patterns": ["loan_est", "loan estimate", "gfe"],
        "folder": "04_Financing",
        "required": False,
        "priority": 7,
    },
    "Preliminary_Title_Report": {
        "display": "Preliminary Title Report",
        "keywords": [
            "preliminary report",
            "preliminary title",
            "title report",
            "title commitment",
            "schedule a",
            "schedule b",
            "title insurance",
        ],
        "filename_patterns": ["title", "prelim", "ptr", "preliminary"],
        "folder": "05_Title_Escrow",
        "required": True,
        "priority": 9,
    },
    "Escrow_Instructions": {
        "display": "Escrow Instructions",
        "keywords": [
            "escrow instructions",
            "escrow agreement",
            "joint escrow instructions",
            "escrow number",
            "escrow officer",
        ],
        "filename_patterns": ["escrow", "escrow_inst"],
        "folder": "05_Title_Escrow",
        "required": True,
        "priority": 9,
    },
    "Closing_Disclosure": {
        "display": "Closing Disclosure",
        "keywords": [
            "closing disclosure",
            "hud-1",
            "settlement statement",
            "alta settlement",
            "closing statement",
        ],
        "filename_patterns": ["closing_disc", "hud1", "hud-1", "settlement", "alta"],
        "folder": "05_Title_Escrow",
        "required": False,
        "priority": 8,
    },
    "Wire_Instructions": {
        "display": "Wire Transfer Instructions",
        "keywords": [
            "wire transfer instructions",
            "wiring instructions",
            "bank wire",
            "aba routing",
            "wire funds",
        ],
        "filename_patterns": ["wire", "wiring"],
        "folder": "05_Title_Escrow",
        "required": False,
        "priority": 8,
    },
    "HOA_Documents": {
        "display": "HOA Documents",
        "keywords": [
            "homeowners association",
            "homeowner association",
            "cc&r",
            "covenants conditions",
            "condominium documents",
            "condo docs",
            "association bylaws",
        ],
        "filename_patterns": ["hoa", "cc&r", "ccr", "condo", "bylaws"],
        "folder": "06_HOA",
        "required": False,
        "priority": 8,
    },
    "Listing_Agreement": {
        "display": "Listing Agreement",
        "keywords": [
            "listing agreement",
            "exclusive authorization",
            "exclusive right to sell",
            "listing contract",
        ],
        "filename_patterns": ["listing", "listing_agmt"],
        "folder": "07_Misc",
        "required": False,
        "priority": 8,
    },
    "Buyer_Representation": {
        "display": "Buyer Representation Agreement",
        "keywords": [
            "buyer representation",
            "buyer agency agreement",
            "exclusive buyer",
            "buyer broker agreement",
        ],
        "filename_patterns": ["buyer_rep", "buyer rep", "bra"],
        "folder": "07_Misc",
        "required": False,
        "priority": 7,
    },
    "Unknown": {
        "display": "Unknown Document",
        "keywords": [],
        "filename_patterns": [],
        "folder": "07_Misc",
        "required": False,
        "priority": 0,
    },
}

REQUIRED_DOCS = [key for key, v in DOC_TYPES.items() if v.get("required")]


def classify_document(filename: str, text: str) -> str:
    """Return the best-matching doc type key, or 'Unknown'."""
    filename_lower = filename.lower()
    text_scan = text.lower()[:2000]

    scores: dict[str, float] = {}

    for doc_type, config in DOC_TYPES.items():
        if doc_type == "Unknown":
            continue

        score = 0.0
        priority = config["priority"]

        # Filename pattern match (strong signal)
        for pattern in config["filename_patterns"]:
            if pattern.lower() in filename_lower:
                score += 20 * priority
                break

        # Keyword match in first 2000 chars
        for keyword in config["keywords"]:
            kw = keyword.lower()
            if kw in text_scan:
                # Bonus if keyword appears in first 300 chars (document header)
                weight = 8 if kw in text_scan[:300] else 4
                score += weight * priority

        if score > 0:
            scores[doc_type] = score

    if not scores:
        return "Unknown"

    return max(scores, key=lambda k: scores[k])


def get_missing_docs(found_types: list[str]) -> list[dict]:
    """Return required doc types not present in found_types."""
    found_set = set(found_types)
    return [
        {"key": key, "display": DOC_TYPES[key]["display"]}
        for key in REQUIRED_DOCS
        if key not in found_set
    ]


def get_folder(doc_type: str) -> str:
    return DOC_TYPES.get(doc_type, DOC_TYPES["Unknown"])["folder"]


def get_display_name(doc_type: str) -> str:
    return DOC_TYPES.get(doc_type, DOC_TYPES["Unknown"])["display"]
