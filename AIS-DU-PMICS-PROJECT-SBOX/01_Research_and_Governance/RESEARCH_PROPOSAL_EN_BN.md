# 📘 Research Proposal & Governance Blueprint (গবেষণা প্রস্তাবনা ও পরিচালনা রূপরেখা)
## Predictive Memory Integrity and Contamination Defense in Agentic LLM Architectures
### এজেন্টিক এলএলএম আর্কিটেকচারে প্রেডিক্টিভ মেমোরি ইন্টিগ্রিটি এবং দূষণ প্রতিরোধ ব্যবস্থা

**Project Identifier:** `AIS-DU-PMICS-PROJECT-SBOX`  
**Academic Alignment:** Dhaka University (DU) — PMICS Research Initiative  
**Human Owner & Final Authority:** Founder Aminul Islam Shamim (AIS) | ID: `MCORE-FDR-AIS-001`  
**Host Architecture:** `mcorebd` (Debian 13 Trixie / WSL2 Sovereign Infrastructure)  
**Security Baseline:** Zero-Trust Ingress (Cloudflare QUIC), Cryptographic Provenance (SHA-256)  
**Economic Mandate:** Zero-Cost Architectural Doctrine (Zero Recurring Cloud Bill)  

---

## 1. Abstract / সারসংক্ষেপ

### English
As autonomous agentic AI systems transition from stateless request-response models to stateful, persistent memory architectures (vector stores, semantic caches, and graph-based lineage), they become uniquely vulnerable to **Memory Contamination and Indirect Prompt Poisoning**. Adversaries can inject adversarial tokens into retrieved memory contexts, subverting agent decision-making while evading standard boundary firewalls. This research introduces a sovereign, zero-cost **Memory Trust Engine (MTE)** providing dual-tier pre-inference provenance scoring, lexical hazard quarantine, and SHA-256 hash-chained memory lineage.

### বাংলা
স্বায়ত্তশাসিত এজেন্টিক এআই ব্যবস্থা যখন স্টেটলেস রিকোয়েস্ট-রেসপন্স মডেল থেকে স্টেটফুল, পারসিস্টেন্ট মেমোরি আর্কিটেকচারে (ভেক্টর স্টোর, সিম্যান্টিক ক্যাশ এবং গ্রাফ-ভিত্তিক মেমোরি লাইনিয়েজ) রূপান্তরিত হয়, তখন সেগুলি **মেমোরি দূষণ এবং পরোক্ষ প্রম্পট পয়জনিং**-এর ঝুঁকিতে পড়ে। আক্রমণকারীরা সংরক্ষিত মেমোরি কনটেক্সটে বিষাক্ত টোকেন প্রবেশ করিয়ে এজেন্টের সিদ্ধান্ত প্রক্রিয়াকে বিকৃত করতে পারে। এই গবেষণায় একটি দেশীয় এবং সম্পূর্ণ জিরো-কস্ট **মেমোরি ট্রাস্ট ইঞ্জিন (MTE)** প্রস্তাব করা হয়েছে যা প্রি-ইনফারেন্স প্রোভেন্যান্স স্কোরিং, লেক্সিক্যাল হ্যাজার্ড কোয়ারেন্টাইন এবং SHA-256 হ্যাশ-চেইন মেমোরি লাইনিয়েজ নিশ্চিত করে।

---

## 2. Problem Statement / সমস্যা বিবৃতি

1. **Adversarial Memory Poisoning:** Malicious payloads stored in shared data sources bypass traditional API gateways and contaminate context windows during RAG retrieval.
2. **Lack of Cryptographic Lineage:** Standard agent frameworks do not track or verify the historical provenance chain of memory items, allowing silent overwrites.
3. **Enterprise Cost Barriers:** Commercial security overlays impose expensive API fees. A sovereign defense architecture must run at zero ongoing operational cost.

---

## 3. Core Research Objectives / গবেষণার মূল উদ্দেশ্যসমূহ

* **Objective 1 (Pre-Inference Quarantine):** Develop an isolated evaluation engine that scores every memory write against strict source provenance and hazard dictionaries before LLM ingestion.
* **Objective 2 (Hash-Chained Lineage):** Implement SHA-256 tamper-evident chaining for all accepted memory blocks, logging rejected payloads into an unalterable quarantine ledger.
* **Objective 3 (Zero-Cost Bare-Metal Sovereignty):** Demonstrate full operational readiness on local Linux compute (Python 3.14, PostgreSQL 17 + pgvector, Qdrant) without relying on paid third-party infrastructure.

---

## 4. Governance & Human Authority / পরিচালনা এবং মানবিক কর্তৃত্ব

* **Final Authority:** Founder Aminul Islam Shamim (AIS) retains absolute approval rights over scope, expenditure, experimental validation claims, and public disclosures.
* **Ethics & Safety:** All adversarial injection vectors are confined to isolated local test environments without external network exposure.
