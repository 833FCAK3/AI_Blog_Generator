# AI Blog Generator

## Description
Transcribes youtube videos via [assemblyai](https://www.assemblyai.com) (english and russian languages supported) and writes a blog style summary using either [chatgpt](https://chat.openai.com/) or local model ran via [Ollama](https://ollama.com/download)

Транскрибирует видео с YouTube с помощью assemblyai (поддерживаются английский и русский языки) и пишет сводку в стиле блога, используя chatgpt или локальную модель, запускаемую через Ollama.

## Start
Clone repo: 
```
>>> git clone https://github.com/833FCAK3/AI_Blog_Generator.git
```
**Make sure you have the following:**
- Install [docker](https://docs.docker.com/engine/install/)
- Install [docker-compose](https://docs.docker.com/compose/install/)
- *For convenience install [MAKE Windows](http://gnuwin32.sourceforge.net/packages/make.htm), otherwise run all the commands from makefile under ```all```

- Configure app ports and timezone in ```.env``` file
- Rename ```api_keys_example.py``` into ```api_keys.py``` and set your [assemblyai](https://www.assemblyai.com) ```api key``` there.
- Launch app with: 
````
>>> make
````
In case you do not have ```make```:
```
docker-compose build --no-cache
docker-compose down
docker-compose run ai_blog_app bash -c "python manage.py migrate"
docker exec -it ollama_app bash -c "ollama pull llama3" 
docker-compose up -d 
```
Access the app on:
http://127.0.0.1:8000
