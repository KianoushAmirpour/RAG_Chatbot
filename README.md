### Description of the project
Utilized Retrieval Augmented Generation (RAG) to answer users' questions about neuroscience based on [Huberman Lab YouTube channel](https://www.youtube.com/@hubermanlab/videos).

### Demo

https://github.com/user-attachments/assets/ffb38b10-e329-4971-9140-22024a2b16b4

### Data
Following information is extracted from the YouTube API: video titles, timestamps, transcripts, and subtitles.  
Transcripts will be aggregated based on subtitle timestamps and will be saved as json file.  
A sample of the ready to use json file can be seen below.
```{   "video_id": "-OBCwiPPfEU",
    "title": "Dr. Matt Walker: The Biology of Sleep & Your Unique Sleep Needs | Huberman Lab Guest Series",
    "published_at": "2024-04-03T12:00:00Z",
    "transcripts": [
        {
            "timestamp": 0,
            "sub_title_section": "Importance of Sleep",
            "text": " "
        },
        {
            "timestamp": 144,
            "sub_title_section": "Sponsors: Eight Sleep, BetterHelp & LMNT",
            "text": ""
      }]
```

### Techniques for enhancing the performance of rag
Generate multiple queries and retrieved results for each of them (with the help of the model)  
Example for multiple query generation
Rerank with cross encoders(model)   
Create and refine theqniques   

### LLM
[Meta-Llama-3-8B-Instruct.Q5_K_M.gguf](https://huggingface.co/QuantFactory/Meta-Llama-3-8B-Instruct-GGUF/tree/main)  

`Llama-cpp` is used to run the model locally.

### Tools
`FastAPI` and `Websockets` to   
`Llama index` to  
`Qdrant` to  
`Docker Compose` to  
`Redis Stream` to   

### To do
Reduce the latency.
Evaluation of retrieved results using metrics like 
