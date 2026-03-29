# KisanVaani v2 System Architecture

This diagram represents the automated flow of the voice-assistant platform.

```mermaid
graph TD
    %% Global Styles
    classDef ai fill:#4b2e83,color:#fff,stroke:#333,stroke-width:2px;
    classDef data fill:#8b3a2b,color:#fff,stroke:#333,stroke-width:2px;
    classDef io fill:#2e6400,color:#fff,stroke:#333,stroke-width:2px;
    classDef gen fill:#7a4a00,color:#fff,stroke:#333,stroke-width:2px;

    %% --- INTERACTION LAYER ---
    subgraph Input_Output [User Interface]
        User((Farmer Voice)):::io --> UI[StreamLit UI]:::io
        TTS[TTS Audio Output]:::io --> User
    end

    %% --- AI PROCESSING LAYER ---
    subgraph AI_Engine [AI & Translation Layer]
        UI --> STT[Sarvam Sarika: Voice to Text]:::ai
        STT --> Trans[Sarvam Mayura: Regional to EN]:::ai
        Trans --> LLM[Llama 3.3: Parameter Extraction]:::ai
    end

    %% --- DATA LAYER ---
    subgraph Data_Source [Knowledge Base]
        API[AgMarkNet & Weather APIs]:::data
        Delta[(Delta Lake Tables)]:::data
        API & Delta --> Fetch[Context Assembly]:::data
    end

    %% --- SYNTHESIS LAYER ---
    subgraph Synthesis [Answer Generation]
        LLM --> Fetch
        Fetch --> Gen[Llama 3.3: Answer Gen]:::gen
        Gen --> TransNative[Translate to Native]:::ai
    end

    %% Connecting the flow back to Output
    TransNative --> TTS

    %% Assigning groups
    subgraph AI_Layer [AI / Indian Models]
        STT
        Param
        TransEN
    end
