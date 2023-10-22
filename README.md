# LLM Benchmarking for Danish via Ollama

# Description
This repository aims to automate and publish benchmarking tests for off-the-shelf variations of common Free and Open Source Software (FOSS) Large Language Models (LLMs), available through Ollama. The goal is to identify a model that matches or surpasses GPT-4's proficiency in Danish communication.

This is done in the following way:
```mermaid
flowchart LR
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

E -- Query --> AE[Result]
F -- Query --> AF[Result]
G -- Query --> AG[Result]
H -- Query --> AH[Result]
I -- Query --> AI[Result]
J -- Query --> AJ[Result]
K -- Query --> AK[Result]
L -- Query --> AL[Result]
M -- Query --> AM[Result]

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

BA -- Score --> CA[Leaderboard]
BB -- Score --> CA[Leaderboard]
BC -- Score --> CA[Leaderboard]
BD -- Score --> CA[Leaderboard]
BE -- Score --> CA[Leaderboard]
BF -- Score --> CA[Leaderboard]
BG -- Score --> CA[Leaderboard]
BH -- Score --> CA[Leaderboard]
BI -- Score --> CA[Leaderboard]


```

- [ ] Experiment with [Modefiles](https://github.com/jmorganca/ollama/blob/main/docs/modelfile.md)
- [ ] Experiemnt with model variations
- [ ] Experiment with larger models like llama2:70b (Need more GPU)
- [ ] Implement RAG
- [ ] Look into spell checker api like Smodin
