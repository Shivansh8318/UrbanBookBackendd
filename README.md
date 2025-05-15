# UrbanBook Backend

## Getting Started

### Installation

1. Clone the repository:
```
git clone https://github.com/Shivansh8318/UrbanBookBackendd.git
cd urbanbookbackend3/backend
```

2. Create and activate a virtual environment:
```
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```


### Running the Server

1. Make sure Redis is running (required for WebSocket support):
```
Use docker
```

2. Start the development server:
```
daphne -b 0.0.0.0 -p 8000 urb_backend.asgi:application
```

### Start ngrok



```
ngrok http 8000
```

Update the base URL in the frontend application to the ngrok URL.

