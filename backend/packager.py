"""
Build the output ZIP: organized folder structure + missing-docs checklist.
"""

import os
import zipfile
from datetime import date


FOLDER_ORDER = [
    "01_Contract",
    "02_Disclosures",
    "03_Inspections",
    "04_Financing",
    "05_Title_Escrow",
    "06_HOA",
    "07_Misc",
]


def build_zip(output_dir: str, zip_path: str, missing_docs: list) -> None:
    """
    Walk output_dir (which already has organized sub-folders) and write a ZIP.
    Appends a MISSING_DOCS_CHECKLIST.txt at the root of the ZIP.
    """
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for folder_name in FOLDER_ORDER:
            folder_path = os.path.join(output_dir, folder_name)
            if not os.path.isdir(folder_path):
                continue
            files = sorted(os.listdir(folder_path))
            # Add sequence prefix to filenames inside ZIP
            for seq, filename in enumerate(files, start=1):
                file_path = os.path.join(folder_path, filename)
                stem, ext = os.path.splitext(filename)
                arc_name = f"{folder_name}/{seq:02d}_{stem}{ext}"
                zf.write(file_path, arc_name)

        # Write checklist
        checklist_text = _build_checklist(missing_docs)
        zf.writestr("MISSING_DOCS_CHECKLIST.txt", checklist_text)


def _build_checklist(missing_docs: list) -> str:
    today = date.today().strftime("%B %d, %Y")
    lines = [
        "=" * 60,
        "  TRANSACTION FILE — MISSING DOCUMENTS CHECKLIST",
        f"  Generated: {today}",
        "=" * 60,
        "",
    ]

    if not missing_docs:
        lines += [
            "  All required documents appear to be present.",
            "",
            "  Required documents checklist:",
            "  [✓] Purchase Agreement",
            "  [✓] Transfer Disclosure Statement (TDS)",
            "  [✓] Agency Disclosure",
            "  [✓] Natural Hazard Disclosure (NHD)",
            "  [✓] Preliminary Title Report",
            "  [✓] Escrow Instructions",
        ]
    else:
        lines += [
            f"  {len(missing_docs)} required document(s) NOT FOUND:",
            "",
        ]
        for doc in missing_docs:
            lines.append(f"  [✗] {doc.display}")
        lines += [
            "",
            "  Action required: obtain and upload missing documents",
            "  before submitting to broker for review.",
        ]

    lines += [
        "",
        "=" * 60,
        "  Folder structure in this ZIP:",
        "  01_Contract       — Purchase Agreement, Addenda, Counter Offers",
        "  02_Disclosures    — TDS, Agency, NHD, Lead Paint, SPQ, SBSA",
        "  03_Inspections    — Home Inspection, Pest/Termite Reports",
        "  04_Financing      — Appraisal, Loan Approval, Loan Estimate",
        "  05_Title_Escrow   — Preliminary Title, Escrow, Closing Disclosure",
        "  06_HOA            — CC&Rs, Bylaws, HOA Docs",
        "  07_Misc           — Unclassified documents",
        "=" * 60,
    ]

    return "\n".join(lines)
