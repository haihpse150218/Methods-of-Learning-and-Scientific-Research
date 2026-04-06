# [2024] Wang — Chain-of-Thought Reasoning without Prompting

## Metadata
- **arXiv:** 2402.10200
- **Venue:** arXiv preprint (Google DeepMind)
- **Year:** 2024
- **Authors:** Xuezhi Wang, Denny Zhou

## 1. Van de (Problem)
Eliciting chain-of-thought (CoT) reasoning from LLMs has relied on carefully crafted prompts (few-shot demonstrations or zero-shot instructions like "Let's think step by step"). These prompting techniques encode task-specific human priors, making it hard to assess the model's intrinsic reasoning ability. The question remains: can LLMs reason effectively without any prompting at all?

## 2. Dong co / Gap
All prior work on CoT reasoning requires either prompt engineering (few-shot CoT, zero-shot CoT) or model finetuning with CoT-annotated data. No existing method explores whether CoT reasoning paths already exist naturally within the model's decoding space. This paper discovers that CoT paths are inherently present among the top-k alternative tokens at the first decoding step, but are hidden by the dominant greedy decoding strategy.

## 3. Phuong phap (Method)
**CoT-decoding** is a task-agnostic decoding modification:

1. **Explore alternative top-k tokens at the first decoding step:** Instead of greedy decoding (always taking top-1 token), examine k alternative tokens (default k=10) at the very first position, then continue with greedy decoding for each path.

2. **Select the best path using answer confidence (Delta):** For each decoding path, compute the confidence metric Delta_k,answer = average probability gap between the top-1 and top-2 tokens across the answer span. Paths with CoT reasoning exhibit significantly higher Delta (higher confidence in the final answer).

3. **Aggregation:** Instead of just taking the max-Delta path, aggregate answers across all k paths using a weighted scheme: for each candidate answer a, compute Delta_a = sum of Delta_k,a across all paths leading to answer a. Select the answer with the highest aggregated Delta.

The input uses a minimal "Q: [question]\nA:" format with no CoT instructions or demonstrations.

## 4. Dong gop chinh (Contributions)
- Discovery that pre-trained LLMs inherently possess CoT reasoning paths in their decoding space, hidden by greedy decoding -- a fundamental finding about model capabilities.
- CoT-decoding: a task-agnostic, unsupervised method to elicit reasoning without any prompting or finetuning, by simply exploring alternative first tokens.
- Answer confidence metric (Delta) that reliably distinguishes CoT paths from non-CoT paths (88% correlation on GSM8K).
- Demonstration that CoT-decoding partially closes the gap between pre-trained and instruction-tuned models without using any supervised data.
- CoT-decoding can be combined with CoT prompting for further gains (e.g., Mistral-7B: 17.5% zero-shot CoT --> 48.4% with CoT-decoding + zero-shot CoT on GSM8K).

## 5. Diem manh (Strengths)
- Entirely unsupervised and task-agnostic: no prompt engineering, no finetuning, no task-specific demonstrations needed.
- Reveals a fundamental insight about LLM capabilities: reasoning is inherent but obscured by greedy decoding.
- Works across multiple model families (PaLM-2, Mistral-7B, Gemma-7B) and scales (XS to Large).
- Complementary to existing prompting techniques: combining CoT-decoding with zero-shot CoT yields further improvements.
- Computationally tractable: only requires k forward passes (k=10), comparable to self-consistency but more effective.

## 6. Han che (Limitations)
- Requires access to model logits (token probabilities), so cannot be applied to black-box API models like GPT-4.
- CoT paths become less prevalent as task complexity increases (multi-step arithmetic with 3+ steps, highly synthetic tasks).
- Currently only branches at the first decoding step; branching at later positions could yield more paths but at much higher computational cost.
- The Delta confidence metric relies on identifiable answer spans, which may be less precise for open-ended generation tasks.
- Does not address generation tasks (only reasoning with definite answers).

## 7. Dataset & Metric
| Dataset | Task Type | Metric |
|---------|-----------|--------|
| GSM8K | Grade-school math | Accuracy |
| MultiArith | Multi-step arithmetic | Accuracy |
| Year Parity | Commonsense reasoning | Accuracy |
| Coin Flip | Symbolic reasoning | Accuracy |
| Web of Lies | Symbolic reasoning (Big-Bench-Hard) | Accuracy |
| Multi-step Arithmetic | Symbolic reasoning (Big-Bench-Hard) | Accuracy |
| Sports Understanding | Natural language (Big-Bench) | Accuracy |
| Object Counting | Natural language (Big-Bench) | Accuracy |

Models: PaLM-2 (XS, S, M, L, Inst-tuned), Mistral-7B (pre-trained + inst-tuned), Gemma-7B.

## 8. Ket qua chinh
- **GSM8K (Mistral-7B):** Greedy 9.9% --> CoT-decoding **25.1%** (+153% relative). Outperforms self-consistency without CoT prompt (12.9%) by a large margin.
- **GSM8K (PaLM-2 Large):** Greedy 34.8% --> CoT-decoding **63.2%** (+82% relative). Pre-trained model with CoT-decoding (63.2%) approaches instruction-tuned model with greedy decoding (67.8%).
- **Year Parity (PaLM-2 Large):** Greedy 57.0% (near chance) --> CoT-decoding **95.0%** (near perfect).
- **CoT-decoding is the only decoding strategy that works:** Top-k sampling (4.9%), nucleus sampling (6.4%), beam search (6.7%), temperature sampling (7.5%) all perform worse than greedy (9.9%) on GSM8K with Mistral-7B.
- **Combined with zero-shot CoT prompting:** Mistral-7B reaches 48.4% on GSM8K; PaLM-2 L reaches 87.0%.
- **Path extraction:** CoT-decoding using answer confidence selects CoT paths far more reliably than ranking by log-probability (72.0% vs. 37.0% on GSM8K) or length-normalized log-prob (51.0%).
- **Scaling with k:** Performance generally improves with larger k, with diminishing returns after k=10.

## 9. Keywords
Chain-of-Thought, decoding, reasoning without prompting, top-k tokens, answer confidence, intrinsic reasoning, CoT-decoding, test-time compute, greedy decoding

## 10. Lien quan den de tai
CoT-decoding is relevant to coding agent harness design in several ways. First, it demonstrates that test-time compute scaling (exploring alternative decoding paths) can substantially improve reasoning -- a principle directly applicable to coding agents where exploring multiple solution approaches improves success rates. Second, the answer confidence metric (Delta) provides a signal for selecting the most reliable reasoning path, analogous to using test results or compilation feedback to select the best code patch in a coding harness. Third, the finding that reasoning capability is inherent but hidden by greedy decoding suggests that coding agent harnesses should explore diverse generation strategies rather than relying on single greedy completions. The method complements tree search approaches (G4_Koh) by operating at the token level rather than the action level.
