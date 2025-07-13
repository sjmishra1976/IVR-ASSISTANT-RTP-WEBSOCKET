
## Use Docker Command once asterisk image is installed
docker run -d \
  --name asterisk \
  --hostname=asterisk-docker \
  --network=ivr-assistant-rtp-websocket_default \
  -p 5060:5060/udp \
  -p 5060:5060/tcp \
  -p 10000-10100:10000-10100/udp \
  -p 8088:8088 \
  andrius/asterisk:latest

## OR Start the astrisk services using docker compose yaml file config 
docker-compose up -d

## Create or edit asterisk config files in /etc/asterisk in the container

pjsip.conf – SIP peers, transport-tcp worked only transport-udp did not

extensions.conf – Dialplan logic

queues.conf

http.conf, ari.conf – ARI (REST API)

## Test and CLI Access from host computer
docker exec -it asterisk asterisk -rvvvvv

## To Get public ip and check port listen on local server
curl ifconfig.me
nc -v -u -z -w 3 192.168.86.112 5060
nc -zv 192.168.86.112 8088

## Check asterisk
  docker exec -it asterisk asterisk -rvvv
## Check registration and end point
  pjsip show registrations
  pjsip show endpoints
## Record audio using mac OS recorder app and convert to aterisk  compatible 8000 hz wave file , mono, 16 bit, 1 channel
ffmpeg -i input.m4a -ar 8000 -ac 1 -sample_fmt s16 output.wav

## You may want to use TTS for professional sound, install openTTS image and use below command
curl -G \
  --data-urlencode "text=Welcome to our service" \
  "http://localhost:5500/api/tts?voice=en_US/cmu-arctic-clb" \
  --output welcome.wav
## To list available voices
curl http://localhost:5500/api/voices

## convert to Asterisk compatible
ffmpeg -i input.wav -ar 8000 -ac 1 -sample_fmt s16 output.wav

## Copy your wav files to var/lib/asterisk/sounds
docker cp /path/to/your/file.wav <container_name>:/var/lib/asterisk/sounds/file.wav

## Default music class
docker exec -it asterisk mkdir -p /var/lib/asterisk/moh/default
docker cp your_music.wav asterisk:/var/lib/asterisk/moh/default/
## config needed for musiconhold
/etc/asterisk/musiconhold.conf
[default]
mode=files
directory=moh/default


## RUN Locally
python3 -m venv venv
source venv/bin/activate
FORCE_CMAKE=1 pip install llama-cpp-python
pip install flask crewai langchain


## DOCKER:: Run Locally with Docker
# Build image
cd <project_root>/ivr-backend/
docker build -t ivr-llama-stt .

# DOCKER:: Run container with access to model and audio files
docker run -p 5000:5000 \
  -v $(pwd)/models:/models \
  -v $(pwd)/audio:/audio \
  ivr-llama-stt
