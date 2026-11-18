# Astronaut Health Monitoring Software: Research Document

**Challenge:** Create health monitoring software that gathers health indicators and enables astronauts to evaluate and act on the status of their own health during long-duration missions.
**Supporting dataset:** NASA OSDR OSD-574 / GLDS-566 (swab metagenomics, Inspiration4 crew, pre-launch vs post-return)
**Prepared:** 15 Nov 2026 (submission closes tonight, 11:59 PM local time)

---

## 1. Problem statement

Long-duration missions (Moon, Mars transit) expose crew to radiation, isolation and confinement, altered gravity and a closed environment. The challenge names four health risk areas: **immune changes, bone loss, cardiovascular events and behavioral health problems**. On distant missions, communication delays and limited ground support mean astronauts must **notice change in themselves and act**, with less real-time help from flight surgeons.

**Core need:** a tool that turns scattered health signals into a clear, personal, actionable picture that works offline and without a doctor in the loop.

## 2. Users and design principles

| User | Need |
|---|---|
| Astronaut (primary) | Fast daily status, plain-language trends, concrete next steps |
| Crew medical officer | Cross-crew view, history, escalation summary |
| Ground flight surgeons | Compressed, delayed-sync reports and alerts |

Principles:
1. **Autonomy first:** works offline, computes on-device, syncs to ground when a link exists.
2. **Personal baselines:** compare each astronaut to their own pre-flight norm, not population averages.
3. **Explainable alerts:** every warning says what changed, by how much, and why it matters.
4. **Actionable:** each status links to a countermeasure or a decision step.
5. **Low burden:** passive data wherever possible; short check-ins only where needed.
6. **Privacy:** crew data stays under crew/agency control; minimal sharing.

## 3. Health risks mapped to measurable indicators

| Risk area | Indicators that can be gathered | Source | Cadence |
|---|---|---|---|
| **Cardiovascular** | Resting heart rate, heart rate variability, blood pressure, SpO2, exercise heart-rate recovery | Wearable, cuff | Continuous / daily |
| **Bone and muscle loss** | Exercise load (type, duration, resistive volume), daily activity, nutrition and vitamin D intake, periodic imaging/biomarker results | Exercise logs, wearable, medical records | Daily / periodic |
| **Immune and infection** | Temperature, symptoms (sore throat, rash, fatigue), skin and wound check, microbiome profile, latent-virus markers if available | Self-report, thermometer, lab/sequencing | Daily / periodic |
| **Behavioral and cognitive** | Sleep duration/quality, mood and stress check-in, social interaction, reaction-time or short cognitive test, workload | Wearable, short survey, task app | Daily |
| **Environment** | Radiation dose, CO2, temperature, noise | Habitat sensors | Continuous |

## 4. Proposed solution: system concept

**Name (working):** Astronaut Health Dashboard

**Modules**
1. **Data ingestion:** wearables (HR, HRV, sleep, activity, temperature), manual entry, habitat sensors, imported lab files.
2. **Baseline engine:** builds each astronaut's pre-flight and rolling in-flight baseline per indicator.
3. **Deviation and trend detection:** z-score and trend slope against personal baseline; combined rules across indicators (e.g. low sleep + elevated resting HR + low mood).
4. **Risk status:** four domain scores (cardio, musculoskeletal, immune, behavioral) shown as green / amber / red.
5. **Guidance layer:** for each amber/red state, shows likely causes and suggested countermeasures (adjust exercise, rest, hydration, check-in with crew medical officer) and a clear escalation rule.
6. **Reports:** weekly summary; compressed packet for ground when communication is available.

**Architecture:** offline-first local app, local database, on-device analytics, optional store-and-forward sync. No dependence on cloud inference.

**Interface:** one home screen with four domain cards, a 7/30-day trend per indicator, a daily 60-second check-in, and a "what should I do" panel.

## 5. Evidence from the supporting dataset (microbiome)

The OSD-574 / GLDS-566 assay table covers 8 swab metagenomes: 4 Inspiration4 crew (C001 to C004), sampled about 44 days before launch (L-44) and 1 day after return (R+1), sequenced on Illumina NovaSeq 6000 (2 x 150 bp).

| Subject | Human reads removed, L-44 → R+1 (%) | Read depth, L-44 → R+1 |
|---|---|---|
| C001 | 40.11 → 85.06 | 5,407,193 → 1,183,943 |
| C002 | 29.43 → 44.48 | 538,857 → 72,399 |
| C003 | 12.20 → 40.00 | 1,999,084 → 2,729,312 |
| C004 | 41.20 → 77.83 | 4,372,797 → 1,768,757 |

Mean human-read fraction rose from about 31% to about 62%; mean depth fell from about 3.08 M to about 1.44 M reads. The file contains no taxonomic or pathway abundances, only a manifest of files (taxonomy, KO/pathway tables, bins, MAGs) that exist per sample.

**What this means for the software design**
1. **Microbiome is a periodic, lab-derived indicator, not a daily one.** It belongs in the immune/infection domain as an occasional input, not a live sensor.
2. **Data quality varies a lot between samples.** One sample (C002 R+1) has only 72,399 reads, and genome-recovery products exist for just 3 of 8 samples. The software should show a **confidence flag** (sequencing depth, host-DNA fraction) beside any microbiome result and avoid strong alerts from low-quality data.
3. **Paired before/after design matches the personal-baseline approach:** each astronaut's pre-flight sample is their own reference. In this data, every crew member shows the same direction of change in host-DNA fraction, but with n = 4 and a short mission this is a design motivation, not a clinical finding.
4. **Pipeline outputs are standardised** (MetaPhlAn taxonomy, pathway abundance tables), so the app can import them as files and summarise them (diversity change, notable taxa, antimicrobial-resistance-related pathways) without running sequencing analysis onboard.

## 6. Alert logic (example)

- **Green:** all indicators within personal baseline range.
- **Amber:** one indicator beyond about 2 standard deviations for 2 or more consecutive days, or a downward 7-day trend in a protected indicator (sleep, HRV, exercise volume).
- **Red:** two or more domains amber together, any acute threshold breach (e.g. fever, chest pain symptom, low SpO2), or a symptom the crew member flags as severe. Red shows an escalation checklist and prepares a report for the medical officer and ground.

Thresholds are placeholders and need clinical validation.

## 7. Validation plan
1. **Synthetic crew data:** simulate 180-day missions with injected events (illness, sleep loss, deconditioning) and measure detection delay and false-alert rate.
2. **Public analog datasets:** test on open wearable/sleep datasets, plus the microbiome tables from OSDR for the immune module.
3. **Usability testing:** short task-based tests with volunteers; target a daily check-in under 60 seconds.
4. **Expert review:** have a clinician or space-medicine specialist check thresholds and guidance text.

## 8. Limitations and risks
- Not a medical device; guidance is decision support and must be reviewed by clinicians before real use.
- Wearable accuracy in microgravity is not guaranteed.
- Alert fatigue and false positives are likely without tuning.
- Small crews mean little data for population-level models; personalisation helps but baselines need enough pre-flight data.
- The microbiome dataset is small (n = 4, 2 timepoints) and unevenly sequenced, so it supports design decisions, not clinical conclusions.
- Behavioral self-report can be underreported when crew fear mission impact; passive signals and privacy controls reduce this.

## 9. Sources to cite
- Challenge statement: "Create Health Monitoring Software for Astronauts on Space Missions" (hackathon page)
- NASA Open Science Data Repository (OSDR): OSD-574 / GLDS-566 study page and README
- NASA Human Research Program, for the standard spaceflight risk areas (verify exact pages before citing)
