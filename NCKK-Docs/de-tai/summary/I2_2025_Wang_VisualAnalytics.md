# [2025] Wang et al. — Illuminating LLM Coding Agents: Visual Analytics

## Metadata
- **arXiv:** 2508.12555
- **Venue:** IEEE TVCG (submitted)
- **Year:** 2025
- **Authors:** Junpeng Wang, Yuzhong Chen, Menghai Pan, Chin-Chia Michael Yeh, Mahashweta Das (Visa Research)

## 1. Van de (Problem)
Coding agents tu dong sinh code nhung ML scientists kho theo doi qua trinh iterative. Kiem tra thu cong tung output khong hieu qua, kho phat hien loi lap lai va lang phi tai nguyen.

## 2. Dong co / Gap
- Cong cu visualization hien tai (AIDE) chi hien thi cay co ban, thieu phan tich sau
- Chua co visual analytics chuyen biet cho coding agents
- Can so sanh code-level, process-level, va LLM-level nhung khong co tool phu hop

## 3. Phuong phap (Method)
He thong visual analytics 3 cap voi 4 views:
1. Code-Level: Tree View + Code View (AST-based functional similarity)
2. Process-Level: Clustering solution-trees bang tree-edit distance
3. LLM-Level: Projection View (t-SNE/PCA/UMAP) + Package View

## 4. Dong gop chinh (Contributions)
- He thong visual analytics dau tien cho coding agents
- Framework 3 cap (Code/Process/LLM) generalizable
- Phat hien: agent lap lai bug, lang phi compute, greedy policy bi ket local minimum
- AST-based code similarity loai bo cosmetic differences

## 5. Diem manh (Strengths)
- Giai quyet van de thuc te cua ML scientists
- AST-based similarity thong minh
- Case study chi tiet: 5 LLMs, 100 solution-trees, 3000 code snippets
- Phat hien "repeated bug" va "wasted computation" co gia tri cao
- Generalizable cho tree-based frameworks khac

## 6. Han che (Limitations)
- Chi test tren AIDE (tree-based), chua thu chain-based frameworks
- Chi ML/Kaggle tasks, chua test SE tasks
- User study voi 5 experts — mau nho
- Chua tich hop auto anomaly detection

## 7. Dataset & Metric
- 24 Kaggle competitions, 5 LLMs x 20 runs x 30 nodes = 3000 snippets
- RMSE, tree-edit distance, AST similarity

## 8. Ket qua chinh
- LLM3 nhieu buggy code nhat, thieu linh hoat package
- Agent lap lai bug xgboost qua nhieu iterations (thieu persistent memory)
- Lang phi compute do sinh code trung lap chuc nang
- Greedy policy de bi ket local minimum

## 9. Keywords
`visual-analytics` `coding-agent` `AIDE` `solution-tree` `AST-similarity` `LLM-evaluation`

## 10. Lien quan den de tai
Lien quan agent evaluation — visual method de hieu hanh vi coding agent. Phat hien: thieu memory dan den lap bug, lang phi compute. Insights co the cai thien harness design.
