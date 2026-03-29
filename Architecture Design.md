# KisanVaani v2 System Architecture

This diagram represents the automated flow of the voice-assistant platform.

```mermaid
graph LR
    %%{init: {'theme': 'dark', 'flowchart': {'rankSpacing': 30, 'nodeSpacing': 30}}}%%
    
    classDef ai fill:#4b2e83,color:#fff,stroke:#333;
    classDef data fill:#8b3a2b,color:#fff,stroke:#333;
    classDef io fill:#2e6400,color:#fff,stroke:#333;
    classDef gen fill:#7a4a00,color:#fff,stroke:#333;

    %% INPUT SECTION (LEFT)
    subgraph Input ["Step 1: Input"]
        
        UI --> STT[Sarvam Sarika: Voice to text query]:::ai
        STT --> Mayura[Sarvam Mayura: regional to english text ]:::ai
Mayura --> LlamaParam[Llama: Parameters extraction]:::ai
    end

    %% PROCESSING & DATA (MIDDLE - SIDE BY SIDE)
    
    
    subgraph Knowledge ["Step 2: Knowledge Retrieval"]
        direction TB
        AgMark[AgMarkNet API]:::data
        Weather[Weather API]:::data
        Delta[(Delta Lake)]:::data
    end

    %% SYNTHESIS (RIGHT)
    LlamaParam --> Context[Context Assembly]:::gen
    AgMark & Weather & Delta --> Context
    
    subgraph Output ["Step 3: Response"]
        Context --> Gen[Answer Gen]:::gen
        Gen --> Native[Native Translation]:::ai
        Native --> TTS[Audio Out]:::io
    end

 

    %% Assigning groups
    subgraph AI_Layer [AI / Indian Models]
        STT
        Param
        TransEN
    end
