## start the astrisk services 
docker-compose up -d

## Create or edit files like:

pjsip.conf – SIP peers, transport-tcp worked only transport-udp did not

extensions.conf – Dialplan logic

queues.conf

http.conf, ari.conf – ARI (REST API)

## Test and CLI Access
docker exec -it asterisk asterisk -rvvvvv

### get public ip
curl ifconfig.me
nc -v -u -z -w 3 192.168.86.112 5060
nc -zv 192.168.86.112 8088

## Docker Command
docker run -d \
  --name asterisk \
  --hostname=asterisk-docker \
  --network=ivr-assistant-rtp-websocket_default \
  -p 5060:5060/udp \
  -p 5060:5060/tcp \
  -p 10000-10100:10000-10100/udp \
  -p 8088:8088 \
  andrius/asterisk:latest
## check asterisk
  docker exec -it asterisk asterisk -rvvv
## check registration and end point
  pjsip show registrations
  pjsip show endpoints
# Record audio using mac OS recorder app and convert to aterisk  compatible 8000 hz wave file , mono, 16 bit, 1 channel
ffmpeg -i input.m4a -ar 8000 -ac 1 -sample_fmt s16 output.wav

## Copy your wav files
docker cp /path/to/your/file.wav <container_name>:/var/lib/asterisk/sounds