# HarnessEval v2 — Kịch bản thuyết trình

> **Đề tài:** HarnessEval — Đánh giá hạ tầng Coding Agent thông qua phân tích ablation đa chiều
> **Trường:** FPT School of Business and Technology (FSB)
> **Slide:** `slide-HarnessEval-v2-en.pptx` / `slide-HarnessEval-v2-en.pdf` (19 slides)
> **Tổng thời lượng dự kiến:** 18 phút thuyết trình + 7 phút Q&A
> **Ngôn ngữ:** Tiếng Việt (giữ nguyên thuật ngữ kỹ thuật tiếng Anh)

---

## Tổng quan kịch bản

| Slide | Chủ đề | Thời lượng | Người nói (gợi ý) |
|------:|--------|-----------:|-------------------|
| 1 | Title | 0:30 | MC mở đầu |
| 2 | Research Team | 0:30 | MC giới thiệu nhóm |
| 3 | Outline | 0:45 | MC dẫn dắt |
| 4 | Problem | 1:30 | Nói chính #1 |
| 5 | Research Gap | 1:30 | Nói chính #1 |
| 6 | Gap Table | 0:45 | Nói chính #1 |
| 7 | Aim + Objectives | 1:30 | Nói chính #2 |
| 8 | Hypotheses | 1:00 | Nói chính #2 |
| 9 | Taxonomy 7 metrics | 1:30 | Nói chính #2 |
| 10 | Modular Harness | 1:15 | Nói chính #3 |
| 11 | Methodology | 1:00 | Nói chính #3 |
| 12 | Ablation Design | 1:00 | Nói chính #3 |
| 13 | ANOVA 2-chiều | 1:15 | Nói chính #4 |
| 14 | Threats & Risks | 1:00 | Nói chính #4 |
| 15 | Timeline & Budget | 0:45 | Nói chính #4 |
| 16 | Implementation Status | 1:00 | Nói chính #5 |
| 17 | Preliminary Results | 1:15 | Nói chính #5 |
| 18 | Contributions | 0:45 | Nói chính #5 kết bài |
| 19 | Q&A | 0:15 mở | — |
| **Tổng** | | **~18 phút** | |

**Quy ước ký hiệu:**
- 🎯 = ý chính cần nhớ
- 💬 = câu nói gợi ý
- 👉 = chuyển slide
- ⚠️ = điểm cẩn thận / dễ bị hỏi

---

## SLIDE 1 — Title (0:30)

🎯 **Mục tiêu:** Mở đầu chuyên nghiệp, giới thiệu tên đề tài.

💬 **Lời mở:**
> "Kính chào quý thầy cô và hội đồng. Em xin được trình bày đề tài nghiên cứu khoa học của nhóm chúng em: **HarnessEval — Đánh giá hạ tầng Coding Agent thông qua phân tích ablation đa chiều trên nhiều mô hình ngôn ngữ lớn**."
>
> "Đây là đề tài thuộc môn Phương pháp học tập và Nghiên cứu khoa học, trường FPT School of Business and Technology. Phiên bản này là v2, đã chỉnh sửa sau vòng phản biện đầu tiên của hội đồng."

👉 *Chuyển slide:* "Trước khi đi vào nội dung, em xin giới thiệu thành viên nhóm."

---

## SLIDE 2 — Research Team (0:30)

🎯 **Mục tiêu:** Giới thiệu giảng viên hướng dẫn và 5 thành viên.

💬 **Lời nói:**
> "Đề tài được thực hiện dưới sự hướng dẫn của **[Tên thầy/cô]**, giảng viên trường FSB. Nhóm chúng em gồm 5 thành viên: Lê Lâm Vĩnh, Hoàng Phi Hải, Đỗ Hoàng Tỷ Phú, Trịnh Hữu Tuấn và Trần Quang Tuấn."

👉 *Chuyển slide:* "Sau đây em xin trình bày phần mục lục bài thuyết trình."

---

## SLIDE 3 — Outline (0:45)

🎯 **Mục tiêu:** Cho hội đồng biết flow để dễ theo dõi.

💬 **Lời nói:**
> "Bài thuyết trình của em gồm 14 phần. Bốn phần đầu sẽ làm rõ **vấn đề và research gap** mà đề tài giải quyết. Tiếp theo từ phần 5 đến phần 9 là **phương pháp luận** — bao gồm taxonomy, kiến trúc modular harness, và mô hình thống kê ANOVA. Phần 10 đến 14 là **kế hoạch thực hiện và kết quả sơ bộ** mà nhóm em đã đạt được. Cuối cùng là phần Q&A."
>
> "Một điểm em muốn nhấn mạnh: nhóm chúng em **đã triển khai code và có kết quả thực nghiệm sơ bộ** — em sẽ trình bày ở slide 12 và 13."

