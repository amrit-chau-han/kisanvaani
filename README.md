
# KisanVaani v2: Voice-First Agritech Assistant

**KisanVaani** is an AI-powered voice assistant that provides Indian farmers with real-time Mandi prices, weather updates, and crop advisories through simple native-language voice queries. By leveraging Databricks Lakehouse and state-of-the-art Indic models, it eliminates the digital literacy barrier in rural agriculture.

---

## 🏗 System Architecture

This system is hosted on the **Databricks Data Intelligence Platform**, utilizing Delta Lake for data storage and Model Serving for inference.

```mermaid
%%{init: {'theme': 'dark', 'flowchart': {'rankSpacing': 70, 'nodeSpacing': 50}}}%%
graph TD
    %% Style Definitions
    classDef ai fill:#4b2e83,color:#fff,stroke:#fff,stroke-width:1px;
    classDef data fill:#8b3a2b,color:#fff,stroke:#fff,stroke-width:1px;
    classDef io fill:#2e6400,color:#fff,stroke:#fff,stroke-width:1px;
    classDef gen fill:#7a4a00,color:#fff,stroke:#fff,stroke-width:1px;

    %% Flow
    Farmer((Farmer Voice Query)):::io --> UI[Cell 11: StreamLit UI]:::io
    
    subgraph AI_Layer [Indic AI Stack]
        STT[Sarvam Saarika: Voice to Text]:::ai
        Trans[Sarvam Maurya: Translation]:::ai
    end

    subgraph Data_Layer [Databricks Lakehouse]
        DB[(Delta Lake: Crop Advisory)]:::data
        API[AgMarkNet & Weather APIs]:::data
    end

    UI --> STT
    STT --> Trans
    Trans --> Context[Cell 6: Context Assembly]:::data
    DB --> Context
    API --> Context
    
    Context --> LLM[Llama 3 70B: Answer Gen]:::gen
    LLM --> UI
