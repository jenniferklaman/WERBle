# WERBle

**WERBle** is a lightweight tool for calculating Word Error Rate (WER) in ASR systems. Designed with low-resource projects in mind, it helps you compare models, debug transcripts, and track improvements with ease (hopefully...).

---

## How to Get Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/WERBle.git
cd WERBle
```

### 2. Install dependencies and Setting up the Venv (recommended)

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

```bash
pip install -r requirements.txt
```

### 3. Run a basic WER check

```bash
python -m werble.cli --ref refs.txt --hyp hyps.txt

```

- `refs.txt`: ground truth transcripts (one per line)  
- `hyps.txt`: model output (same order, one per line)

### 4. Example output

```
WER: 18.7%
Insertions: 3  Deletions: 4  Substitutions: 5
```

---

## Next Steps

- Per-token error analysis  
- Visualization support  
- Structure mode (WER from IPA + phoneme mappings)  
- Python + C hybrid implementation

---

## License

MIT License. See `LICENSE` file for details.