👉 *Chuyển slide:* "Bắt đầu với phần đầu tiên — đặt vấn đề."

---

## SLIDE 4 — Problem: The Evaluation Paradox (1:30)

🎯 **Mục tiêu:** Hội đồng phải hiểu *coding agent* gồm 2 phần và *paradox* hiện tại.

💬 **Lời nói:**
> "Hiệu suất của một coding agent — như Claude Code, Cursor hay SWE-Agent — phụ thuộc vào hai yếu tố hoàn toàn khác nhau."
>
> "Yếu tố thứ nhất là **base LLM** — đây là Claude, GPT, DeepSeek. Cộng đồng đã có rất nhiều benchmark đánh giá các mô hình này: SWE-bench, HumanEval, MMLU..."
>
> "Yếu tố thứ hai là **harness** — hay còn gọi là *scaffold*. Đây là toàn bộ phần xung quanh model: tool system cho phép agent đọc file, chạy bash; context manager quản lý lịch sử hội thoại; orchestration logic điều khiển vòng lặp agent. Bui và cộng sự năm 2026 gọi đây là *'hệ điều hành cho agent'*."
>
> "Bằng chứng cho thấy harness **rất quan trọng**: Lou và cộng sự năm 2026 đã chứng minh rằng *một model nhỏ với harness tốt có thể vượt một model lớn với harness yếu*, đồng thời giảm 100% các hành động bất hợp lệ. Bui và cộng sự cho thấy kỹ thuật Adaptive Context Compaction giúp giảm 54% lượng token sử dụng — đây là con số cực kỳ lớn."
>
> "**Vậy nghịch lý ở đâu?** Khi một paper báo cáo *'Agent A đạt 70% trên SWE-bench'*, chúng ta hoàn toàn **không biết** component nào của harness đã đóng góp vào con số đó. Là tool system tốt? Là context manager? Hay đơn giản chỉ là model tốt? Không ai trả lời được."

⚠️ **Có thể bị hỏi:** "Tại sao điều này quan trọng?" → Trả lời: "Vì developer cần biết nên đầu tư cải thiện cái gì. Nếu không tách được, chúng ta đang tối ưu mù."

👉 *Chuyển slide:* "Tại sao gap này tồn tại đến giờ chưa ai giải quyết? Có ba lý do."

---

## SLIDE 5 — Research Gap: Three Genuine Reasons (1:30)

🎯 **Mục tiêu:** Phòng ngừa câu hỏi *"Tại sao chưa ai làm? Có phải gap giả không?"*

💬 **Lời nói:**
> "Đây là câu hỏi mà nhóm chúng em đã được hội đồng hỏi trong vòng phản biện đầu tiên. Em xin được trả lời chi tiết."
>
> "Nhóm em đã phân tích **49 papers** từ năm 2023 đến 2026, và xác nhận: **không có công trình nào đánh giá bản thân harness một cách hệ thống**. Có ba lý do chính:"
>
> "**Thứ nhất — vai trò khác nhau.** Princeton xây SWE-Agent, Anthropic xây Claude Code. Họ là *developers* — có incentive ra harness mới, không phải *evaluators* so sánh các hệ thống. Giống như Toyota và Honda sản xuất xe, nhưng người đánh giá an toàn lại là Euro NCAP, IIHS — các tổ chức độc lập. Cộng đồng coding agent thiếu vai trò evaluator độc lập này."
>
> "**Thứ hai — lĩnh vực phát triển quá nhanh.** Từ 2023 đến 2026, số lượng coding agent tăng từ vài hệ thống lên hàng chục. Mọi người đang chạy đua xây dựng, chưa ai dừng lại để meta-evaluate."
>
> "**Thứ ba — chỉ có bằng chứng gián tiếp.** Lou và cộng sự đã so sánh harness — nhưng trên *game tasks*, không phải coding. Robeyns và cộng sự với SICA tự cải thiện harness từ 17% lên 53% trên SWE-bench — nhưng họ *không đo từng component*."
>
> "Tóm lại: research gap này hoàn toàn *thật sự*, không phải gap nhân tạo."

⚠️ **Câu hỏi tiềm năng:** "Vậy tại sao Anthropic không tự đánh giá Claude Code?" → "Vì họ không có incentive so sánh với đối thủ. Họ ưu tiên ship feature."

👉 *Chuyển slide:* "Em xin trình bày bảng tổng hợp cụ thể những gì đã có và chưa có."

---

## SLIDE 6 — Gap Table (0:45)

🎯 **Mục tiêu:** Visual hóa gap để hội đồng "thấy" rõ.

