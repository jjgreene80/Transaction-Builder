"""
Generate sample real estate transaction documents as PDFs for testing TC Doc Tool.
Run from the tc-doc-tool directory: python make_samples.py
"""

import fitz
import os

OUT = os.path.join(os.path.dirname(__file__), "sample_docs")
os.makedirs(OUT, exist_ok=True)


def make_pdf(filename: str, pages: list[str]) -> None:
    doc = fitz.open()
    for content in pages:
        page = doc.new_page(width=612, height=792)  # Letter
        page.insert_text((72, 72), content, fontsize=11, fontname="helv")
    doc.save(os.path.join(OUT, filename))
    doc.close()
    print(f"  created: {filename}")


PROPERTY = "1234 Maple Street, Sacramento, CA 95814"
BUYER    = "John & Sarah Buyer"
SELLER   = "Robert & Linda Seller"
PRICE    = "$485,000"
CLOSE    = "July 15, 2026"
ESCROW_NO = "ESC-2026-00412"

# ── Required documents ──────────────────────────────────────────────────────

make_pdf("purchase_agreement.pdf", [
    f"""CALIFORNIA RESIDENTIAL PURCHASE AGREEMENT
AND JOINT ESCROW INSTRUCTIONS

Property Address: {PROPERTY}
Buyer: {BUYER}
Seller: {SELLER}
Purchase Price: {PRICE}
Close of Escrow: {CLOSE}
Escrow Number: {ESCROW_NO}

1. OFFER: Buyer offers to purchase the above property at the stated price
   subject to the terms and conditions set forth in this agreement.

2. FINANCE TERMS: Buyer to obtain a conventional loan of $388,000 at a
   fixed rate not to exceed 7.25% for 30 years. Down payment: $97,000.

3. CONTINGENCIES:
   (a) Loan contingency: 21 days from acceptance.
   (b) Appraisal contingency: 17 days from acceptance.
   (c) Inspection contingency: 17 days from acceptance.

4. CLOSING COSTS: Each party to pay their customary costs.

5. POSSESSION: At close of escrow.

6. PERSONAL PROPERTY included: All attached fixtures, built-in appliances,
   window coverings, garage door openers.

Buyer Signature: ________________________  Date: __________
Seller Signature: ________________________  Date: __________

Page 1 of 8""",
])

make_pdf("transfer_disclosure_statement.pdf", [
    f"""REAL ESTATE TRANSFER DISCLOSURE STATEMENT (TDS)
(California Civil Code §1102)

Property Address: {PROPERTY}
Seller: {SELLER}
Date: June 4, 2026

THIS STATEMENT IS A DISCLOSURE OF THE CONDITION OF THE ABOVE DESCRIBED
PROPERTY IN COMPLIANCE WITH SECTION 1102 OF THE CIVIL CODE AS OF THE
DATE SIGNED BY THE SELLER.

SECTION I — SELLER'S INFORMATION

Are you (Seller) aware of any significant defects/malfunctions in any of
the following? (Check applicable items)

[ ] Interior walls    [ ] Ceilings    [X] Roof (repaired 2023)
[ ] Windows          [ ] Doors       [ ] Foundation
[ ] Plumbing         [ ] Electrical  [ ] HVAC

Water Heater: Gas, installed 2019, operational.
Heating: Central forced air, last serviced Jan 2026.
Cooling: Central A/C, last serviced Jan 2026.

SECTION II — SELLER CERTIFIES

Seller certifies the information above is true and correct to the best
of Seller's knowledge as of the date signed.

Seller Signature: _______________________  Date: __________

Page 1 of 3""",
])

