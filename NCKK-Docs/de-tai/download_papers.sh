#!/bin/bash
PAPERS_DIR="/d/MSA-FPT/Methods of Learnning and scientific research/NCKK-Docs/de-tai/papers"
cd "$PAPERS_DIR"

# All 50 papers arXiv IDs with short names
declare -A PAPERS=(
  # A. Harness & Architecture
  ["A1_2026_Bui_OpenDev"]="2603.05344"
  ["A2_2026_Lou_AutoHarness"]="2603.03329"
  ["A3_2026_Cao_LongContext"]="2603.20432"
  # B. Multi-Agent Coding
  ["B1_2026_Lyu_TheBotCompany"]="2603.25928"
  ["B2_2026_Loose_FuzzHarness"]="2603.08616"
  ["B3_2026_Chen_ToolToTeammate"]="2603.27440"
  ["B4_2025_ALMAS"]="2510.03463"
  ["B5_2025_Xiong_KGACG"]="2510.19868"
  ["B6_2025_MOSAIC"]="2510.08804"
  ["B7_2025_Liu_LessonL"]="2505.23946"
  ["B8_2025_XLCoGen"]="2509.19918"
  ["B9_2025_MACOG"]="2510.03902"
  ["B10_2025_Robeyns_SICA"]="2504.15228"
  # C. Evaluation & Benchmarks
  ["C1_2025_Deng_SWEBenchPro"]="2509.16941"
  ["C2_2025_Thai_SWEEVO"]="2512.18470"
  ["C3_2025_Prathifkumar_SWEMemory"]="2512.10218"
  ["C4_2025_Fu_AutoBenchmark"]="2510.24358"
  ["C5_2025_Xu_SWECompass"]="2511.05459"
  # D. Safety & Security
  ["D1_2025_Chhabra_AgenticSecurity"]="2510.23883"
  ["D2_2025_BeurerKellner_SecurePatterns"]="2506.08837"
  ["D3_2025_Liu_AIShellJack"]="2509.22040"
  ["D4_2026_Maloyan_PromptInjection"]="2601.17548"
  ["D5_2025_Hossain_DefensePipeline"]="2509.14285"
  # E. Memory & Context
  ["E1_2025_Chhikara_Mem0"]="2504.19413"
  ["E2_2025_Xu_AMEM"]="2502.12110"
  ["E3_2026_Yu_AgeMem"]="2601.01885"
  ["E4_2026_Borro_Memori"]="2603.19935"
  ["E5_2025_Rezazadeh_CollabMemory"]="2505.18279"
  # F. Tool-Use
  ["F1_2024_Patil_Gorilla"]="2305.15334"
  ["F2_2024_Qin_ToolLLM"]="2307.16789"
  ["F3_2024_Du_AnyTool"]="2402.04253"
  ["F4_2024_Qu_ToolLearningSurvey"]="2405.17935"
  ["F5_2024_Yuan_EasyTool"]="2401.06201"
  # G. Planning & Reasoning
  ["G1_2024_Huang_PlanningSurvey"]="2402.02716"
  ["G2_2024_Liu_LLMP"]="2304.11477"
  ["G3_2024_Ma_AgentBoard"]="2401.13178"
  ["G4_2024_Koh_TreeSearch"]="2407.01476"
  ["G5_2024_Wang_CoTDecoding"]="2402.10200"
  # H. Orchestration
  ["H1_2024_Wu_AutoGen"]="2308.08155"
  ["H2_2024_Chen_AgentVerse"]="2308.10848"
  ["H3_2024_Hong_MetaGPT"]="2308.00352"
  ["H4_2024_Chen_ScalingMAS"]="2401.07324"
  ["H5_2024_Li_CAMEL"]="2303.17760"
  # I. Supplement
  ["I1_2025_AgenticProgramming"]="2508.11126"
  ["I2_2025_Wang_VisualAnalytics"]="2508.12555"
  # Surveys
  ["S1_2023_Wang_AutonomousAgentsSurvey"]="2308.11432"
  ["S2_2024_Han_MASChallenges"]="2402.03578"
  ["S3_2025_Liu_MemorySurvey"]="2603.07670"
  ["S5_2025_EvalSurvey"]="2503.16416"
)

SUCCESS=0
FAIL=0
SKIP=0

for name in $(echo "${!PAPERS[@]}" | tr ' ' '\n' | sort); do
  arxiv_id="${PAPERS[$name]}"
  filename="${name}.pdf"
  
  if [ -f "$filename" ]; then
    echo "SKIP: $filename (already exists)"
    ((SKIP++))
    continue
  fi
  
  url="https://arxiv.org/pdf/${arxiv_id}"
  echo "Downloading: $filename ..."
  if curl -sL -o "$filename" --connect-timeout 15 --max-time 120 "$url"; then
    # Check if actually PDF (not HTML error page)
    if file "$filename" | grep -q "PDF"; then
      echo "  OK: $filename"
      ((SUCCESS++))
    else
      echo "  FAIL (not PDF): $filename"
      rm -f "$filename"
      ((FAIL++))
    fi
  else
    echo "  FAIL (download): $filename"
    rm -f "$filename"
    ((FAIL++))
  fi
  
  # Rate limit: wait 2s between downloads
  sleep 2
done

echo ""
echo "========================================="
echo "Done! Success: $SUCCESS | Skip: $SKIP | Fail: $FAIL"
echo "Total PDFs: $(ls -1 *.pdf 2>/dev/null | wc -l)"
