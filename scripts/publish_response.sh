#!/usr/bin/env sh

set -x
cd "$(dirname "$0")"
TIMESTAMP=$(gdate +%s%N)

TOPIC="/coach/durandom"
T='{"message": "https://www.mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/Samples/AFsp/M1F1-Alaw-AFsp.wav", "priority": 9}'
T='{"message": "https://gitlab.com/mr_belowski/CrewChiefV4/-/raw/master/CrewChiefV4/sounds/driver_names/Ek.wav?inline=false", "priority": 9}'
T='{"message": "brake normal gear 2", "priority": 9}'
T='{"message": "https://github.com/durandom/racing-assets/raw/main/speech.mp3", "priority": 9}'

if [ -z "$MQTT_HOST" ]; then
  MQTT_HOST=telemetry.b4mad.racing
fi
CLIENT_ID=$(hostname)-$$

mosquitto_pub -u crewchief -P crewchief \
  -t "$TOPIC" \
  -p 31883 -h $MQTT_HOST -i $CLIENT_ID -d \
  -m "$T"
