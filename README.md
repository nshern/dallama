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

E -- Evaluate--> N[Language detection]
F -- Evaluate--> P[Language detection]
G -- Evaluate--> Q[Language detection]
H -- Evaluate--> R[Language detection]
I -- Evaluate--> S[Language detection]
J -- Evaluate--> T[Language detection]
K -- Evaluate--> U[Language detection]
L -- Evaluate--> V[Language detection]
M -- Evaluate--> W[Language detection]

N -- Evaluate --> AA[Bing Proof/Spell checker]
P -- Evaluate --> AB[Bing Proof/Spell checker]
Q -- Evaluate --> AC[Bing Proof/Spell checker]
R -- Evaluate --> AD[Bing Proof/Spell checker]
S -- Evaluate --> AE[Bing Proof/Spell checker]
T -- Evaluate --> AF[Bing Proof/Spell checker]
U -- Evaluate --> AG[Bing Proof/Spell checker]
V -- Evaluate --> AH[Bing Proof/Spell checker]
W -- Evaluate --> AI[Bing Proof/Spell checker]

AA -- Evaluate --> BA[Language Tool API]
AB -- Evaluate --> BB[Language Tool API]
AC -- Evaluate --> BC[Language Tool API]
AD -- Evaluate --> BD[Language Tool API]
AE -- Evaluate --> BE[Language Tool API]
AF -- Evaluate --> BF[Language Tool API]
AG -- Evaluate --> BG[Language Tool API]
AH -- Evaluate --> BH[Language Tool API]
AI -- Evaluate --> BI[Language Tool API]

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
