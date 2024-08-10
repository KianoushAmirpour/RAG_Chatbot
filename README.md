### Description of the project
Utilized Retrieval Augmented Generation (RAG) to answer users' questions about neuroscience based on [Huberman Lab YouTube channel](https://www.youtube.com/@hubermanlab/videos).  

### Demo

https://github.com/user-attachments/assets/c2a26e74-bbf5-4710-84e9-037af3058203

### Data
The following information is extracted from the YouTube API: video titles, timestamps, transcripts, and subtitles.  
Transcripts are aggregated based on subtitle timestamps and saved as a JSON file.  
A sample of the preprocessed data can be seen below.  
```{   "video_id": "-OBCwiPPfEU",
    "title": "Dr. Matt Walker: The Biology of Sleep & Your Unique Sleep Needs | Huberman Lab Guest Series",
    "published_at": "2024-04-03T12:00:00Z",
    "transcripts": [
        {
            "timestamp": 0,
            "sub_title_section": "Importance of Sleep",
            "text": ""
        },
        {
            "timestamp": 144,
            "sub_title_section": "Sponsors: Eight Sleep, BetterHelp & LMNT",
            "text": ""
      }]
```

### Techniques used for enhancing the performance of RAG
* Generating multiple queries from user's initial query can help capture various aspects of their intent.
  
```
  User query: how do sleeping positions impact my health?
  Generated queries by llm:
    1. What are the benefits of sleeping on your back for overall health?
    2. How does sleeping on your stomach affect your spine and joints in the long term?
    3. Can sleeping with a pillow between your knees help alleviate lower back pain?
```
* Reranking retrieved results for each query using `cross-encoder/ms-marco-MiniLM-L-12-v2` and sort the results based on similarity scores.
* Create and Refine strategy  
  You can see the differences between the response when this strategy is not enabled (first one) and when it is enabled (second one)
```
  Based on the provided context, it seems that sleeping position can have an impact on one's health.
  The speaker mentions that being horizontal (lying flat) can cause the body temperature to drop more quickly,
  which is one of the reasons why it may be harder to fall asleep and sleep quality may not be as good when at a 45° angle.
  Additionally, the speaker references a study by their colleagues at the University of Surrey,
  which suggests that sleeping position can affect the distribution of blood flow in the body.
  It's also mentioned that snoring is related to sleeping position, and that people who are prone to snoring may benefit
  from avoiding certain positions or adjusting their sleep setup.
  The speaker does not provide a comprehensive answer on how sleeping positions impact health,
  but it seems that there are some specific effects associated with different positions.
  In summary, the provided context suggests that sleeping position can affect body temperature, blood flow,
  and potentially even snoring, which may have implications for overall health.
```  
```
 Here's a refined version of the original answer that incorporates the additional context:
 Sleeping positions can have a significant impact on your overall health, and it's essential to consider your
 individual body type when choosing a sleeping position.
 For instance, if you're someone with thicker wrists, knees, or elbows, you may want to avoid sleeping in a position
 that puts pressure on these areas, such as lying flat on your stomach.
 On the other hand, if you have a more slender build and can move easily from side to side,
 you may find that sleeping on your side is comfortable for you.
 However, it's essential to note that sleeping at an angle (e.g., 45°) may not be suitable for everyone,
 especially those with spinal issues or back pain.
 Research has shown that certain sleeping positions can affect the cellular and molecular state of our bodies,
 including blood circulation and inflammation levels.
 For example, lying down can help improve blood circulation and reduce inflammation, which can have positive effects on overall health.
 It's also important to consider your snoring habits when choosing a sleeping position.
 If you're a snorer, certain positions may exacerbate or alleviate the issue, which can impact your overall health.
 In addition to these factors, it's crucial to prioritize sleep quality and maintain a consistent sleep schedule.
 Sleep deprivation can have far-reaching effects on our emotional and mood states, as well as our cardiovascular system.
 Even losing just one hour of sleep can impact our emotional state and increase the risk of sentencing errors.
 Ultimately, finding a comfortable sleeping position that suits your individual body type is crucial for maintaining good health.
 By taking into account your unique characteristics and needs, you can optimize your sleep quality and wake up feeling refreshed and rejuvenated.
```  

### LLM
The LLM used in this project is the quantized version of `Llama-3-8B-Instruct`. [Meta-Llama-3-8B-Instruct.Q5_K_M.gguf](https://huggingface.co/QuantFactory/Meta-Llama-3-8B-Instruct-GGUF/tree/main)  

`Llama-cpp`is also used to run the model locally. You can find more information [here](https://llama-cpp-python.readthedocs.io/en/latest/)

### Tools
* Qdrant is used as the vector database.
* LlamaIndex is used as the framework to build this chatbot.
* Docker Compose is used to run Qdrant and Redis.
* Redis Streams is used for handling real-time communication and also keep track of chat history(memory).
* FastAPI and WebSockets are used to send messages between the client and server in real time.

### To do
Adjust the Create and Refine strategy to also return the URLs of the videos  
Latency Reduction  
Evaluation of RAG  
