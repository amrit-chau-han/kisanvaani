
# KisanVaani v2: Voice-First Agritech Assistant

**KisanVaani** is a multilingual AI assistant built on Databricks Lakehouse, providing farmers real-time market and weather insights. Using Sarvam Saarika (STT) and Sarvam Maurya (NLU/Translation), it enables voice-to-voice interaction in Hindi, English, Marathi, and Punjabi. By integrating AgMarkNet and OpenWeatherMap with Delta Lake caching, the system delivers precise, actionable crop advice for any district in under 10 seconds—bridging the digital literacy gap for rural India.

---

## 🏗 System Architecture

This system is hosted on the **Databricks Data Intelligence Platform**, utilizing Delta Lake for data storage and Model Serving for inference.

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


    %% Main Flow
    Farmer((Farmer Voice Query)):::io --> UI[StreamLit UI]:::io
    UI --> STT[Sarvam Sarika Model for Voice Query to Text query]:::ai
    STT --> Param[Translate query from regional language to English]:::ai
    Param --> TransEN[Extract Parameters]:::ai

    %% Data Layer
    AgMark[AgMarkNet API]:::data --> Fetch[Fetch Data]:::data
    Weather[OpenWeatherMap]:::data --> Fetch
    Tables[(Delta Lake Tables)]:::data --> Fetch
    
    TransEN --> Context[Context Assembly]:::data
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
```


## How to Run

To launch the **KisanVaani v2** assistant within your Databricks workspace, follow these steps:

1. **Open the Notebook**: Navigate to the `app_launcher.ipynb` file in this repository.
2. **Start the Server**: Run the main execution cell. This will initialize the backend connection to the **Sarvam** and **Llama** model endpoints.
3. **Access the Interface**: 
   - After the cell runs, a **Streamlit Proxy URL** will be generated in the output.
   - Click the link to open the assistant in a new browser tab.

---

##  Demo Steps (How to Use)

Once the application interface is open, follow these steps to interact with the assistant:

### 1. Voice Query
* Click the **Microphone icon** (Start Recording).
* Speak your question clearly in your native language (e.g., Hindi, Marathi, or English).
* *Example:* "What is the current market price for cotton in the Akola Mandi?"

### 2. Real-Time Processing
* **STT:** Watch as the **Sarvam Saarika** model converts your voice into text on the screen.
* **Context:** The system will automatically fetch live data from **AgMarkNet** and **OpenWeatherMap**.

### 3. Response & Playback
* **Answer Card:** A visual card will appear with the specific prices or weather advisory you requested.
* **Audio Playback:** The **Sarvam TTS** engine will automatically play the response back to you in the same language you spoke.

---

##  Tech Stack
* **Platform:** Databricks Lakehouse
* **Models:** Sarvam Saarika (STT), Sarvam Maurya (Translation), Llama 3 70B (LLM)
* **UI:** Streamlit

UI libraries
pip install streamlit sarvam-sdk databricks-sdk pandas
