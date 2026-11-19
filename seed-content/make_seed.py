"""Generate fictional Contoso seed content for a custom trainable classifier.
Positive: engineering design specifications (proprietary product IP).
Negative: everyday business documents, including some hard negatives
(public user guides, marketing product pages) that mention products but are not specs.
All content is fictional."""
import argparse, os, random
from docx import Document

ap = argparse.ArgumentParser(description="Generate fictional classifier seed content.")
ap.add_argument("--out", default="./seed", help="Output folder")
ap.add_argument("--positive", type=int, default=60, help="Positive samples (50-500)")
ap.add_argument("--negative", type=int, default=160, help="Negative samples (150-1500)")
ap.add_argument("--seed", type=int, default=42, help="Random seed for repeatable output")
args = ap.parse_args()
random.seed(args.seed)
OUT = args.out
for sub in ("positive", "negative"):
    os.makedirs(os.path.join(OUT, sub), exist_ok=True)

PRODUCTS = ["Aurora thermal sensor", "Halcyon micro-pump", "Kestrel drone gimbal", "Meridian battery pack",
            "Obsidian edge gateway", "Lumen optical encoder", "Tidewater flow valve", "Vantage lidar module",
            "Cobalt motor controller", "Sable haptic actuator", "Northwind heat exchanger", "Quill stylus digitiser"]
CODES = ["AUR", "HAL", "KES", "MER", "OBS", "LUM", "TID", "VAN", "COB", "SAB", "NWH", "QUI"]
ENGINEERS = ["R. Byrne", "A. Okafor", "M. Lindqvist", "S. Tanaka", "P. Murphy", "D. Kowalski", "L. Fernandes",
             "C. Walsh", "J. Mbeki", "E. Novak", "H. Doyle", "K. Ahmed"]
MATERIALS = ["6061-T6 aluminium", "PEEK", "316L stainless steel", "glass-filled nylon (PA66-GF30)",
             "titanium grade 5", "polycarbonate", "FR-4 laminate", "copper C110", "silicone (Shore 40A)"]

