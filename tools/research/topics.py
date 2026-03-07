"""
Master catalog of 150+ survival, engineering, and emergency research topics.

Each entry is a (subcategory, search_query) tuple organized by domain.
Used by the scraper to gather training data for the offline AI model.

This file is original work — safe for Apache 2.0 open-source distribution.
"""

# ─────────────────────────────────────────────────────────────
# CORE SURVIVAL TOPICS
# ─────────────────────────────────────────────────────────────
SURVIVAL_TOPICS: dict[str, list[tuple[str, str]]] = {
    "medical": [
        ("trauma", "emergency trauma surgery procedures shrapnel removal stitching"),
        ("pharmacy", "improvised antibiotics and antiseptics from natural sources"),
        ("anesthesia", "field anesthesia and pain management techniques"),
        ("triage", "mass casualty triage protocols and ethics"),
        ("pediatrics", "emergency childbirth and infant care without hospitals"),
        ("infection", "treating infectious diseases cholera typhoid in grid-down"),
        ("dentistry", "emergency dental extraction and infection control"),
        ("botany", "medicinal plants and their chemical processing"),
        ("hygiene", "preventing outbreaks in high-density survival shelters"),
    ],
    "water_food": [
        ("extraction", "atmospheric water generation and extraction from humidity"),
        ("filtration", "building high-capacity bio-sand and charcoal water filters"),
        ("chemistry", "chemical water purification using household bleach and iodine"),
        ("preservation", "pressure canning and long-term grain storage logic"),
        ("agriculture", "intensive high-yield gardening in small urban spaces"),
        ("foraging", "identifying edible vs toxic mushrooms and plants in the wild"),
        ("nutrition", "therapeutic diets for specific illnesses and malnutrition"),
        ("cooking", "building high-efficiency rocket stoves and solar ovens"),
        ("livestock", "small-scale protein production rabbits and insects"),
    ],
    "energy_comm": [
        ("solar", "wiring salvaged solar panels and charge controllers basics"),
        ("batteries", "lead-acid battery maintenance and reconditioning techniques"),
        ("radio", "HF radio signal propagation and long-range antenna design"),
        ("antennas", "building improvised yagi and wire antennas from scrap"),
        ("shielding", "faraday cage construction for protecting electronics"),
        ("lighting", "creating safe oil lamps and candles from animal fat"),
        ("computing", "offline data storage and mesh networking protocols"),
        ("generators", "converting engines to run on propane or wood gas"),
        ("signals", "low-tech communication smoke mirrors and Morse code"),
    ],
    "mechanical": [
        ("engines", "small engine repair and maintenance using recycled oil"),
        ("blacksmithing", "building a charcoal forge and basic metalworking"),
        ("machining", "manual lathe and drill press operations for parts"),
        ("carpentry", "structural joining and building without power tools"),
        ("welding", "improvised stick welding using car batteries"),
        ("lubricants", "extracting lubricants and grease from organic sources"),
        ("pumps", "designing manual water pumps and irrigation systems"),
        ("automotive", "hot-wiring and bypass electronics for older vehicles"),
        ("materials", "testing scrap metal for strength and brittle failure"),
    ],
    "shelter_defense": [
        ("structure", "reinforcing concrete and brick against blast pressure"),
        ("ventilation", "positive pressure air filtration for bunkers"),
        ("security", "perimeter alarm systems using tripwires and sensors"),
        ("navigation", "topographical map reading and celestial navigation"),
        ("camouflage", "visual and thermal signature management in urban war"),
        ("ballistics", "understanding barrier penetration of various materials"),
        ("entrenchment", "digging safe foxholes and subterranean tunnels"),
        ("psychology", "managing collective trauma and leadership in crises"),
        ("logistics", "supply chain management for isolated communities"),
    ],
    "ignition_survival": [
        ("fire", "friction fire techniques bow drill and flint and steel"),
        ("ignition", "solar ignition using parabolic mirrors and lenses"),
        ("chemistry_fire", "chemical fire starters using potassium permanganate and glycerin"),
        ("insulation", "primitive clothing and shelter insulation for extreme cold"),
    ],
}