💬 **Lời nói:**
> "Bảng này tổng hợp 6 khía cạnh."
>
> "Đo *output* của agent — đã có rất nhiều: SWE-bench, SWE-Compass, AgentBoard."
>
> "Đo tool accuracy *riêng lẻ* — đã có ToolLLM, AnyTool, Gorilla. Nhưng **đo tool TRONG harness coding** thì chưa ai làm."
>
> "Đo memory *riêng lẻ* — Mem0, A-MEM, nhưng chỉ trên chatbot. **Đo memory TRONG harness coding** chưa có."
>
> "Hai dòng cuối em muốn nhấn mạnh — màu đỏ: **so sánh cross-backend** và **tách biệt harness vs LLM**. Cả hai đều *hoàn toàn chưa ai làm*. Đây là vùng trắng mà đề tài chúng em sẽ lấp."

👉 *Chuyển slide:* "Đó là gap. Bây giờ em trình bày mục tiêu cụ thể của đề tài."

---

## SLIDE 7 — Aim + 5 Objectives (1:30)

🎯 **Mục tiêu:** Hội đồng nhớ được aim + 5 objectives đo được.

💬 **Lời nói:**
> "Mục đích nghiên cứu của đề tài: *xây dựng khung đánh giá tổng hợp đầu tiên cho hạ tầng coding agent, cho phép phân tách và định lượng đóng góp của từng thành phần harness, độc lập với base LLM*."
>
> "Cụm từ *'tổng hợp đầu tiên'* — em xin nhấn mạnh — là điều chỉnh từ vòng v1. V1 nói *'đầu tiên'* nhưng không chính xác, vì từng khía cạnh đã có người nghiên cứu riêng lẻ. V2 sửa thành *'tổng hợp đầu tiên'* — tức là *gom lại trong một framework thống nhất*."
>
> "5 mục tiêu cụ thể:"
> - "**O1** — Xây taxonomy 3 chiều, 7 metrics, validate bởi 5 chuyên gia. Tiêu chí: Fleiss kappa từ 0.6 trở lên."
> - "**O2** — Fork và refactor SWE-Agent thành modular harness. Tiêu chí: resolve rate sai lệch không quá ±3% so với SWE-Agent gốc."
> - "**O3** — Ablation study với 150 task × 27 conditions, có pilot study. Tổng 7,050 evaluations."
> - "**O4** — Phân tích ANOVA 2-chiều với p < 0.05 sau hiệu chỉnh Bonferroni."
> - "**O5** — Phát hành toolkit open-source trên GitHub."
>
> "Những thay đổi từ v1: giảm 5 chiều xuống còn 3, giảm 80 conditions xuống 27, thêm pilot study, thêm ANOVA 2-chiều — đều theo phản biện của hội đồng."

👉 *Chuyển slide:* "Đề tài có 4 giả thuyết để kiểm chứng."

---

## SLIDE 8 — Hypotheses H1–H4 (1:00)

🎯 **Mục tiêu:** Hội đồng thấy hypotheses *trung tính*, không confirmation bias.

💬 **Lời nói:**
> "Bốn giả thuyết được phát biểu *trung tính*, có thể kiểm chứng:"
>
> "**H1** — Tool system có effect size lớn nhất, Cohen's d > 0.5."
>
> "**H2** — Context management có effect size trung bình, d từ 0.3 đến 0.5."
>
> "**H3** — Harness configuration giải thích ít nhất 20% variance của resolve rate."
>
> "**H4** — Variance giữa các LLM backends *giảm* khi harness chất lượng cao hơn — tức là có *interaction effect*."
>
> "Một điểm em muốn nhấn mạnh: nhóm chúng em **không dự đoán con số cụ thể** kiểu *'30 đến 40%'*. V1 từng có cách phát biểu này và bị hội đồng phê bình là *confirmation bias*. V2 chỉ nêu *hướng* có thể kiểm chứng. Dù H được ủng hộ hay bị bác bỏ — cả hai đều là **đóng góp khoa học**."

👉 *Chuyển slide:* "Bây giờ em trình bày taxonomy 3 chiều với 7 metrics."

---

## SLIDE 9 — Taxonomy: 3 Dimensions, 7 Metrics (1:30)

🎯 **Mục tiêu:** Hội đồng hiểu mỗi metric đo cái gì và validate ra sao.

