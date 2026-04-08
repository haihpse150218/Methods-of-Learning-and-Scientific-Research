# HUONG DAN CHAY HarnessEval

> Ngay tao: 07/04/2026
> Trang thai: Da test thanh cong voi Ollama (qwen2.5:1.5b)

---

## 0. Yeu cau he thong

| Thanh phan | Phien ban | Kiem tra |
|------------|-----------|---------|
| Python | >= 3.10 | `python --version` |
| Docker Desktop | >= 29.x | `docker --version` (phai dang chay) |
| Git | >= 2.x | `git --version` |
| Ollama | >= 0.20 | `ollama --version` (tuy chon, de test mien phi) |

**RAM:** >= 8GB (16GB khuyen nghi neu dung model 7B)

---

## 1. Cai dat

### 1.1. Clone project (neu chua co)

```bash
cd "D:\MSA-FPT\Methods of Learnning and scientific research"
git clone <repo-url>
```

### 1.2. Cai dat HarnessEval toolkit

```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2"
pip install -e ".[dev]"
pip install flask
```

### 1.3. Cai dat SWE-Agent

```bash
cd SWE-agent
pip install -e .
cd ..
```

### 1.4. Kiem tra cai dat

```bash
# Kiem tra harness_eval
python -m pytest tests/ -v                    # 123 tests phai pass

# Kiem tra SWE-Agent
PYTHONIOENCODING=utf-8 python -c "import sweagent; print(sweagent.__version__)"

# Kiem tra Docker
docker ps                                     # khong bao loi la OK

# Kiem tra CLI
harness-eval info                             # hien 27 conditions
```

---

## 2. Chay experiment

### 2.1. Cach A: Test voi Ollama (MIEN PHI — khong can API key)

**Buoc 1:** Dam bao Ollama dang chay va co model

```bash
ollama list                                   # xem model da co
# Neu chua co model:
ollama pull qwen2.5:1.5b                      # nhe, 986MB, ket qua kem
# HOAC (khuyen nghi):
ollama pull qwen2.5-coder:7b                  # tot hon, 4.7GB
```

**Buoc 2:** Mo Docker Desktop (bat buoc)

**Buoc 3:** Chay 3 conditions test

```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2/SWE-agent"
bash run_test.sh
```

Thoi gian: ~5-10 phut cho ca 3 conditions.

Script se chay:
- Condition 1: `full_full_ollama` — tat ca tools, full context
- Condition 2: `medium_sliding_window_ollama` — tools trung binh, sliding window
- Condition 3: `minimal_summary_ollama` — chi co bash, context nen

**Buoc 4:** Convert ket qua sang format UI

```bash
python convert_results.py
```

**Buoc 5:** Mo Flask app de xem ket qua

```bash
cd ..
python app/server.py
```

Mo browser: http://localhost:5000

### 2.2. Cach B: Test voi API key (KET QUA TOT)

**Buoc 1:** Set API key

```bash
# Chon 1 trong 3:
export ANTHROPIC_API_KEY="sk-ant-api03-..."       # Claude (~$0.35/eval)
export OPENAI_API_KEY="sk-proj-..."                # GPT-4o (~$0.30/eval)
export DEEPSEEK_API_KEY="sk-..."                   # DeepSeek (~$0.15/eval)
```

**Buoc 2:** Chay 1 condition test

```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2/SWE-agent"

# Vi du: Full tools + Full context + Claude
python -m sweagent run \
  --config config/harness_eval/base.yaml \
  --config config/harness_eval/tool_full.yaml \
  --config config/harness_eval/ctx_full.yaml \
  --config config/harness_eval/be_claude.yaml \
  --env.repo.github_url "https://github.com/SWE-agent/test-repo" \
  --problem_statement.github_url "https://github.com/SWE-agent/test-repo/issues/1" \
  --output_dir trajectories/test_harness/full_full_claude
```

**Buoc 3:** Convert + xem

```bash
python convert_results.py
cd .. && python app/server.py
```

### 2.3. Cach C: Chay 1 condition bat ky (tu chon)

Cau truc lenh:

```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2/SWE-agent"

python -m sweagent run \
  --config config/harness_eval/base.yaml \
  --config config/harness_eval/tool_<LEVEL>.yaml \
  --config config/harness_eval/ctx_<STRATEGY>.yaml \
  --config config/harness_eval/be_<BACKEND>.yaml \
  --env.repo.github_url "<GITHUB_REPO_URL>" \
  --problem_statement.github_url "<GITHUB_ISSUE_URL>" \
  --output_dir trajectories/test_harness/<CONDITION_ID>
```

**Thay the:**

| Placeholder | Gia tri co the |
|-------------|---------------|
| `<LEVEL>` | `full`, `medium`, `minimal` |
| `<STRATEGY>` | `full`, `sliding_window`, `summary` |
| `<BACKEND>` | `claude`, `gpt`, `deepseek`, `ollama` |
| `<CONDITION_ID>` | vi du: `full_sliding_window_claude` |

---

## 3. Xem ket qua tren Flask UI

### 3.1. Khoi dong

```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2"
python app/server.py
```

Mo browser: **http://localhost:5000**