def spec_doc(i):
    p = random.randrange(len(PRODUCTS)); prod, code = PRODUCTS[p], CODES[p]
    rev = random.choice("ABCDEFG"); num = f"{code}-DS-{random.randint(100,999)}"
    d = Document()
    title = random.choice(["Engineering Design Specification", "Detailed Design Specification",
                           "Mechanical Design Specification", "Electrical Design Specification",
                           "Firmware Architecture Specification", "Product Design Requirements Specification"])
    d.add_heading(f"{title} - {prod}", 0)
    d.add_paragraph(f"Document number: {num}  Revision: {rev}  Owner: {random.choice(ENGINEERS)}")
    d.add_paragraph(random.choice([
        "CONTOSO CONFIDENTIAL - PROPRIETARY. This document contains Contoso trade secrets and must not be shared outside the engineering programme.",
        "Contoso Ltd - Restricted engineering information. Disclosure to third parties requires an executed NDA and approval from the programme lead.",
        "Proprietary and confidential. Contains Contoso intellectual property subject to patent filing. Do not distribute."]))
    d.add_heading("1. Scope", 1)
    d.add_paragraph(f"This specification defines the {random.choice(['mechanical','electrical','thermal','firmware','system'])} design of the {prod} "
                    f"for the {random.choice(['Gen 2','Gen 3','2027','next-generation','industrial'])} product line. It supersedes revision "
                    f"{chr(ord(rev)-1) if rev!='A' else 'draft'} and incorporates findings from design review DR-{random.randint(10,99)}.")
    d.add_heading("2. Design requirements", 1)
    reqs = [f"Operating temperature range of -{random.randint(20,40)} C to +{random.randint(60,125)} C.",
            f"Mean time between failures of at least {random.randint(20,90)},000 hours.",
            f"Ingress protection rating IP{random.choice([54,65,67,68])}.",
            f"Supply voltage {random.choice([3.3,5,12,24,48])} V +/- {random.randint(2,10)}%.",
            f"Peak current draw not to exceed {random.randint(150,2400)} mA.",
            f"Mass budget of {random.randint(12,900)} g including fasteners.",
            f"Resolution of {random.choice([0.01,0.05,0.1,0.5])} units across the full measurement range.",
            f"Response latency below {random.randint(2,40)} ms at the 99th percentile.",
            f"Vibration tolerance per IEC 60068-2-6, {random.randint(5,20)} g sine sweep."]
    for r in random.sample(reqs, random.randint(4, 7)):
        d.add_paragraph(f"REQ-{random.randint(100,999)}: {r}", style="List Bullet")
    d.add_heading("3. Detailed design", 1)
    d.add_paragraph(random.choice([
        f"The housing is machined from {random.choice(MATERIALS)} with a nominal wall thickness of {random.uniform(0.8,4):.2f} mm and a flatness tolerance of {random.uniform(0.01,0.1):.3f} mm.",
        f"The proprietary {random.choice(['dual-loop PID','adaptive Kalman','phase-shifted PWM','field-oriented control'])} algorithm runs at {random.choice([1,2,8,20,40])} kHz on the {random.choice(['STM32H7','nRF5340','RP2040','i.MX RT1170'])} and is the core differentiator for this product.",
        f"Heat is dissipated through a {random.choice(MATERIALS)} spreader bonded with thermal interface material rated at {random.uniform(1.5,8):.1f} W/mK."]))
    d.add_paragraph(random.choice([
        f"Critical dimensions: bore diameter {random.uniform(4,40):.3f} mm H7, shaft {random.uniform(4,40):.3f} mm g6, seal groove depth {random.uniform(0.5,3):.2f} mm.",
        f"Bill of materials target cost is EUR {random.uniform(4,180):.2f} per unit at {random.choice([10,50,100])}k annual volume.",
        f"The novel {random.choice(['impeller geometry','optical slit pattern','coil winding layout','sealing interface'])} described in this section is the subject of patent application CTS-PA-{random.randint(1000,9999)}."]))
    d.add_heading("4. Verification and test", 1)
    d.add_paragraph(f"Design verification testing (DVT) comprises {random.randint(6,30)} test cases including thermal cycling ({random.randint(100,1000)} cycles), "
                    f"drop testing from {random.choice([0.8,1.2,1.5])} m and EMC pre-compliance to EN 55032 Class {random.choice('AB')}.")
    if random.random() < 0.6:
        d.add_heading("5. Open issues", 1)
        d.add_paragraph(random.choice(["Supplier qualification for the second-source component is outstanding.",
                                       "Tolerance stack-up on the lid interface exceeds budget by 0.04 mm and is under review.",
                                       "Firmware watchdog timing needs validation at low temperature."]))
    d.add_paragraph(f"Approved by: {random.choice(ENGINEERS)}, Chief Engineer. Next review: design freeze gate {random.choice(['G3','G4','G5'])}.")
    return d, f"{num}_{prod.split()[0]}_Design_Spec_Rev{rev}.docx"

NEG_KINDS = {}
def neg(kind):
    def w(f): NEG_KINDS[kind] = f; return f
    return w

@neg("meeting")
def _(d):
    d.add_heading(f"{random.choice(['Weekly team','Monthly operations','Sales pipeline','Leadership','Facilities'])} meeting notes", 0)
    d.add_paragraph(f"Attendees: {', '.join(random.sample(ENGINEERS,4))}")
    for _ in range(random.randint(3,6)):
        d.add_paragraph(random.choice(["Reviewed actions from the last meeting - most are complete.",
            "Agreed to move the quarterly review to the second week of the month.",
            "Budget for the team offsite was approved.", "Recruitment for two open roles is progressing.",
            "Customer satisfaction scores improved slightly this quarter.", "Office move timeline confirmed for spring.",
            "Reminder to complete mandatory training by month end.", "Discussed holiday cover for December."]), style="List Bullet")

@neg("policy")
def _(d):
    t = random.choice(["Travel and expenses policy","Remote working policy","Annual leave policy","Acceptable use policy",
                       "Health and safety guidance","Company car policy","Parental leave policy","Code of conduct summary"])
    d.add_heading(t, 0)
    for _ in range(random.randint(4,7)):
        d.add_paragraph(random.choice(["Employees should submit claims within 30 days with receipts attached.",
            "Managers approve requests in the HR system before the date of absence.",
            "Use only approved booking channels for flights and hotels.",
            "Report any incident or near miss to your line manager the same day.",
            "Company equipment must be returned when you leave Contoso.",
            "This policy is reviewed annually by the People team.",
            "Questions can be raised with your HR business partner.",
            "Working hours should be agreed with your manager and recorded."]))