💬 **Lời nói:**
> "Taxonomy gồm 3 chiều, mỗi chiều 2-3 metrics, tổng 7 metrics."
>
> "**Chiều 1 — Tool Dispatch.** Đo việc agent dùng tool có hiệu quả không."
> - "M1.1 *Correct Selection Rate* — phần trăm tool calls chọn được tool phù hợp. Điểm quan trọng: chúng em **không** so với một *single ground truth* — đây là sửa đổi sau câu hỏi #4 của hội đồng. Thay vào đó, dùng *acceptable tool set* — tức là tập các tool có thể chấp nhận được — và đo agreement giữa 2 annotators bằng Fleiss kappa."
> - "M1.2 *Redundant Call Rate* — phần trăm tool calls mà output không được dùng trong 3 turns sau."
> - "M1.3 *Utilization Breadth* — số lượng tool types được dùng trên tổng số tools available."
>
> "**Chiều 2 — Context Utilization.**"
> - "M2.1 *Info Retention* — đo bằng BERTScore giữa output với full context và output với context đã compact, trên cùng một task."
> - "M2.2 *Effective Token Ratio* — phần trăm tokens trong context có liên quan đến task hiện tại. Đây là metric mà v1 nói mơ hồ là *'token waste'* — câu hỏi #9 của hội đồng. V2 sửa thành: dùng *LLM classifier* (Claude Haiku) phân loại từng segment, sau đó validate accuracy của classifier trên 200 segments với human labels."
>
> "**Chiều 3 — Backend Portability.**"
> - "M3.1 — Standard deviation của resolve rate qua 3 LLM backends."
> - "M3.2 — Tỷ lệ min over max."

⚠️ **Câu hỏi tiềm năng:** "Tại sao 7 metrics chứ không phải 5 hay 11?" → "V1 có 11 metrics, hội đồng yêu cầu giảm scope. V2 giữ những metrics có thể đo được tự động hoặc validate được rõ ràng."

👉 *Chuyển slide:* "Để đo được 7 metrics này, chúng em cần một harness có thể swap component được."

---

## SLIDE 10 — Modular Harness Architecture (1:15)

🎯 **Mục tiêu:** Hội đồng hiểu kiến trúc 3 layer và lý do fork SWE-Agent.

💬 **Lời nói:**
> "Để chạy ablation study, chúng em cần một harness mà mỗi layer có thể *swap* qua config. Đây là kiến trúc 3 layers:"
>
> "**Layer 1 — Tool Dispatch.** Có 3 mức: Full với 12 tools, Medium với 8, Minimal với 5. Quan trọng: minimal là *subset* của medium, medium là *subset* của full — tức là *gradual reduction*, không phải tắt ngẫu nhiên. Điều này tránh confounding."
>
> "**Layer 2 — Context Management.** Ba strategy: Full History không cắt, Sliding Window 50K tokens, và Summary/ACC chỉ giữ 2K tokens."
>
> "**Layer 3 — LLM Backend.** Ba mô hình: Claude Sonnet 4, GPT-4o, DeepSeek-V3. Tất cả set temperature = 0 để tránh non-determinism."
>
> "L4 và L5 — Safety và Orchestration — em để mờ vì là *future work*. L5 chúng em giữ nguyên từ SWE-Agent gốc."
>
> "Về kỹ thuật: chúng em dùng *Strategy Pattern + Dependency Injection + Factory Pattern*. Mỗi layer được swap qua YAML config. Việc fork SWE-Agent thay vì tự xây — giảm rủi ro: SWE-Agent có sẵn ~15 nghìn LOC, MIT license, đã hoạt động ổn định."

⚠️ **Câu hỏi tiềm năng:** "Vì sao không tự xây harness từ đầu?" → "V1 từng đề xuất tự xây, hội đồng cảnh báo rủi ro vì 6 tháng không đủ. V2 đổi sang fork để có baseline đáng tin cậy."

👉 *Chuyển slide:* "Phương pháp thực hiện gồm 4 giai đoạn."

---

## SLIDE 11 — Methodology: 4 Phases (1:00)

🎯 **Mục tiêu:** Hội đồng thấy có pilot — không cam kết mù.

💬 **Lời nói:**
> "Bốn giai đoạn thực nghiệm:"
>
> "**P1** — Thiết kế taxonomy và validate bởi 5 experts. 6 tuần."
>
> "**P1.5** — *Pilot study*. Đây là giai đoạn **mới** so với v1, theo yêu cầu của hội đồng. 5 conditions × 20 tasks × 2 runs = 200 evaluations, chi phí khoảng 80 đô."
>
> "**P2** — Fork SWE-Agent, refactor modular, verify ±3% trên 50 tasks. 3 tuần."
>
> "**P3** — Full ablation 27 conditions × 150 tasks = 7,050 evaluations. 7 tuần."
>
> "Tại sao cần pilot? Bốn lý do:"
> - "Một, validate xem metrics có *phân biệt được* giữa các conditions hay không. Nếu 2 conditions cho kết quả giống nhau thì merge → giảm scope."
> - "Hai, ước tính chi phí chính xác cho full experiment."
> - "Ba, debug pipeline."
> - "Bốn, tính preliminary effect sizes để power analysis."
>
> "Tóm lại: pilot giúp **không cam kết mù** vào full experiment đắt tiền."

👉 *Chuyển slide:* "Em trình bày chi tiết thiết kế ablation."

---

## SLIDE 12 — Ablation Design (1:00)

🎯 **Mục tiêu:** Show con số cụ thể: 27, 150, 7050, $2.5k.