# ─────────────────────────────────────────────────────────────
# WAR-SPECIFIC PRIORITY PROTOCOLS (TIER 0)
# ─────────────────────────────────────────────────────────────
WAR_SURVIVAL_PRIORITY: dict[str, list[tuple[str, str]]] = {
    "zero_dark_comms": [
        ("packet_radio", "VHF/UHF packet radio for text messaging without internet"),
        ("mesh_networking", "building off-grid LoRa mesh networks for city-wide alerts"),
        ("signal_flares", "creating chemical signal flares and smoke markers"),
        ("courier_logistics", "establishing secure physical courier routes and dead drops"),
        ("one_time_pads", "manual encryption with paper and pen one-time pads"),
    ],
    "emergency_governance": [
        ("triage_society", "rationing and distribution protocols for food and medical supplies"),
        ("conflict_mediation", "resolving internal community disputes without police or courts"),
        ("security_councils", "organizing community watch and neighborhood defense sectors"),
        ("quarantine", "establishing and maintaining quarantine zones in high-density shelters"),
        ("legal_framework", "simplified common law and restorative justice for triage societies"),
    ],
    "biological_defense": [
        ("sanitation_war", "managing human waste in underground shelters to prevent cholera"),
        ("centrifuge_diy", "building a manual blood/fluid centrifuge from bicycle parts"),
        ("lab_glassware", "repairing and improvising laboratory glassware for chemistry"),
        ("patient_tracking", "manual epidemiological monitoring and outbreak tracking"),
    ],
    "portable_computing": [
        ("raspberry_pi_survival", "configuring low-power linux servers for offline wiki access"),
        ("solar_charging", "ultra-efficient charging of 5V devices from salvaged electronics"),
        ("data_hoarding", "compressing and indexing millions of pages for offline lookup"),
        ("offline_mapping", "loading and using offline GIS/OpenStreetMap data on 8GB devices"),
    ],
}

# ─────────────────────────────────────────────────────────────
# INDUSTRIAL & CIVIL EXPANSION
# ─────────────────────────────────────────────────────────────
EMERGENCY_EXPANSION: dict[str, list[tuple[str, str]]] = {
    "chemistry_industrial": [
        ("fuel", "converting plastic waste into diesel or fuel oil pyrolysis"),
        ("hygiene", "manufacturing soap and lye from wood ash and animal fat"),
        ("acids", "creating sulfuric and nitric acid from raw materials"),
        ("smelting", "extracting iron and copper from ore and scrap metal"),
        ("distillation", "building fractional distillation columns for alcohol and fuel"),
        ("solvents", "making acetone and ethanol for medical and industrial use"),
        ("extraction", "extracting essential oils and plant resins for antiseptic use"),
        ("explosives_safety", "safe handling and creation of industrial blasting agents for mining"),
        ("rubber", "reclaiming and vulcanizing rubber from old tires"),
    ],
    "civil_infrastructure": [
        ("concrete", "mixing improvised concrete and mortar from lime and ash"),
        ("bridges", "structural repair of small bridges and overpasses"),
        ("canals", "manual irrigation and drainage canal engineering"),
        ("roads", "stabilizing soil and building corduroy roads for heavy vehicles"),
        ("sanitation", "large scale sewage treatment without electricity"),
        ("masonry", "building load-bearing brick and stone structures"),
        ("pumps", "designing hydraulic ram pumps for moving water uphill"),
        ("ventilation", "passive cooling and air exchange for massive bunkers"),
    ],
    "logistics_comms": [
        ("encryption", "manual cipher techniques (One-Time Pad) for security"),
        ("cables", "splicing and repairing submarine and terrestrial fiber/copper cables"),
        ("satellites", "tracking and receiving weather satellite data without internet"),
        ("supply_chain", "establishing secure delivery and trade routes in warzones"),
        ("archives", "long-term data storage on stone or physical media"),
        ("frequency", "spectrum management for local emergency broadcasts"),
        ("mesh", "low-power LoRa mesh networking for city-wide messaging"),
    ],
    "social_governance": [
        ("conflict", "de-escalation and mediation protocols for stressed groups"),
        ("law", "establishing community justice and security councils"),
        ("psychology", "treating complex PTSD and trauma in field conditions"),
        ("education", "teaching core science and math without school access"),
        ("leadership", "decision-making frameworks for high-stakes crises"),
        ("logistics", "rationing and equitable resource distribution systems"),
    ],
    "aviation_maritime": [
        ("drones", "DIY drone repair and frequency hopping for surveillance"),
        ("sailing", "basic navigation and repair of small watercraft"),
        ("engines", "troubleshooting large diesel marine and truck engines"),
        ("gliders", "building simple reconnaissance gliders from wood/fabric"),
    ],
}

# ─────────────────────────────────────────────────────────────
# HUMAN LEGACY: SPIRITUAL, EDUCATIONAL & PSYCHOLOGICAL
# ─────────────────────────────────────────────────────────────
HUMAN_LEGACY_EXPANSION: dict[str, list[tuple[str, str]]] = {
    "philosophy_religion": [
        ("theology", "core tenets and scriptures of world major religions for comfort and burial"),
        ("stoicism", "stoic philosophy for maintaining mental fortitude in extreme suffering"),
        ("meditation", "breathwork and mindfulness techniques for reducing acute anxiety and panic"),
        ("rituals", "secular and religious burial and mourning rites for communities"),
        ("morality", "ethics and moral philosophy in scarcity situations for resource sharing"),
        ("purpose", "finding existential meaning and logotherapy during long-term displacement"),
    ],
    "pedagogy_children": [
        ("literacy", "phonics and basic reading instruction for children without school access"),
        ("arithmetic", "teaching elementary mathematics and geometry using physical objects"),
        ("science", "conducting basic physics and biology experiments with household waste"),
        ("play", "therapeutic group games and storytelling for traumatized children"),
        ("apprenticeship", "master-apprentice learning models for teaching survival skills to youth"),
        ("self_defense", "safe situational awareness and safety training for children in conflict areas"),
    ],
    "health_wellness": [
        ("sleep", "optimizing sleep hygiene and safety in high-noise war environments"),
        ("stretching", "yoga and mobility exercises to prevent injury in manual labor"),
        ("herbalism", "cultivating adaptogens and calming herbs like valerian and lavender"),
        ("group_therapy", "facilitating peer-to-peer mental support circles without professional aid"),
        ("grief", "processing sudden loss and bereavement in high-casualty zones"),
    ],
    "curated_knowledge": [
        ("bibliography", "list of 1000 essential physical books for planetary recovery"),
        ("encyclopedia", "how to build a physical wiki or paper filing system for local data"),
        ("preservation", "protecting paper and digital records from humidity and UV decay"),
        ("heritage", "preserving local cultural oral histories and genealogies"),
    ],
}