make_pdf("agency_disclosure.pdf", [
    f"""DISCLOSURE REGARDING REAL ESTATE AGENCY RELATIONSHIPS
(California Civil Code §2079.14)

Property: {PROPERTY}
Date: June 4, 2026

SELLER'S AGENT
A Seller's agent under a listing agreement acts as the agent for the
Seller only. A Seller's agent is not the Buyer's agent, even if by
agreement the agent may receive compensation for services rendered,
either in full or in part from the Buyer.

BUYER'S AGENT
A selling agent can, with a Buyer's consent, agree to act as agent for
the Buyer only. In these situations, the agent will not be the Seller's
agent even if by agreement the agent may receive compensation for services
rendered, either in full or in part from the Seller.

DUAL AGENT
A real estate agent acting as a dual agent represents both the Buyer and
the Seller in the same transaction. This requires the informed consent
of both parties.

AGENCY CONFIRMATION
The listing agent is acting as agent for the SELLER.
The selling agent is acting as agent for the BUYER.

Seller Acknowledgment: ___________________  Date: __________
Buyer Acknowledgment: ___________________  Date: __________""",
])

make_pdf("natural_hazard_disclosure.pdf", [
    f"""NATURAL HAZARD DISCLOSURE STATEMENT (NHD)
TDS Disclosure Report

Property Address: {PROPERTY}
Buyer: {BUYER}
Seller: {SELLER}
Date of Report: June 4, 2026
Report Number: NHD-2026-58821

NATURAL HAZARD ZONE DISCLOSURES

1. SPECIAL FLOOD HAZARD AREA (SFHA)
   This property IS NOT in a Special Flood Hazard Area.

2. AREA OF POTENTIAL FLOODING
   This property IS NOT in an Area of Potential Flooding.

3. HIGH FIRE HAZARD SEVERITY ZONE
   This property IS NOT in a High or Very High Fire Hazard Severity Zone.

4. WILDLAND AREA THAT MAY CONTAIN SUBSTANTIAL FOREST FIRE RISK
   This property IS NOT in a Wildland Fire Area.

5. EARTHQUAKE FAULT ZONE
   This property IS NOT in an Earthquake Fault Zone per Alquist-Priolo Act.

6. SEISMIC HAZARD ZONE
   This property IS in a Seismic Hazard Zone (Liquefaction potential).

This report was prepared by SafeDisclose, Inc. per California Gov. Code §8589.3.

Buyer Signature: _______________________  Date: __________
Seller Signature: _______________________  Date: __________""",
])

make_pdf("preliminary_title_report.pdf", [
    f"""PRELIMINARY REPORT
Issued by: California Title Company
Order Number: CTC-2026-78441
Date of Report: June 4, 2026

Property Address: {PROPERTY}
APN: 123-456-789-00

In response to the above referenced application for a policy of title insurance,
California Title Company hereby reports that it is prepared to issue a policy
of title insurance in the form and amount shown on Schedule A.

SCHEDULE A
Amount of Insurance: {PRICE}
Proposed Insured: {BUYER}
Vesting: Joint Tenants
Estate or Interest: Fee Simple

SCHEDULE B — EXCEPTIONS
The policy or policies to be issued will contain exceptions to the following:

1. Property taxes for the fiscal year 2026-2027, not yet due or payable.
2. Supplemental taxes, if any.
3. CC&Rs recorded January 12, 2001 as Document No. 2001-0045231.
4. Easement for public utilities along the westerly 10 feet of the property.
5. Any unrecorded matters which would be disclosed by an accurate survey
   or inspection of the property.

Title Officer: Michael Chen
Direct: (916) 555-0192

Page 1 of 4""",
])

make_pdf("escrow_instructions.pdf", [
    f"""JOINT ESCROW INSTRUCTIONS
Escrow Number: {ESCROW_NO}
Escrow Officer: Patricia Mills
Escrow Company: Valley Escrow Services, Inc.
Date Opened: June 4, 2026

Property: {PROPERTY}
Buyer: {BUYER}
Seller: {SELLER}
Purchase Price: {PRICE}
Close of Escrow: {CLOSE}

BUYER'S INSTRUCTIONS

Buyer deposits the sum of $9,700 as earnest money deposit.
Buyer will deposit the balance of funds required to close on or before
{CLOSE}.

Buyer instructs escrow to:
1. Record Grant Deed conveying title to Buyer.
2. Obtain a CLTA/ALTA homeowner's policy of title insurance.
3. Prorate property taxes, HOA dues, and rents as of close of escrow.
4. Pay off existing loan of Seller per beneficiary demand.

SELLER'S INSTRUCTIONS

Seller instructs escrow to:
1. Execute and deliver Grant Deed to Buyer upon close.
2. Pay Seller's closing costs and commission per listing agreement.
3. Deliver net proceeds to Seller within 24 hours of close.

Buyer Signature: _______________________  Date: __________
Seller Signature: _______________________  Date: __________

Page 1 of 3""",
])