💬 **Lời nói:**
> "Bốn con số chính: 27 conditions, 150 tasks, 7,050 evaluations, ngân sách khoảng 2,500 đô."
>
> "27 = 3 × 3 × 3 *full factorial*: 3 mức tool, 3 strategy context, 3 backend. Đây là *ablation đầy đủ* — không bỏ sót combination nào."
>
> "Dataset: 150 tasks từ SWE-bench Verified, sample bằng *stratified random sampling* theo độ khó."
>
> "Số runs: 10 conditions quan trọng nhất chạy 3 runs để report mean ± std; 17 conditions còn lại chạy 1 run. Tổng = 10 × 3 + 17 × 1, nhân 150 tasks = 4,500 + 2,550 = 7,050 evaluations."
>
> "Power analysis: với alpha = 0.05 và 150 tasks mỗi condition, power đạt ≥ 0.80."

⚠️ **Câu hỏi tiềm năng:** "Vì sao chỉ có 10 conditions chạy 3 runs?" → "Để cân bằng giữa độ tin cậy và ngân sách. 10 critical conditions là những combination quan trọng nhất theo H1-H4."

👉 *Chuyển slide:* "Cách phân tích thống kê — đây là đóng góp lý thuyết chính."

---

## SLIDE 13 — Two-Way ANOVA (1:15)

🎯 **Mục tiêu:** Hội đồng hiểu cách *tách biệt* harness vs LLM.

💬 **Lời nói:**
> "Đây là phần em muốn nhấn mạnh — câu hỏi #1 của hội đồng vòng v1 là *'làm sao tách biệt harness và LLM?'* Em xin trả lời chi tiết."
>
> "Trước hết, *'độc lập với LLM'* **không có nghĩa** harness và LLM không tương tác. Nó có nghĩa: chúng ta có thể *phân tách* phần variance do harness gây ra với phần variance do LLM gây ra."
>
> "Mô hình thống kê: *Total Variance = Var(Harness) + Var(LLM) + Var(Harness × LLM) + Error*."
>
> "Factor A là *Harness configuration* với 9 levels — tức 3 tool × 3 context. Factor B là *LLM backend* với 3 levels: Claude, GPT, DeepSeek. Biến phụ thuộc là *resolve rate*."
>
> "Cách diễn giải:"
> - "Nếu *Var(Harness)* có ý nghĩa thống kê → harness *có ảnh hưởng độc lập*."
> - "Nếu *Var(H × LLM)* có ý nghĩa → có *interaction*. Tức là: harness tốt cho Claude có thể không tốt cho GPT — đây là điều cần cảnh báo cho cộng đồng."
> - "*eta squared* cho biết phần trăm variance được giải thích bởi mỗi factor."
>
> "Đây là **đóng góp lý thuyết chính** của đề tài: *formalize cách phân tách harness quality khỏi LLM quality*. Trước đây không ai làm việc này."
>
> "Post-hoc: dùng Tukey HSD cho pairwise comparison, Cohen's d cho effect size, Bonferroni correction cho 7 metrics."

⚠️ **Câu hỏi tiềm năng:** "Tại sao two-way thay vì three-way?" → "Vì gộp Tool và Context vào Factor A để giảm complexity. Three-way ANOVA cũng được thực hiện như sensitivity analysis (slide 17)."

👉 *Chuyển slide:* "Em trình bày các threats và risks — yêu cầu của hội đồng."

---

## SLIDE 14 — Threats to Validity & Risks (1:00)

🎯 **Mục tiêu:** Show thinking nghiêm túc về validity.

💬 **Lời nói:**
> "Đây là phần **mới** so với v1 — hội đồng yêu cầu bổ sung."
>
> "Bên trái — *Threats to validity*:"
> - "*Internal — confounding khi tắt tool*: Nếu tắt tool X, performance giảm có thể vì agent mất công cụ, hoặc vì harness dispatch kém. Mitigation: giảm tools theo bậc 12 → 8 → 5, không tắt hoàn toàn; ghi nhận task nào *cần* tool nào."
> - "*Internal — LLM non-determinism*: Set temperature = 0; chạy 3 runs cho critical conditions."
> - "*External — chỉ test Python*: Caution khi generalize sang Java, Go..."
> - "*Construct — M1.1 phụ thuộc annotator*: Dùng 2 annotators, đo Fleiss kappa."
>
> "Bên phải — *Top risks*:"
> - "*Cao*: API cost vượt ngân sách. Mitigation: pilot ước tính trước, dùng DeepSeek rẻ nhất cho nhiều conditions."
> - "*Trung bình*: Docker environment fail. Mitigation: pre-filter, retry × 2."
> - "*Trung bình*: Metrics không phân biệt được giữa conditions. Mitigation: pilot phát hiện sớm."
> - "*Thấp*: DeepSeek API không ổn định. Backup: Qwen2.5-72B."

