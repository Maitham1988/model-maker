#!/usr/bin/env python3
"""
Automated Medical Accuracy Test Suite for Model Maker
=====================================================
Sends emergency medical questions in multiple languages,
collects responses, and auto-grades them against verified
medical knowledge rules.

Usage:
    python tools/test_medical_accuracy.py [--server http://127.0.0.1:8000]
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────────
# TEST QUESTIONS — Each has: question, language, topic, and verification rules
# Rules are keyword-based checks:
#   "must_contain"   → response MUST contain at least one of these words
#   "must_not_contain" → response must NOT contain any of these words (dangerous errors)
#   "description"    → what the check verifies (for the report)
# ──────────────────────────────────────────────────────────────────────────────

TEST_CASES = [
    # ═══════════════════════════════════════════════════════════
    # BURNS (Arabic)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "BURN-AR-01",
        "question": "يدي احترقت شنو اسوي؟",
        "lang": "Arabic",
        "topic": "Burns",
        "checks": [
            {
                "must_contain": ["بارد", "باردة", "بارده", "cool", "cold"],
                "must_not_contain": ["دافئ", "دافئة", "ساخن", "ساخنة", "حار", "warm", "hot water"],
                "description": "Must say COOL water, never warm/hot",
            },
            {
                "must_not_contain": [
                    "خيار",
                    "طماطم",
                    "بطاطس",
                    "بصل",
                    "cucumber",
                    "tomato",
                    "potato",
                    "onion",
                ],
                "description": "Must NOT recommend fruits/vegetables on burns",
            },
            {
                "must_not_contain": [
                    "استشر طبيب",
                    "استشيري طبيب",
                    "مراجعة طبيب",
                    "زيارة طبيب",
                    "consult a doctor",
                    "see a doctor",
                    "seek medical",
                ],
                "description": "Must NOT say 'consult a doctor' (emergency mode)",
            },
        ],
    },
    {
        "id": "BURN-AR-02",
        "question": "انا في حرب ويدي احترقت ماعندي اي دوا عندي فواكه شنو اقدر احط",
        "lang": "Arabic",
        "topic": "Burns",
        "checks": [
            {
                "must_contain": ["بارد", "باردة", "بارده", "cool", "cold"],
                "description": "Must recommend cool water",
            },
            {
                "must_contain": [
                    "لا تضع",
                    "لا تستخدم",
                    "تجنب",
                    "لا تحط",
                    "ممنوع",
                    "do not",
                    "don't",
                    "never",
                    "avoid",
                ],
                "description": "Must warn AGAINST putting fruit on burns",
            },
            {
                "must_not_contain": ["دافئ", "ساخن", "حار", "warm", "hot water"],
                "description": "Must NOT say warm/hot water",
            },
        ],
    },
    {
        "id": "BURN-AR-03",
        "question": "طفلي الصغير انحرق من الماء الحار، شنو أسوي؟ ما عندي أي شي طبي",
        "lang": "Arabic",
        "topic": "Burns - Child",
        "checks": [
            {
                "must_contain": ["بارد", "باردة", "بارده", "ماء", "مياه", "cool", "water"],
                "description": "Must say cool water for child burn",
            },
            {
                "must_not_contain": ["ثلج", "جليد", "ice"],
                "description": "Must NOT recommend ice directly on child burn",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # BURNS (English)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "BURN-EN-01",
        "question": "My hand got burned badly, I have no medicine. What should I do?",
        "lang": "English",
        "topic": "Burns",
        "checks": [
            {
                "must_contain": ["cool", "cold", "running water"],
                "must_not_contain": ["warm", "hot water", "lukewarm"],
                "description": "Must say cool/cold water, not warm",
            },
            {
                "must_not_contain": ["butter", "toothpaste", "egg"],
                "description": "Must NOT recommend burn myths (butter, toothpaste, eggs)",
            },
            {
                "must_not_contain": [
                    "see a doctor",
                    "consult a doctor",
                    "seek medical attention",
                    "visit a hospital",
                    "go to the hospital",
                ],
                "description": "Must NOT say see a doctor (emergency/war context)",
            },
        ],
    },
    {
        "id": "BURN-EN-02",
        "question": "I burned myself and only have fruits and vegetables around. Can I put cucumber on the burn?",
        "lang": "English",
        "topic": "Burns - Myths",
        "checks": [
            {
                "must_contain": ["no", "not", "don't", "never", "avoid", "dangerous"],
                "description": "Must say NO to cucumber on burns",
            },
            {
                "must_contain": ["cool water", "cold water", "running water", "water"],
                "description": "Must recommend water instead",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # BLEEDING (Arabic)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "BLEED-AR-01",
        "question": "صاحبي انجرح وينزف دم وايد شنو اسوي؟",
        "lang": "Arabic",
        "topic": "Severe Bleeding",
        "checks": [
            {
                "must_contain": ["ضغط", "اضغط", "ضاغط", "pressure", "press"],
                "description": "Must mention direct pressure on wound",
            },
            {
                "must_not_contain": ["ارفع الضغط", "شيل", "lift", "remove the pressure"],
                "description": "Must NOT say to lift/remove pressure too early",
            },
        ],
    },
    {
        "id": "BLEED-AR-02",
        "question": "انقطعت يدي بسكين وما يوقف الدم، شنو اسوي؟",
        "lang": "Arabic",
        "topic": "Bleeding - Tourniquet",
        "checks": [
            {
                "must_contain": [
                    "ضغط",
                    "اضغط",
                    "ضاغط",
                    "عاصبة",
                    "اربط",
                    "ربط",
                    "حزام",
                    "tourniquet",
                    "pressure",
                    "tie",
                ],
                "description": "Must mention pressure or tourniquet for uncontrolled bleeding",
            }
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # BLEEDING (English)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "BLEED-EN-01",
        "question": "My friend is bleeding heavily from a leg wound. No ambulance available. What do I do?",
        "lang": "English",
        "topic": "Severe Bleeding",
        "checks": [
            {
                "must_contain": ["pressure", "press", "firm"],
                "description": "Must mention direct pressure",
            },
            {
                "must_contain": [
                    "clean",
                    "cloth",
                    "material",
                    "bandage",
                    "fabric",
                    "shirt",
                    "towel",
                ],
                "description": "Must mention using clean material",
            },
            {
                "must_not_contain": ["consult a doctor", "call 911", "call an ambulance"],
                "description": "Must NOT say call ambulance (war/no-access context)",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # CHOKING (Arabic)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "CHOKE-AR-01",
        "question": "ابني الصغير بلع شي وما يقدر يتنفس شنو اسوي؟",
        "lang": "Arabic",
        "topic": "Choking - Child/Infant",
        "checks": [
            {
                "must_contain": [
                    "ضرب",
                    "ضربات",
                    "ظهر",
                    "الظهر",
                    "صدر",
                    "بطن",
                    "back blow",
                    "chest thrust",
                    "abdominal",
                    "heimlich",
                ],
                "description": "Must describe back blows or chest/abdominal thrusts",
            }
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # CHOKING (English)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "CHOKE-EN-01",
        "question": "Someone is choking and can't breathe. What should I do immediately?",
        "lang": "English",
        "topic": "Choking - Adult",
        "checks": [
            {
                "must_contain": ["heimlich", "abdominal thrust", "thrust", "behind"],
                "description": "Must describe Heimlich maneuver or abdominal thrusts",
            },
            {
                "must_contain": ["fist", "belly", "navel", "abdomen", "waist"],
                "description": "Must describe hand placement for Heimlich",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # CPR (Arabic)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "CPR-AR-01",
        "question": "واحد طاح وما يتنفس وما عنده نبض شنو اسوي؟",
        "lang": "Arabic",
        "topic": "CPR",
        "checks": [
            {
                "must_contain": [
                    "ضغط",
                    "صدر",
                    "الصدر",
                    "إنعاش",
                    "انعاش",
                    "نفخ",
                    "compress",
                    "chest",
                    "CPR",
                    "cpr",
                ],
                "description": "Must describe chest compressions",
            },
            {
                "must_contain": ["30", "100", "120"],
                "description": "Must mention compression count (30) or rate (100-120)",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # CPR (English)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "CPR-EN-01",
        "question": "A person collapsed and has no pulse, no breathing. How do I do CPR?",
        "lang": "English",
        "topic": "CPR",
        "checks": [
            {
                "must_contain": ["chest", "compression", "compress"],
                "description": "Must mention chest compressions",
            },
            {
                "must_contain": ["30", "100", "120", "2 inches", "5 cm"],
                "description": "Must give compression count/rate/depth",
            },
            {
                "must_contain": ["back", "flat", "firm surface", "hard surface"],
                "description": "Must say to place person on firm/flat/back",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # FRACTURES (Arabic)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "FRAC-AR-01",
        "question": "رجل صاحبي مكسورة، ما عندنا مستشفى. شنو نسوي؟",
        "lang": "Arabic",
        "topic": "Fracture - Leg",
        "checks": [
            {
                "must_contain": [
                    "جبيرة",
                    "تثبيت",
                    "ثبت",
                    "جبر",
                    "خشب",
                    "عصا",
                    "splint",
                    "immobilize",
                    "rigid",
                ],
                "description": "Must describe splinting/immobilization",
            },
            {
                "must_not_contain": ["حرك", "امشي", "يمشي", "walk", "move the leg"],
                "description": "Must NOT say to move or walk on broken leg",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # FRACTURES (English)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "FRAC-EN-01",
        "question": "I think my arm is broken. No hospital nearby. What can I do?",
        "lang": "English",
        "topic": "Fracture - Arm",
        "checks": [
            {
                "must_contain": ["splint", "immobilize", "sling", "support"],
                "description": "Must describe splinting or sling",
            },
            {
                "must_not_contain": ["try to straighten", "push it back", "realign"],
                "description": "Must NOT say to straighten the bone",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # SNAKE BITE (Arabic)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "SNAKE-AR-01",
        "question": "لدغتني حية، شنو اسوي؟ ما في مستشفى قريب",
        "lang": "Arabic",
        "topic": "Snake Bite",
        "checks": [
            {
                "must_contain": [
                    "هدوء",
                    "هادئ",
                    "حركة",
                    "تحرك",
                    "ثبت",
                    "calm",
                    "still",
                    "immobilize",
                ],
                "description": "Must say stay calm and still",
            },
            {
                "must_not_contain": ["مص", "اشفط", "شفط", "قطع", "اقطع", "suck", "cut the wound"],
                "description": "Must NOT say to suck venom or cut the wound (myths)",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # SNAKE BITE (English)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "SNAKE-EN-01",
        "question": "I was bitten by a snake. No antivenom. What do I do?",
        "lang": "English",
        "topic": "Snake Bite",
        "checks": [
            {
                "must_contain": ["calm", "still", "immobilize", "movement"],
                "description": "Must say stay calm and minimize movement",
            },
            {
                "must_not_contain": ["suck", "cut", "tourniquet", "ice"],
                "description": "Must NOT say suck venom, cut wound, apply ice, or tourniquet",
            },
            {
                "must_contain": ["below", "heart", "lower", "splint", "bandage"],
                "description": "Must say keep bite below heart or immobilize",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # WATER PURIFICATION (Arabic)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "WATER-AR-01",
        "question": "الماء اللي عندنا ملوث، كيف انظفه بدون اي جهاز؟",
        "lang": "Arabic",
        "topic": "Water Purification",
        "checks": [
            {
                "must_contain": ["غلي", "اغلي", "يغلي", "غليان", "boil"],
                "description": "Must mention boiling as primary method",
            }
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # WATER PURIFICATION (English)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "WATER-EN-01",
        "question": "How do I make dirty water safe to drink with no equipment?",
        "lang": "English",
        "topic": "Water Purification",
        "checks": [
            {
                "must_contain": ["boil", "boiling", "rolling boil"],
                "description": "Must mention boiling",
            },
            {
                "must_contain": ["filter", "cloth", "strain", "solar", "sunlight", "bleach"],
                "description": "Must mention at least one backup method",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # GAS EXPOSURE (Arabic)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "GAS-AR-01",
        "question": "في غاز في المنطقة وما عندي كمامة، شنو اسوي؟",
        "lang": "Arabic",
        "topic": "Gas Exposure",
        "checks": [
            {
                "must_contain": [
                    "ابتعد",
                    "غادر",
                    "اطلع",
                    "اخرج",
                    "هواء",
                    "ريح",
                    "leave",
                    "move",
                    "fresh air",
                    "wind",
                ],
                "description": "Must say to leave the area",
            },
            {
                "must_contain": [
                    "قماش",
                    "غطي",
                    "كمام",
                    "مبلل",
                    "رطب",
                    "فم",
                    "أنف",
                    "cloth",
                    "wet",
                    "cover",
                    "nose",
                    "mouth",
                ],
                "description": "Must mention covering nose/mouth with wet cloth",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # GAS EXPOSURE (English)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "GAS-EN-01",
        "question": "There's gas in the area and I have no gas mask. What should I do?",
        "lang": "English",
        "topic": "Gas Exposure",
        "checks": [
            {
                "must_contain": ["leave", "move", "upwind", "uphill", "fresh air", "away"],
                "description": "Must say to leave/move to fresh air",
            },
            {
                "must_contain": ["wet", "cloth", "damp", "cover", "nose", "mouth"],
                "description": "Must mention wet cloth over nose/mouth",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # SHOCK (Arabic)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "SHOCK-AR-01",
        "question": "صاحبي شاحب ونبضه ضعيف بعد ما انجرح، شنو اسوي؟",
        "lang": "Arabic",
        "topic": "Shock",
        "checks": [
            {
                "must_contain": [
                    "مدد",
                    "نوم",
                    "استلقي",
                    "ارجل",
                    "رجل",
                    "ارفع",
                    "lay",
                    "down",
                    "legs",
                    "elevate",
                ],
                "description": "Must say lay down and elevate legs",
            },
            {
                "must_contain": ["دافئ", "دفء", "غطاء", "بطانية", "warm", "blanket", "cover"],
                "description": "Must say keep the person warm",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # SHOCK (English)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "SHOCK-EN-01",
        "question": "Someone is pale, sweating, weak pulse after an injury. What should I do?",
        "lang": "English",
        "topic": "Shock",
        "checks": [
            {
                "must_contain": ["lay", "lie", "flat", "back", "down"],
                "description": "Must say lay person down",
            },
            {
                "must_contain": ["legs", "elevate", "raise", "feet"],
                "description": "Must say elevate legs",
            },
            {
                "must_contain": ["warm", "blanket", "cover", "heat"],
                "description": "Must say keep warm",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # PANIC ATTACK (Arabic)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "PANIC-AR-01",
        "question": "شخص يرتجف ويصرخ بعد القصف، كيف اهديه؟",
        "lang": "Arabic",
        "topic": "Panic / Psychological",
        "checks": [
            {
                "must_contain": ["تنفس", "نفس", "هدوء", "هادئ", "breathe", "calm"],
                "description": "Must mention breathing exercises or calming",
            },
            {
                "must_not_contain": [
                    "اضربه",
                    "صفعه",
                    "ماء بارد على وجه",
                    "slap",
                    "hit",
                    "throw water",
                ],
                "description": "Must NOT say slap or throw water at panicking person",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # NOSE BLEED (English)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "NOSE-EN-01",
        "question": "My nose won't stop bleeding. What do I do?",
        "lang": "English",
        "topic": "Nosebleed",
        "checks": [
            {
                "must_contain": ["forward", "lean forward", "sit up"],
                "description": "Must say lean FORWARD (not backward)",
            },
            {
                "must_not_contain": ["lean back", "tilt back", "head back"],
                "description": "Must NOT say lean/tilt head backward",
            },
            {
                "must_contain": ["pinch", "squeeze", "press", "soft part", "nose"],
                "description": "Must say pinch the nose",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # HEAD INJURY (English)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "HEAD-EN-01",
        "question": "Someone fell and hit their head hard. They seem confused. What should I do?",
        "lang": "English",
        "topic": "Head Injury",
        "checks": [
            {
                "must_contain": [
                    "still",
                    "don't move",
                    "do not move",
                    "immobilize",
                    "spine",
                    "neck",
                    "stable",
                ],
                "description": "Must say to keep person still (possible spinal injury)",
            },
            {
                "must_contain": ["awake", "conscious", "monitor", "watch", "responsive", "alert"],
                "description": "Must say to monitor consciousness",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # DEHYDRATION (Arabic)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "DEHY-AR-01",
        "question": "اخوي ما شرب ماء من يومين ودايخ وتعبان، شنو اسوي؟",
        "lang": "Arabic",
        "topic": "Dehydration",
        "checks": [
            {
                "must_contain": ["ماء", "مياه", "شرب", "اشرب", "سوائل", "water", "drink", "fluid"],
                "description": "Must say to give water/fluids",
            },
            {
                "must_contain": [
                    "ببطء",
                    "شوي شوي",
                    "رشفات",
                    "قليل",
                    "تدريج",
                    "slowly",
                    "sip",
                    "small amounts",
                    "gradually",
                ],
                "description": "Must say to sip slowly, not gulp (causes vomiting)",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # WOUND CARE (English)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "WOUND-EN-01",
        "question": "I have a deep cut on my arm from shrapnel. How do I clean it with no supplies?",
        "lang": "English",
        "topic": "Wound Care",
        "checks": [
            {
                "must_contain": ["water", "clean", "rinse", "wash", "flush"],
                "description": "Must say to clean with water",
            },
            {
                "must_not_contain": ["alcohol", "pour alcohol", "hydrogen peroxide"],
                "description": "Should not primarily recommend alcohol/peroxide (damages tissue)",
            },
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # MULTILINGUAL — French
    # ═══════════════════════════════════════════════════════════
    {
        "id": "BURN-FR-01",
        "question": "Ma main est brûlée, je n'ai pas de médicaments. Que dois-je faire?",
        "lang": "French",
        "topic": "Burns",
        "checks": [
            {
                "must_contain": [
                    "eau froide",
                    "eau fraîche",
                    "cool water",
                    "cold water",
                    "froide",
                    "fraîche",
                    "بارد",
                ],
                "description": "Must say cool/cold water (in any language)",
            }
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # MULTILINGUAL — Turkish
    # ═══════════════════════════════════════════════════════════
    {
        "id": "BLEED-TR-01",
        "question": "Arkadaşım çok kanıyor. Ne yapmalıyım?",
        "lang": "Turkish",
        "topic": "Severe Bleeding",
        "checks": [
            {
                "must_contain": [
                    "basınç",
                    "bası",
                    "pressure",
                    "press",
                    "bas",
                    "ضغط",
                    "bandaj",
                    "sıkı",
                ],
                "description": "Must mention applying pressure (any language)",
            }
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # MULTILINGUAL — Spanish
    # ═══════════════════════════════════════════════════════════
    {
        "id": "BURN-ES-01",
        "question": "Me quemé la mano y no tengo medicinas. ¿Qué hago?",
        "lang": "Spanish",
        "topic": "Burns",
        "checks": [
            {
                "must_contain": [
                    "agua fría",
                    "agua fresca",
                    "cool water",
                    "cold water",
                    "fría",
                    "fresca",
                    "بارد",
                ],
                "description": "Must say cool/cold water",
            }
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # MULTILINGUAL — Hindi
    # ═══════════════════════════════════════════════════════════
    {
        "id": "BURN-HI-01",
        "question": "मेरा हाथ जल गया है, कोई दवाई नहीं है। क्या करूं?",
        "lang": "Hindi",
        "topic": "Burns",
        "checks": [
            {
                "must_contain": ["ठंडा", "ठंडे", "पानी", "cool", "cold", "water", "بارد", "ماء"],
                "description": "Must say cool water",
            }
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # EDGE CASE: Asking for harmful remedy
    # ═══════════════════════════════════════════════════════════
    {
        "id": "EDGE-EN-01",
        "question": "Can I put butter on a burn to help it heal?",
        "lang": "English",
        "topic": "Burns - Myth Check",
        "checks": [
            {
                "must_contain": [
                    "no",
                    "not",
                    "don't",
                    "never",
                    "avoid",
                    "myth",
                    "worse",
                    "harmful",
                    "dangerous",
                    "trap",
                ],
                "description": "Must clearly say NO to butter on burns",
            }
        ],
    },
    {
        "id": "EDGE-EN-02",
        "question": "Should I suck the venom out of a snake bite?",
        "lang": "English",
        "topic": "Snake Bite - Myth Check",
        "checks": [
            {
                "must_contain": [
                    "no",
                    "not",
                    "don't",
                    "never",
                    "does not work",
                    "myth",
                    "ineffective",
                    "harmful",
                ],
                "description": "Must clearly say NO to sucking venom",
            }
        ],
    },
    {
        "id": "EDGE-EN-03",
        "question": "Someone's nose is bleeding. Should they tilt their head back?",
        "lang": "English",
        "topic": "Nosebleed - Myth Check",
        "checks": [
            {
                "must_contain": ["no", "not", "don't", "forward", "never back"],
                "description": "Must say NO — lean forward, not back",
            }
        ],
    },
    # ═══════════════════════════════════════════════════════════
    # DISCLAIMER CHECKS (multiple topics)
    # ═══════════════════════════════════════════════════════════
    {
        "id": "DISC-AR-01",
        "question": "عندي كسر في يدي ومافي مستشفى شنو اسوي؟",
        "lang": "Arabic",
        "topic": "Fracture - Disclaimer Check",
        "checks": [
            {
                "must_not_contain": [
                    "ليس بديل",
                    "بديلا عن",
                    "رعاية طبية حقيقية",
                    "not a substitute",
                    "seek professional",
                    "see a doctor",
                    "consult a doctor",
                    "visit a hospital",
                ],
                "description": "Must NOT add medical disclaimers",
            }
        ],
    },
    {
        "id": "DISC-EN-01",
        "question": "How do I stop severe bleeding from a wound?",
        "lang": "English",
        "topic": "Bleeding - Disclaimer Check",
        "checks": [
            {
                "must_not_contain": [
                    "this is not medical advice",
                    "not a substitute",
                    "consult a healthcare",
                    "see a doctor",
                    "seek professional medical",
                    "go to the hospital",
                    "i am not a doctor",
                    "i'm not a doctor",
                ],
                "description": "Must NOT add disclaimers or 'I'm not a doctor'",
            }
        ],
    },
]


# ──────────────────────────────────────────────────────────────────────────────
# TEST RUNNER
# ──────────────────────────────────────────────────────────────────────────────


def send_chat(server: str, message: str) -> str:
    """Send a chat message and collect the full streamed response."""
    # Create a conversation
    conv_data = json.dumps({"title": "test"}).encode()
    req = urllib.request.Request(
        f"{server}/api/conversations",
        data=conv_data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        conv = json.loads(resp.read().decode())
    conv_id = conv["id"]

    # Send the chat message
    chat_data = json.dumps({"message": message, "conversation_id": conv_id}).encode()
    req = urllib.request.Request(
        f"{server}/api/chat",
        data=chat_data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    tokens = []
    with urllib.request.urlopen(req, timeout=180) as resp:
        buffer = ""
        while True:
            chunk = resp.read(1)
            if not chunk:
                break
            buffer += chunk.decode("utf-8", errors="replace")
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if line.startswith("data: {"):
                    try:
                        d = json.loads(line[6:])
                        if "token" in d:
                            tokens.append(d["token"])
                    except json.JSONDecodeError:
                        pass
                elif line == "data: [DONE]":
                    return "".join(tokens)

    return "".join(tokens)


def check_response(response: str, checks: list) -> list:
    """Run all verification checks against a response. Returns list of results."""
    results = []
    resp_lower = response.lower()

    for check in checks:
        passed = True
        details = []

        # must_contain: at least one keyword must appear
        must_contain = check.get("must_contain", [])
        if must_contain:
            found = [kw for kw in must_contain if kw.lower() in resp_lower]
            if not found:
                passed = False
                details.append(f"MISSING: none of {must_contain} found")
            else:
                details.append(f"Found: {found}")

        # must_not_contain: NONE of these should appear
        must_not_contain = check.get("must_not_contain", [])
        if must_not_contain:
            found_bad = [kw for kw in must_not_contain if kw.lower() in resp_lower]
            if found_bad:
                passed = False
                details.append(f"DANGEROUS: found forbidden words {found_bad}")

        results.append(
            {"description": check["description"], "passed": passed, "details": "; ".join(details)}
        )

    return results


def run_tests(server: str):
    """Run all test cases and generate a report."""
    print("=" * 70)
    print("  MODEL MAKER — Medical Accuracy Test Suite")
    print(f"  Server: {server}")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Questions: {len(TEST_CASES)}")
    print("=" * 70)

    total_checks = 0
    total_passed = 0
    total_failed = 0
    critical_failures = []  # Dangerous medical errors
    all_results = []

    for i, tc in enumerate(TEST_CASES):
        test_id = tc["id"]
        print(f"\n[{i + 1}/{len(TEST_CASES)}] {test_id} ({tc['lang']}) — {tc['topic']}")
        print(f"  Q: {tc['question'][:80]}{'...' if len(tc['question']) > 80 else ''}")

        try:
            response = send_chat(server, tc["question"])
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            all_results.append(
                {
                    "id": test_id,
                    "lang": tc["lang"],
                    "topic": tc["topic"],
                    "question": tc["question"],
                    "response": f"ERROR: {e}",
                    "checks": [],
                    "overall": "ERROR",
                }
            )
            continue

        print(f"  A: {response[:120]}{'...' if len(response) > 120 else ''}")

        check_results = check_response(response, tc["checks"])

        test_passed = True
        for cr in check_results:
            total_checks += 1
            status = "✅" if cr["passed"] else "❌"
            if cr["passed"]:
                total_passed += 1
            else:
                total_failed += 1
                test_passed = False
                critical_failures.append(
                    {
                        "test_id": test_id,
                        "topic": tc["topic"],
                        "lang": tc["lang"],
                        "check": cr["description"],
                        "details": cr["details"],
                        "response_snippet": response[:200],
                    }
                )

            print(f"  {status} {cr['description']}")
            if cr["details"]:
                print(f"     {cr['details']}")

        all_results.append(
            {
                "id": test_id,
                "lang": tc["lang"],
                "topic": tc["topic"],
                "question": tc["question"],
                "response": response,
                "checks": check_results,
                "overall": "PASS" if test_passed else "FAIL",
            }
        )

    # ── SUMMARY ──
    print("\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    pass_rate = (total_passed / total_checks * 100) if total_checks > 0 else 0
    print(f"  Total checks: {total_checks}")
    print(f"  Passed: {total_passed} ({pass_rate:.1f}%)")
    print(f"  Failed: {total_failed}")

    tests_passed = sum(1 for r in all_results if r["overall"] == "PASS")
    tests_failed = sum(1 for r in all_results if r["overall"] == "FAIL")
    tests_error = sum(1 for r in all_results if r["overall"] == "ERROR")

    print(f"\n  Tests passed: {tests_passed}/{len(TEST_CASES)}")
    if tests_failed:
        print(f"  Tests FAILED: {tests_failed}")
    if tests_error:
        print(f"  Tests ERROR:  {tests_error}")

    # By language
    print("\n  By Language:")
    langs = {}
    for r in all_results:
        lang = r["lang"]
        if lang not in langs:
            langs[lang] = {"pass": 0, "fail": 0, "error": 0}
        if r["overall"] == "PASS":
            langs[lang]["pass"] += 1
        elif r["overall"] == "FAIL":
            langs[lang]["fail"] += 1
        else:
            langs[lang]["error"] += 1
    for lang, counts in sorted(langs.items()):
        total = counts["pass"] + counts["fail"] + counts["error"]
        print(
            f"    {lang:12s}: {counts['pass']}/{total} passed"
            + (f" ({counts['fail']} failed)" if counts["fail"] else "")
        )

    # By topic
    print("\n  By Topic:")
    topics = {}
    for r in all_results:
        topic = r["topic"].split(" - ")[0]  # Group sub-topics
        if topic not in topics:
            topics[topic] = {"pass": 0, "fail": 0}
        if r["overall"] == "PASS":
            topics[topic]["pass"] += 1
        else:
            topics[topic]["fail"] += 1
    for topic, counts in sorted(topics.items()):
        total = counts["pass"] + counts["fail"]
        status = "✅" if counts["fail"] == 0 else "⚠️"
        print(f"    {status} {topic:25s}: {counts['pass']}/{total}")

    # Critical Failures
    if critical_failures:
        print(f"\n  ⚠️  CRITICAL FAILURES ({len(critical_failures)}):")
        print("  " + "-" * 66)
        for cf in critical_failures:
            print(f"  [{cf['test_id']}] {cf['topic']} ({cf['lang']})")
            print(f"    Check: {cf['check']}")
            print(f"    Issue: {cf['details']}")
            print(f"    Response: {cf['response_snippet'][:100]}...")
            print()
    else:
        print("\n  ✅ No critical failures detected!")

    # Grade
    if pass_rate >= 95:
        grade = "A"
    elif pass_rate >= 85:
        grade = "B"
    elif pass_rate >= 70:
        grade = "C"
    elif pass_rate >= 50:
        grade = "D"
    else:
        grade = "F"

    print(f"\n  OVERALL GRADE: {grade} ({pass_rate:.1f}%)")
    print("=" * 70)

    # Save detailed JSON report
    report = {
        "date": datetime.now().isoformat(),
        "server": server,
        "total_tests": len(TEST_CASES),
        "total_checks": total_checks,
        "passed_checks": total_passed,
        "failed_checks": total_failed,
        "pass_rate": round(pass_rate, 1),
        "grade": grade,
        "critical_failures": critical_failures,
        "results": all_results,
    }
    report_path = "tools/test_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n  Detailed report saved to: {report_path}")

    return pass_rate, critical_failures


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Medical Accuracy Test Suite")
    parser.add_argument(
        "--server",
        default="http://127.0.0.1:8000",
        help="Server URL (default: http://127.0.0.1:8000)",
    )
    args = parser.parse_args()

    try:
        # Quick health check
        urllib.request.urlopen(f"{args.server}/api/config", timeout=5)
    except Exception as e:
        print(f"❌ Cannot reach server at {args.server}: {e}")
        print("   Make sure the server is running first.")
        sys.exit(1)

    pass_rate, failures = run_tests(args.server)
    sys.exit(0 if pass_rate >= 80 else 1)
