# DogGPT telegram bot

This is a telegram bot to get responces from OpenAI text models.

installation:
```
git clone https://github.com/AntonZamyatin/dogGPT
cd dogGPT

# using virtual environment (optional)
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

After installation you should create `.env` file in `dogGPT` directory.

This is a text file with api keys for services:

```.env
OpenAI_ORG_ID="[org id from openAI]"
OpenAI_API_KEY="[api key from openAI]"
TG_BOT_TOKEN="[telegram bot token]"
```