👉 *Chuyển slide:* "Timeline và ngân sách."

---

## SLIDE 15 — Timeline & Budget (0:45)

🎯 **Mục tiêu:** Show feasibility — 6 tháng, $2.5-3.1k.

💬 **Lời nói:**
> "6 giai đoạn trong 24 tuần — tức 6 tháng. Em đã trình bày 4 phase chính ở slide 11. Hai phase cuối: P4 phân tích và viết luận văn, P5 review và phát hành toolkit."
>
> "Ngân sách: pilot 80 đô, full experiment 2,500 đô, contingency 500 đô. Tổng 2,500 đến 3,100 đô."
>
> "So với v1: v1 ước tính 800-1,200 đô — *không thực tế*. V2 đã tính cả retry và pilot, đồng thời *giảm số evaluations từ 16,000 xuống 7,050* — giảm 56%."

👉 *Chuyển slide:* "Bây giờ em trình bày phần đặc biệt — những gì nhóm em đã làm được."

---

## SLIDE 16 — Implementation Status: ALREADY BUILT (1:00)

🎯 **Mục tiêu:** Show CODE đã chạy được — đây là điểm mạnh nhất.

💬 **Lời nói:**
> "Em xin nhấn mạnh: nhóm chúng em **không chỉ trình bày proposal** — chúng em đã *thực sự code* và có hệ thống chạy được."
>
> "Bốn con số:"
> - "**167 tests** đang pass — toàn bộ test suite."
> - "**9 phases** đã hoàn thành theo kế hoạch coding nội bộ."
> - "**27 conditions** đã được generate đầy đủ."
> - "**360 trajectories** thực nghiệm đã thu thập."
>
> "Toolkit `harness_eval` Python package gồm các module:"
> - "*configs* — định nghĩa 27 conditions."
> - "*metrics* — code 7 metrics M1.1 đến M3.2."
> - "*parsers* — parse SWE-Agent log."
> - "*pipeline analysis* — chạy ANOVA, Cohen's d, GLMM."
> - "*pipeline runner* — chạy được 3 chế độ: dry-run synthetic, real với SWE-Agent, và Ollama local."
> - "*harness module* — implement 3 ABC interfaces với 9 concrete providers."
> - "*CLI* — 5 lệnh: info, pilot, run, analyze, convert."
>
> "Ngoài ra chúng em xây dashboard Streamlit với 5 tab: Config Builder, Run Monitor, Log Viewer, Compare, ANOVA. Hỗ trợ chạy parallel với ThreadPoolExecutor 4 workers. Đã embed 150 tasks SWE-bench Verified với difficulty-aware. Hỗ trợ Ollama local cho test miễn phí."

⚠️ **Có thể bị hỏi demo:** Sẵn sàng mở `streamlit run streamlit_app.py` để demo nếu hội đồng yêu cầu.

👉 *Chuyển slide:* "Vì đã có code chạy được, em xin trình bày kết quả ANOVA sơ bộ."

---

## SLIDE 17 — Preliminary Empirical Results (1:15)

🎯 **Mục tiêu:** Show H1, H2 đã có hướng được ủng hộ.

💬 **Lời nói:**
> "Đây là kết quả ANOVA *thực tế* mà nhóm em đã chạy trên dữ liệu hiện tại."
>
> "Setup: 360 observations, 18 conditions (vì hiện chỉ có 2 backend là claude và sonnet, haiku còn trống)."
>
> "Đọc bảng từ trên xuống:"
> - "**Tool** — eta² = 0.054, F = 10.26, **p < 0.001 ba sao**. Highly significant."
> - "**Context** — eta² = 0.025, F = 4.72, **p = 0.0095 hai sao**. Significant."
> - "Backend — eta² = 0.0025, p = 0.33. Chưa significant — vì chỉ có 2 levels."
> - "Các interaction effects: chưa significant."
>
> "**Quan sát sơ bộ:**"
> - "Hướng của **H1** đã được ủng hộ: Tool có effect lớn nhất (0.054 > Context 0.025)."
> - "Hướng của **H2** đã được ủng hộ: Context có effect trung bình *và có ý nghĩa thống kê*."
> - "Cần thêm dữ liệu cho **H4** vì backend mới có 2 levels."
>
> "**Lưu ý quan trọng:** dữ liệu hiện tại là *realistic dry-run* dựa trên 150 tasks SWE-bench thật, *chưa* phải kết quả từ chạy SWE-Agent thực sự. Kết quả thực nghiệm cuối cùng sẽ có sau Phase P3 — sau khi chúng em chạy đầy đủ 27 conditions với API thật."

