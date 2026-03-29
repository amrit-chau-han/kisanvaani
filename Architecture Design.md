# KisanVaani v2 System Architecture

This diagram represents the automated flow of the voice-assistant platform.

```mermaid
graph TD
    %%{init: {'theme': 'dark', 'flowchart': {'rankSpacing': 50, 'nodeSpacing': 50}}}%%
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
    STT --> Param[Translate query from regional language to English]:::ai
    Param --> TransEN[Extract Parameters]:::ai
    
    %% Data Layer
    AgMark[AgMarkNet API]:::data --> Fetch[Fetch Data]:::data
    Weather[OpenWeatherMap]:::data --> Fetch
    Tables[(Delta Lake Tables)]:::data --> Fetch
    
    TransEN --> Context[Cell 6: Context Assembly]:::data
    Fetch --> Context
    
    Context --> Gen[Answer Generation]:::gen
    Gen --> TransNative[Translate to Native]:::util
    
    TransNative --> Card[Answer Card]:::io
    TransNative --> TTS[TTS Audio]:::io
    
    Card -.-> Log[Delta Query Log]:::io
    TTS -.-> Log
    
    %% Assigning groups
    subgraph AI_Layer [AI / Indian Models]
        STT
        Param
        TransEN
    end