@neg("newsletter")
def _(d):
    d.add_heading(f"Contoso staff newsletter - {random.choice(['January','March','May','July','September','November'])} edition", 0)
    for _ in range(random.randint(3,5)):
        d.add_paragraph(random.choice(["Congratulations to the Dublin office on winning the charity step challenge!",
            "Our new canteen menu launches next week with more vegetarian options.",
            "Welcome to the twelve new starters who joined this month.",
            "The annual summer party will be held at the usual venue - save the date.",
            "Thank you to everyone who volunteered at the community clean-up.",
            "Reminder: the car park will be resurfaced over the bank holiday weekend.",
            "Meet the team: this month we profile the customer support crew."]))

@neg("userguide")  # hard negative: public product docs
def _(d):
    p = random.choice(PRODUCTS)
    d.add_heading(f"{p} - Quick start guide", 0)
    for s in random.sample(["Unpack the device and check all items are present.","Charge the unit fully before first use.",
            "Download the Contoso companion app from your app store.","Press and hold the power button for three seconds.",
            "Pair the device by following the on-screen instructions.","Clean the surface with a soft dry cloth only.",
            "For warranty support visit the Contoso support website.","Do not expose the product to open flame."], 5):
        d.add_paragraph(s, style="List Number")

@neg("marketing")  # hard negative: public product page copy
def _(d):
    p = random.choice(PRODUCTS)
    d.add_heading(f"Introducing the {p}", 0)
    d.add_paragraph(random.choice(["Smarter, smaller and more reliable than ever.","Built for professionals who demand the best.",
                                   "The new standard in its class."]))
    d.add_paragraph(f"Available from {random.choice(['spring','summer','autumn'])} through Contoso partners. Contact sales for volume pricing.")
    d.add_paragraph("Follow us on social media for launch news and customer stories.")

@neg("it")
def _(d):
    d.add_heading(random.choice(["How to reset your password","Connecting to the guest Wi-Fi","Setting up MFA on your phone",
                                 "Booking a meeting room","Printing from your laptop","Requesting new software"]), 0)
    for s in random.sample(["Open the company portal from the Start menu.","Sign in with your work account.",
                            "Select the option that matches your request.","Follow the prompts to complete setup.",
                            "If you have problems, raise a ticket with the service desk.","Restart your device if changes do not apply."], 4):
        d.add_paragraph(s, style="List Number")

@neg("sales")
def _(d):
    d.add_heading(f"Q{random.randint(1,4)} sales summary - {random.choice(['EMEA','UK and Ireland','DACH','Nordics','Benelux'])}", 0)
    d.add_paragraph(f"Revenue was {random.randint(85,120)}% of target. {random.randint(4,30)} new accounts were opened.")
    d.add_paragraph(random.choice(["Pipeline coverage remains healthy for next quarter.","Two large renewals slipped into next month.",
                                   "Partner channel performance exceeded expectations."]))

@neg("event")
def _(d):
    d.add_heading(random.choice(["Invitation: customer appreciation evening","Agenda: partner summit","Lunch and learn: wellbeing",
                                 "Town hall agenda","Graduate open day programme"]), 0)
    for t in ["09:30 Arrival and coffee","10:00 Welcome","11:00 Breakout sessions","12:30 Lunch","14:00 Close"][:random.randint(3,5)]:
        d.add_paragraph(t)

@neg("customer")
def _(d):
    d.add_heading("Customer service call script", 0)
    for s in ["Thank you for calling Contoso, how can I help today?","Can I take your order number please?",
              "I am sorry to hear that - let me look into it for you.","Is there anything else I can help you with?"]:
        d.add_paragraph(s)

@neg("facilities")
def _(d):
    d.add_heading(random.choice(["Fire evacuation procedure","Office cleaning schedule","Visitor sign-in process","Parking allocation"]), 0)
    for _ in range(4):
        d.add_paragraph(random.choice(["Assemble at the designated point in the car park.","Visitors must wear a badge at all times.",
            "Cleaning takes place each evening after 18:00.","Spaces are allocated on a first come basis.",
            "Fire wardens will check each floor.","Report faults to the facilities helpdesk."]))

def neg_doc(i):
    kind = random.choice(list(NEG_KINDS))
    d = Document(); NEG_KINDS[kind](d)
    return d, f"{kind}_{i:03d}.docx"

for i in range(args.positive):
    d, n = spec_doc(i); d.save(os.path.join(OUT, "positive", n))
for i in range(args.negative):
    d, n = neg_doc(i); d.save(os.path.join(OUT, "negative", n))
print("done")
