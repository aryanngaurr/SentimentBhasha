# Hinglish Sentiment Analysis  
A simple Python app that predicts positive/negative sentiment in Hinglish text.  

## Files  
- `app.py`: the main Flask script  
- `requirements.txt`: Python libraries needed  
- `*.pkl`: trained model and transformers  
- `test___muk.txt`: sample input  

## How to run  
1. Install Python 3.8+  
2. `pip install -r requirements.txt`  
3. `python app.py`  
4. Send a POST request to `http://127.0.0.1:5000/predict` with JSON:  
   `{ "text": "मुझे यह app पसंद है" }`
