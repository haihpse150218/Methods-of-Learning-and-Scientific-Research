# [2025] Deng et al. — SWE-Bench Pro

## Metadata
- **arXiv:** 2509.16941
- **Venue:** Scale AI Technical Report
- **Year:** 2025
- **Authors:** Xiang Deng, Jeff Da, Edwin Pan, Yannis Yiming He, Charles Ide, Kanak Garg, et al.

## 1. Van de (Problem)
Cac benchmark hien tai (SWE-Bench, SWE-Bench Verified) bi nhiem du lieu (contamination) va chua phan anh do phuc tap thuc te cua software engineering cong nghiep. 161/500 task trong SWE-Bench Verified chi can sua 1-2 dong code — qua don gian so voi thuc te.

## 2. Dong co / Gap
- Benchmark cu dung repo open-source (MIT/Apache) → de bi lan vao training data cua LLM
- Task qua don gian, khong doi hoi multi-file editing
- Thieu task tu codebase thuong mai/enterprise thuc te
- Chua co co che chong contamination hieu qua

## 3. Phuong phap (Method)
- Thu thap 1,865 problems tu 41 repo (public GPL + commercial startup repos)
- Chia 3 tap: Public (731), Commercial (276), Held-out (858)
- Human-centered augmentation: them requirements + interface specs cho moi task
- Contamination-resistant: dung copyleft license (GPL) + proprietary repos
- Docker-based environments cho Python, JS/TS, Go

## 4. Dong gop chinh (Contributions)
- Benchmark moi 1,865 tasks phuc tap hon SWE-Bench (trung binh 107.4 LOC, 4.1 files)
- Chien luoc chong contamination bang copyleft + commercial repos
- Human augmentation workflow 3 buoc dam bao resolvability
- Phan tich failure modes chi tiet bang LLM-as-a-judge
- Commercial set dau tien trong coding agent benchmark

## 5. Diem manh (Strengths)
- Contamination-resistant design rat tot (GPL + held-out + commercial)
- Task phuc tap, sat thuc te cong nghiep (multi-file, multi-language)
- Phan tich failure mode rat chi tiet (Table 4) — phan biet Wrong Solution, Tool-Use, Syntax Error, Incorrect File
- Human verification dam bao chat luong
- Da ngon ngu: Python, JS, TS, Go

## 6. Han che (Limitations)
- Phan bo ngon ngu khong deu (thieu Java, C++, Rust)
- Chi dua vao test suite (fail2pass/pass2pass) — khong danh gia code quality, security, maintainability
- Commercial set khong public — kho tai hien ket qua
- Chi dung SWE-Agent scaffold — ket qua co the khac voi scaffold khac
- Chua co evaluation cho collaborative/multi-agent scenarios

## 7. Dataset & Metric
- **Dataset:** SWE-Bench Pro (1,865 tasks, 41 repos)
- **Metric:** Pass@1 (resolve rate)
- **Scaffold:** SWE-Agent

## 8. Ket qua chinh
- Best model: Claude Sonnet 4.5 = 43.6%, Claude Sonnet 4 = 42.7% (public set)
- Commercial set: Claude Opus 4.1 = 17.8%, GPT-5 = 15.7% (kho hon nhieu)
- So voi SWE-Bench Verified (~70%+), SWE-Bench Pro chi dat <45% → phuc tap hon
- Failure modes: Opus 4.1 chu yeu sai ve semantic (Wrong Solution 50.3%), Sonnet 4 bi context overflow (35.6%)

## 9. Keywords
`SWE-bench` `coding-agent-evaluation` `benchmark` `contamination` `enterprise` `multi-file` `failure-analysis`

## 10. Lien quan den de tai
Truc tiep lien quan — cho thay benchmark hien tai chua du tot de danh gia coding agent. Gap: can framework danh gia toan dien hon (khong chi test-based), can benchmark cho multi-agent va harness-level evaluation.