### 3.2. 5 Tabs

| Tab | Chuc nang | Cach dung |
|-----|-----------|-----------|
| **1. Config** | Chon tool/context/backend, xem condition info | Click radio buttons, bam "Generate YAML" |
| **2. Pipeline** | Xem 6 buoc pipeline | Chon condition tu Tab 1, bam "View Pipeline" |
| **3. Logs** | Duyet tat ca trajectory logs | Click vao task de xem chi tiet turns + metrics |
| **4. Compare** | So sanh nhieu conditions | Tick checkbox o Tab 3, bam "Compare Selected" |
| **5. ANOVA** | Phan tich thong ke | Bam "Run ANOVA on Sample Data" hoac "Run on Trajectories" |

### 3.3. Workflow xem ket qua

```
Tab 3 (Logs)
  → Tick 2-3 logs tu cac conditions khac nhau
  → Bam "Compare Selected"
  → Chuyen sang Tab 4 (Compare)
  → Xem bang so sanh + bar chart
  → Xem Cross-Backend Portability (M3.1, M3.2) neu chon nhieu backends

Tab 5 (ANOVA)
  → Bam "Run ANOVA on Sample Data" de xem demo
  → Hoac "Run ANOVA on Trajectories" khi da co du data
  → Xem ANOVA table, pie chart, hypothesis H1-H4
```

---

## 4. Chay tests

```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2"

# Chay tat ca 123 tests
python -m pytest tests/ -v

# Chay tung module
python -m pytest tests/test_configs.py -v      # 36 tests — configs
python -m pytest tests/test_metrics.py -v      # 38 tests — 7 metrics
python -m pytest tests/test_analysis.py -v     # 10 tests — ANOVA
python -m pytest tests/test_parser.py -v       # 22 tests — parser
python -m pytest tests/test_runner.py -v       # 17 tests — runner
```

---

## 5. Chay dry-run pipeline (khong can Docker/API)

```bash
cd "NCKK-Docs/de-tai/DE-CUONG-HarnessEval-v2"

# Pilot: 5 conditions x 20 tasks (synthetic data)
python -c "
from harness_eval.pipeline.runner import run_pilot
results = run_pilot('app/trajectories/pilot', dry_run=True)
print(f'Done: {len(results)} conditions')
for r in results:
    print(f'  {r.condition_id}: {r.resolve_rate:.0%} resolve, \${r.total_cost:.2f}')
"

# Full: 27 conditions x 8 tasks (synthetic data)
python -c "
from harness_eval.pipeline.runner import run_full
results = run_full('app/trajectories/full_dry', dry_run=True)
print(f'Done: {len(results)} conditions')
"
```

---

## 6. Cau truc thu muc

```
DE-CUONG-HarnessEval-v2/
├── harness_eval/                    # Python package chinh
│   ├── configs/                     # 27 conditions (3x3x3)
│   ├── metrics/                     # 7 metrics (M1.1-M3.2)
│   ├── parsers/                     # Parse .traj + JSON trajectories
│   ├── pipeline/                    # ANOVA analysis + runner
│   ├── harness/                     # Interfaces + factory cho SWE-Agent
│   └── cli.py                       # CLI: harness-eval info
├── tests/                           # 123 tests (100% pass)
├── app/                             # Flask UI (5 tabs)
│   ├── server.py                    # Flask app
│   ├── templates/                   # 7 Jinja2 templates
│   ├── static/css/                  # Dark theme CSS
│   └── trajectories/                # Trajectory JSON files (UI doc tu day)
├── SWE-agent/                       # SWE-Agent clone
│   ├── config/harness_eval/         # 10 YAML configs cho ablation
│   ├── run_test.sh                  # Script test 3 conditions
│   └── convert_results.py           # Convert .traj -> JSON cho Flask
├── scripts/generate_samples.py      # Generate sample data
├── pyproject.toml                   # Package config
└── HUONG-DAN-CHAY.md               # FILE NAY
```

---

## 7. Xu ly loi thuong gap

### Docker khong chay

```
Error: failed to connect to the docker API
```
→ Mo Docker Desktop, doi 30 giay, thu lai.

### Windows long path

```
Error: Filename too long
```
→ `git config --global core.longpaths true`

### Ollama khong ket noi

```
Error: Connection refused localhost:11434
```
→ Chay `ollama serve` trong terminal khac, hoac kiem tra `ollama ps`.

### SWE-Agent emoji error (Windows)

```
UnicodeEncodeError: 'charmap' codec can't encode character
```
→ Them `PYTHONIOENCODING=utf-8` truoc lenh, hoac set trong terminal:
```bash
export PYTHONIOENCODING=utf-8
```

### pip install loi "Multiple top-level packages"

```
Error: Multiple top-level packages discovered in a flat-layout
```
→ Da fix trong `pyproject.toml`. Chay lai `pip install -e ".[dev]"`.

---

## 8. Lien he

| File | Noi dung |
|------|---------|
| `Plan-Coding-HarnessEval.md` | Chi tiet tung session coding |
| `Plan-HarnessEval.md` | Tong quan toan bo du an |
| `DE-CUONG-HarnessEval-v2.md` | De cuong nghien cuu |