# ── Common optional documents ────────────────────────────────────────────────

make_pdf("addendum_1.pdf", [
    f"""ADDENDUM TO PURCHASE AGREEMENT

Addendum No. 1
Date: June 5, 2026
Property: {PROPERTY}
Original Purchase Agreement Date: June 4, 2026

This Addendum modifies the Purchase Agreement as follows:

1. CLOSE OF ESCROW: The close of escrow date is extended from July 10, 2026
   to July 15, 2026 to allow additional time for loan processing.

2. SELLER CREDITS: Seller agrees to provide a buyer credit of $5,000 toward
   Buyer's closing costs, as detailed in the purchase agreement.

3. REPAIRS: Seller agrees to repair the roof flashing on the north side of
   the property prior to close of escrow. Seller to provide receipts.

All other terms and conditions of the original Purchase Agreement remain
in full force and effect.

Buyer Signature: _______________________  Date: __________
Seller Signature: _______________________  Date: __________""",
])

make_pdf("home_inspection_report.pdf", [
    f"""HOME INSPECTION REPORT

Inspector: David Torres, Certified Home Inspector #CHI-4421
Company: ProInspect Services
Inspection Date: June 7, 2026
Property Address: {PROPERTY}
Client: {BUYER}

SUMMARY OF FINDINGS

ROOF
Condition: Fair. Composition shingles, approximately 8 years old.
Estimated remaining life: 10-12 years. Flashing at chimney shows
minor gaps — recommend sealing.

FOUNDATION
Condition: Good. Concrete perimeter foundation. No significant cracks
or signs of movement observed.

ELECTRICAL
Condition: Good. 200-amp service panel updated 2018. GFCI protection
present in kitchen and bathrooms.

PLUMBING
Condition: Good. Copper supply lines. ABS drain lines. Water heater
is gas, installed 2019.

HVAC
Condition: Good. Central forced air furnace and A/C, both serviced
January 2026. Filters clean.

RECOMMENDED REPAIRS
1. Seal chimney flashing (Minor — estimated $150-300)
2. Repair loose gutter at northeast corner (Minor — estimated $75-150)
3. Replace missing GFCI outlet cover in garage (Minor — under $25)

This report is for the exclusive use of the client named above.

Page 1 of 12""",
])

make_pdf("seller_property_questionnaire.pdf", [
    f"""SELLER PROPERTY QUESTIONNAIRE (SPQ)
(C.A.R. Form SPQ)

Property Address: {PROPERTY}
Seller: {SELLER}
Date: June 4, 2026

A. GENERAL INFORMATION
1. How long have you owned the property? 11 years
2. How long have you occupied the property? 11 years
3. Are there any pending or threatened legal actions affecting
   the property? NO

B. INSURANCE
1. Has the property ever had an insurance claim filed?
   YES — Roof damage claim 2022, repaired and closed.

C. PROPERTY USE
1. Has the property been used for any business purpose? NO
2. Has the property been used for the manufacture of drugs? NO

D. ENVIRONMENTAL
1. Are you aware of any hazardous materials on the property? NO
2. Any underground storage tanks? NO
3. Any asbestos, lead paint, or urea-formaldehyde? NO (built 1998)

E. STRUCTURAL
1. Any room additions, structural modifications, or alterations
   made without permits? NO
2. Any settling, slippage, or movement of the property? NO

Seller Signature: _______________________  Date: __________""",
])

print(f"\nDone — {len(os.listdir(OUT))} sample documents created in: {OUT}")
print("Upload the files from that folder to test TC Doc Tool.")
