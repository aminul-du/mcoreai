# =============================================================================
# AIS-DU-PMICS-PROJECT-SBOX: Google Colab Native Drive Verification Cell
# Run this inside your Colab Notebook connected to https://colab.mcoreai.dev
# =============================================================================
from google.colab import drive
import os, hashlib
from pathlib import Path

drive.mount("/content/drive")
ROOT_PATH = Path("/content/drive/MyDrive/AIS-DU-PMICS-PROJECT-SBOX")

if not ROOT_PATH.exists():
    raise FileNotFoundError(f"Root folder not found at: {ROOT_PATH}")

print("✅ Found Root:", ROOT_PATH)

SUBFOLDERS = [
    "01_Research_and_Governance",
    "02_Data_and_Provenance",
    "03_Compute_Notebooks",
    "04_Memory_Security_Experiments",
    "05_Evidence_and_Validation",
    "06_Presentation_and_Reports"
]

for sub in SUBFOLDERS:
    p = ROOT_PATH / sub
    p.mkdir(parents=True, exist_ok=True)
    print(f"  📁 Subfolder verified: {sub}")

# G4: Non-sensitive transfer verification
test_file = ROOT_PATH / "05_Evidence_and_Validation" / "g4_transfer_probe.txt"
payload = f"AIS-DU-PMICS G4 Transfer Probe Verification at {hashlib.sha256(bAIS-DU-PMICS).hexdigest()}
"
with open(test_file, "w") as f:
    f.write(payload)

with open(test_file, "rb") as f:
    sha = hashlib.sha256(f.read()).hexdigest()

print(f"✅ G4 Probe Verified: {test_file.name} (SHA-256: {sha})")