⚠️ **Có thể bị hỏi:** "Dry-run khác real ra sao?" → "Dry-run dùng synthetic data với resolve rate gắn với độ khó tasks (easy 75%, hard 30%) — mô phỏng pattern thực tế. Giúp validate pipeline và phát hiện bug trước khi tốn tiền API."

👉 *Chuyển slide:* "Em xin tóm tắt đóng góp."

---

## SLIDE 18 — Contributions & Publishability (0:45)

🎯 **Mục tiêu:** Highlight 3 đóng góp + venues khả thi.

💬 **Lời nói:**
> "Đề tài có 3 loại đóng góp:"
>
> "**Đóng góp lý thuyết** — formalize cách phân tách harness quality khỏi LLM quality qua ANOVA 2-chiều. Đây là điều chưa ai làm."
>
> "**Đóng góp thực nghiệm** — định lượng đóng góp của từng component harness lần đầu tiên."
>
> "**Toolkit** — framework đánh giá có thể tái sử dụng, open-source GitHub, kèm docs và CI/CD."
>
> "Ý nghĩa thực tiễn:"
> - "Developer biết nên ưu tiên cải thiện component nào của harness."
> - "Researcher có framework chuẩn để so sánh harness mới."
> - "Industry có guidelines thiết kế harness dựa trên data."
>
> "Về publishability — nhóm em nhắm tới 4 venues: ICSE 2027 NIER là *strong fit* nhất, vì đây là track New Ideas dành cho research mới về SE và evaluation. Ngoài ra MSR 2027, LLM Agents Workshop ở NeurIPS hoặc ICML, và EMNLP Demo Track."

👉 *Chuyển slide:* "Em xin kết thúc bài thuyết trình tại đây."

---

## SLIDE 19 — Q&A (0:15 mở)

🎯 **Mục tiêu:** Đóng đẹp, mời câu hỏi.

💬 **Lời nói:**
> "Em xin chân thành cảm ơn quý thầy cô và hội đồng đã lắng nghe. Nhóm em sẵn sàng nhận câu hỏi và phản biện."

---

## Phần Q&A — Câu hỏi dự kiến và cách trả lời

### Nhóm 1: Về scope và feasibility

**Q1:** "150 tasks có đủ không? Tại sao không phải 500 hay 1000 như SWE-bench?"

**A:** "Hai lý do. Một, ngân sách: 27 conditions × 150 tasks × ~$0.27 = $1,900 cho full experiment, đã trong giới hạn $2,500-3,100. Nếu tăng lên 500, cost sẽ ×3 → không khả thi 6 tháng. Hai, power analysis: với 150 tasks và alpha 0.05, power đã ≥ 0.80 cho hypotheses chính. Nhiều hơn không cần thiết."

**Q2:** "6 tháng có đủ cho 5 mục tiêu này?"

**A:** "Chúng em đã chia phase rõ ràng: P1 6 tuần, P1.5 2 tuần, P2 3 tuần, P3 7 tuần, P4-5 6 tuần. Quan trọng: nhóm em **đã code xong toolkit** — tức là P2 đã hoàn thành phần lớn. Nếu không có toolkit này thì 6 tháng có thể không đủ."

### Nhóm 2: Về phương pháp luận

**Q3:** "Tại sao two-way ANOVA chứ không phải three-way?"

**A:** "Em đã có sensitivity analysis với three-way. Two-way là *primary analysis* để giảm complexity và tăng statistical power. Hội đồng có thể xem chi tiết ở slide 17."

**Q4:** "Single ground truth vs acceptable set — chứng minh acceptable set tốt hơn ra sao?"

**A:** "Single ground truth có vấn đề: nhiều task có nhiều cách giải hợp lý. Ví dụ với task 'tìm bug', dùng `grep` hay dùng `find` đều acceptable. Single ground truth sẽ phạt sai. Chúng em dùng 2 annotators định nghĩa *acceptable set* cho từng task, đo Fleiss kappa để đảm bảo đồng thuận."

**Q5:** "BERTScore cho M2.1 có đủ chính xác không?"

**A:** "BERTScore là metric chuẩn trong NLP, đã được validate. Chúng em còn validate thêm bằng 30 cặp human preference để đảm bảo BERTScore correlate với human judgment."

### Nhóm 3: Về tách biệt harness vs LLM

**Q6:** "Làm sao biết harness *thực sự* độc lập với LLM?"

**A:** "Đây chính là câu hỏi #1 của hội đồng vòng v1. Em đã trả lời ở slide 13: *'độc lập'* nghĩa là *có thể decompose variance*, không phải *uncorrelated*. ANOVA cho biết phần trăm variance do harness vs do LLM. Nếu Var(H × LLM) significant → có interaction → harness *không* hoàn toàn độc lập, và chúng em sẽ báo cáo điều này — đây cũng là kết quả khoa học có giá trị."

### Nhóm 4: Về threats

