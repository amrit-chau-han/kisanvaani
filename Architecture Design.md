# KisanVaani v2 System Architecture

This diagram represents the automated flow of the voice-assistant platform.

```mermaid
graph TD
    %% Define Styles to match your SVG colors
    classDef ai fill:#4b2e83,color:#fff,stroke:#333,stroke-width:2px;
    classDef data fill:#8b3a2b,color:#fff,stroke:#333,stroke-width:2px;
    classDef io fill:#2e6400,color:#fff,stroke:#333,stroke-width:2px;
    classDef gen fill:#7a4a00,color:#fff,stroke:#333,stroke-width:2px;
    classDef util fill:#444,color:#fff,stroke:#333,stroke-width:2px;

    %% Configuration
    Config[Cell 1: Config]:::util

    %% Main Flow
    Farmer((Farmer Voice Query)):::io --> UI[Cell 11: StreamLit UI]:::io
    UI --> STT[Sarvam Sarika Model for Voice Query to Text query]:::ai
    STT --> Param[Parameter Extraction]:::ai
    Param --> TransEN[Translate to EN]:::ai
    
    %% Data Layer
    AgMark[AgMarkNet API]:::data --> Fetch[Cell 5: Fetch Data]:::data
    Weather[OpenWeatherMap]:::data --> Fetch
    Tables[(Delta Lake Tables)]:::data --> Fetch
    
    TransEN --> Context[Cell 6: Context Assembly]:::data
    Fetch --> Context
    
    Context --> Gen[Cell 7: Answer Generation]:::gen
    Gen --> TransNative[Cell 8: Translate to Native]:::util
    
    TransNative --> Card[Answer Card]:::io
    TransNative --> TTS[Cell 9: TTS Audio]:::io
    
    Card -.-> Log[Cell 2: Delta Query Log]:::io
    TTS -.-> Log
    
    %% Assigning groups
    subgraph AI_Layer [AI / Indian Models]
        STT
        Param
        TransEN
    end