# ─────────────────────────────────────────────────────────────
# TRANSPORT & HEAVY MACHINERY
# ─────────────────────────────────────────────────────────────
TRANSPORT_HEAVY_EXPANSION: dict[str, list[tuple[str, str]]] = {
    "automotive_repair": [
        ("diesel_basics", "maintenance of heavy duty diesel engines trucks and tractors"),
        ("electronics_bypass", "hotwiring and bypassing ECU/immobilizers on older vehicles"),
        ("clutch_brakes", "manual repair and bleeding of hydraulic brake and clutch systems"),
        ("tires", "vulcanizing rubber and patching tires using heat and raw rubber"),
        ("lubrication", "reclaiming and filtering used engine oil for reuse"),
        ("alternators", "repairing and rewinding copper coils in alternators and starters"),
    ],
    "industrial_machines": [
        ("pumps", "repairing centrifugal and diaphragm water pumps for agriculture"),
        ("generators", "synchronizing multiple small generators for three-phase power"),
        ("lathes", "operating manual lathes and milling machines for spare parts"),
        ("welding", "building a DC arc welder from three 12V car batteries"),
        ("hydraulics", "repairing hydraulic hoses and cylinders for heavy earthmovers"),
        ("hyster", "forklift and material handling equipment repair and bypass"),
    ],
    "rail_maritime": [
        ("locomotives", "basic switching and operation of diesel-electric locomotives"),
        ("marine_outboard", "diagnosing and fixing 2-stroke and 4-stroke outboard boat engines"),
        ("navigation", "using a sextant and nautical charts for open water navigation"),
        ("rigging", "knot-tying and rope-work for high-load industrial and maritime use"),
    ],
    "aviation_maintenance": [
        ("cessna_basics", "basic airframe and engine (Lycoming/Continental) maintenance for small aircraft"),
        ("fuel_avgas", "distilling high-octane fuel for aviation use from ethanol/gasoline blends"),
        ("avionics", "basic radio and transponder repair in older analog cockpits"),
    ],
}

# ─────────────────────────────────────────────────────────────
# MULTILINGUAL SURVIVAL QUERIES
# ─────────────────────────────────────────────────────────────
TRANSLATION_QUERIES: dict[str, list[tuple[str, str]]] = {
    "arabic_survival": [
        ("first_aid_ar", "إسعافات أولية طارئة للحروب والنزاعات"),
        ("water_ar", "استخراج مياه الشرب من الهواء والبيئة المحيطة"),
        ("engineering_ar", "هندسة ميكانيكية لإصلاح محركات الديزل في الطوارئ"),
    ],
    "spanish_survival": [
        ("primeros_auxilios_es", "primeros auxilios de emergencia en zonas de guerra"),
        ("agua_es", "filtración y obtención de agua potable en condiciones extremas"),
        ("mecánica_es", "reparación de motores y mecánica de emergencia"),
    ],
    "french_survival": [
        ("premiers_secours_fr", "premiers secours d'urgence en zone de conflit"),
        ("eau_fr", "extraction et purification de l'eau en situation de survie"),
        ("mecanique_fr", "mécanique de survie et réparation de moteurs"),
    ],
}


# ─────────────────────────────────────────────────────────────
# MERGED MASTER CATALOG
# ─────────────────────────────────────────────────────────────
def get_all_topics() -> dict[str, list[tuple[str, str]]]:
    """Return the complete merged topic catalog."""
    merged = {}
    for source in [
        SURVIVAL_TOPICS,
        WAR_SURVIVAL_PRIORITY,
        EMERGENCY_EXPANSION,
        HUMAN_LEGACY_EXPANSION,
        TRANSPORT_HEAVY_EXPANSION,
        TRANSLATION_QUERIES,
    ]:
        merged.update(source)
    return merged


if __name__ == "__main__":
    all_topics = get_all_topics()
    total = sum(len(v) for v in all_topics.values())
    print(f"Categories: {len(all_topics)}")
    print(f"Total topics: {total}")
    for cat, topics in all_topics.items():
        print(f"  {cat}: {len(topics)} topics")