**Q7:** "Confounding khi tắt tool — mitigation có thực sự work không?"

**A:** "Đây là threats chính. Mitigation gồm 3 lớp: (1) giảm dần 12→8→5 thay vì tắt random, đảm bảo minimal ⊂ medium ⊂ full; (2) ghi nhận task nào cần tool nào — nếu task cần tool đã bị tắt, loại khỏi phân tích component đó; (3) report kết quả cả khi *include* và *exclude* các edge cases — sensitivity analysis."

**Q8:** "Chỉ Python — kết quả có generalize sang Java/Go không?"

**A:** "Em đã nêu ở Threats to External Validity. Câu trả lời thẳng: *không generalize trực tiếp*. Tool system Python (pytest, pip) khác Java (maven, junit). Chúng em sẽ ghi rõ trong limitation. Future work: extend sang Java sau khi framework đã được validate."

### Nhóm 5: Về kết quả sơ bộ

**Q9:** "Dry-run khác real ra sao? Tại sao tin được kết quả sơ bộ?"

**A:** "Dry-run của chúng em không random — mà dùng *realistic synthetic data*: 150 tasks thật từ SWE-bench Verified, resolve rate gắn với độ khó (easy 75%, medium 55%, hard 30%, expert 15%) — mô phỏng pattern thực tế. Mục đích: validate pipeline + power analysis. Em **không** claim kết quả sơ bộ là kết quả cuối — em chỉ nói *hướng* H1, H2 đã được dữ liệu mô phỏng *ủng hộ*. Kết quả cuối sẽ có sau P3."

**Q10:** "Vì sao haiku trống?"

**A:** "Haiku là model nhỏ, generate dry-run đang được tiến hành. Trong 1-2 tuần tới sẽ có đủ 3 backends để chạy three-way ANOVA full."

### Nhóm 6: Về toolkit

**Q11:** "Toolkit khác gì SWE-Agent gốc?"

**A:** "SWE-Agent gốc là *single configuration* — không cho phép swap component dễ dàng. Chúng em refactor thành *modular*: 3 layer ABC + 9 concrete provider + factory pattern, mỗi layer swap qua YAML. Ngoài ra thêm metrics layer (7 metrics chưa có), parser, dashboard, CLI."

**Q12:** "Có thể demo không?"

**A:** "Có ạ. Em mở dashboard ngay được — `streamlit run streamlit_app.py`." *(Sẵn sàng mở terminal nếu cần.)*

---

## Mẹo trình bày

### Trước thuyết trình
- [ ] Test slide trên máy chiếu của trường (resolution, font Segoe UI)
- [ ] In sẵn script này (giấy A4) làm tham khảo
- [ ] Chuẩn bị laptop với dashboard Streamlit chạy sẵn (cho slide 16)
- [ ] Có sẵn link GitHub repo (nếu có) để hiển thị
- [ ] Test PDF backup nếu PowerPoint lỗi

### Trong thuyết trình
- **Tốc độ:** ~140 từ/phút (chậm hơn nói chuyện thường)
- **Ngắt câu:** sau mỗi ý chính, ngắt 1-2 giây
- **Eye contact:** quét qua hội đồng, không chỉ nhìn slide
- **Tay:** chỉ vào slide khi cần highlight (slide 6, 9, 17)
- **Khi quên:** im lặng 2 giây, xem slide, tiếp tục — đừng "ờ ừm"

### Thời gian
- Set timer trên điện thoại 18 phút
- Slide 4-13 là core — dành thời gian nhất
- Slide 16-17 là *kill point* — show off code đã chạy được

### Chia phần (gợi ý)
- **MC mở/kết:** slide 1-3, 18-19
- **Speaker 1 (vấn đề):** slide 4-6
- **Speaker 2 (mục tiêu + taxonomy):** slide 7-9
- **Speaker 3 (phương pháp):** slide 10-13
- **Speaker 4 (kết quả + plan):** slide 14-17

5 thành viên có thể chia: MC + 4 speaker chính. Hoặc chia khác tuỳ thoả thuận.

---

## Checklist trước ngày bảo vệ

- [ ] Điền tên thầy hướng dẫn vào slide 2 (đang là placeholder)
- [ ] Confirm chia phần thuyết trình giữa 5 thành viên
- [ ] Test PowerPoint trên máy chiếu thực tế
- [ ] Backup PDF + USB
- [ ] In script (bản này) cho từng người
- [ ] Tập thuyết trình chạy thử full ít nhất 2 lần
- [ ] Chuẩn bị câu trả lời cho 12 câu hỏi dự kiến ở trên
- [ ] Mở sẵn dashboard Streamlit + terminal có toolkit
- [ ] Trang phục: smart casual (áo sơ mi)
- [ ] Đến sớm 15 phút để test thiết bị

---

**Chúc nhóm bảo vệ thành công!** 🎯
