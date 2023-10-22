# LLM Benchmarking for Danish via Ollama

# Problem that is trying to be solved

# Description
This repository poses a design for a framework for automating and publishing benchmarking tests for off-the-shelf variations of common Free and Open Source Software (FOSS) Large Language Models (LLMs), available through [Ollama](https://ollama.ai/), specifically with the **goal of identifiying model(s) that can match or surpass GPT-4's proficiency in Danish communication** (should these exist).

The framework is not inherently designed to evaluate Danish per se, but could likewise be used to evaluate other languages, albeit this not being the focus of this repo.

The process is carried out in three overall steps:
1. **Model creation**
1. **Evaluation**
1. **Scoring**


```mermaid
flowchart LR
subgraph Model Creation
A[Ollama] --Pull--> B[Vicuna:13b]
A[Ollama] --Pull--> C[Vicuna:33b]
A[Ollama] --Pull--> D[Vicuna:70b]

B[Vicuna:13b] --Create variation via modelfile-->E[Vicuna:13b variation 1]
C[Vicuna:33b] --Create variation via modelfile-->F[Vicuna:33b variation 1]
D[Vicuna:70b] --Create variation via modelfile-->G[Vicuna:70b variation 1]
B[Vicuna:13b] --Create variation via modelfile-->H[Vicuna:13b variation 2]
C[Vicuna:33b] --Create variation via modelfile-->I[Vicuna:33b variation 2]
D[Vicuna:70b] --Create variation via modelfile-->J[Vicuna:70b variation 2]
B[Vicuna:13b] --Create variation via modelfile-->K[Vicuna:13b variation 3]
C[Vicuna:33b] --Create variation via modelfile-->L[Vicuna:33b variation 3]
D[Vicuna:70b] --Create variation via modelfile-->M[Vicuna:70b variation 3]

end
E -- Query --> AE[Result]
F -- Query --> AF[Result]
G -- Query --> AG[Result]
H -- Query --> AH[Result]
I -- Query --> AI[Result]
J -- Query --> AJ[Result]
K -- Query --> AK[Result]
L -- Query --> AL[Result]
M -- Query --> AM[Result]

subgraph Evaluation Chain
AE -- Evaluate--> DN[Language detection]
AF -- Evaluate--> DP[Language detection]
AG -- Evaluate--> DQ[Language detection]
AH -- Evaluate--> DR[Language detection]
AI -- Evaluate--> DS[Language detection]
AJ -- Evaluate--> DT[Language detection]
AK -- Evaluate--> DU[Language detection]
AL -- Evaluate--> DV[Language detection]
AM -- Evaluate--> DW[Language detection]

DN -- Evaluate --> AAA[...]
DP -- Evaluate --> AAB[...]
DQ -- Evaluate --> AAC[...]
DR -- Evaluate --> AAD[...]
DS -- Evaluate --> AAE[...]
DT -- Evaluate --> AAF[...]
DU -- Evaluate --> AAG[...]
DV -- Evaluate --> AAH[...]
DW -- Evaluate --> AAI[...]

AAA -- Evaluate --> BA[Language Tool API]
AAB -- Evaluate --> BB[Language Tool API]
AAC -- Evaluate --> BC[Language Tool API]
AAD -- Evaluate --> BD[Language Tool API]
AAE -- Evaluate --> BE[Language Tool API]
AAF -- Evaluate --> BF[Language Tool API]
AAG -- Evaluate --> BG[Language Tool API]
AAH -- Evaluate --> BH[Language Tool API]
AAI -- Evaluate --> BI[Language Tool API]
end

subgraph Results
BA -- Score --> CA[Leaderboard]
BB -- Score --> CA[Leaderboard]
BC -- Score --> CA[Leaderboard]
BD -- Score --> CA[Leaderboard]
BE -- Score --> CA[Leaderboard]
BF -- Score --> CA[Leaderboard]
BG -- Score --> CA[Leaderboard]
BH -- Score --> CA[Leaderboard]
BI -- Score --> CA[Leaderboard]
end
```

The **Model creation** step can be extended *vertically*, as additional variations can be added parameters for variations include:
- Base model
- Variations (Tags)
- Modelfile parameters
- Pre-prompt
- RAG
- Fine-tuning

The **Evaluation** step can be extended *horizontally*, adding additional evaluation steps. Possibilities include:
- Language detection
- Bing Proof
- Bing spell-checker
- Language tool

The process can be run *ad infinitum* to increase result confidence

## To-dos
- [ ] Experiment with [Modelfiles](https://github.com/jmorganca/ollama/blob/main/docs/modelfile.md)
- [ ] Experiemnt with model variations
- [ ] Experiment with larger models like llama2:70b (Need more GPU)
- [ ] Implement RAG
- [ ] Look into spell checker api like Smodin
