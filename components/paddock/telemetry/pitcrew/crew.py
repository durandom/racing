#!/usr/bin/env python3

import datetime
import os
import threading
import logging
import time
import paho.mqtt.client as mqtt
from telemetry.models import Game, Driver, Car, Track, SessionType, Coach
import json

from .coach import Coach as PitCrewCoach
from .history import History
from .mqtt import Mqtt

_LOGGER = logging.getLogger("pitcrew")


class Crew:
    def __init__(self):
        mqttc = mqtt.Client()
        mqttc.on_message = self.on_message
        mqttc.on_connect = self.on_connect
        mqttc.on_publish = self.on_publish
        mqttc.on_subscribe = self.on_subscribe
        # mqttc.username_pw_set(env('B4MAD_RACING_CLIENT_USER'), env('B4MAD_RACING_CLIENT_PASSWORD'))
        mqttc.username_pw_set(
            os.environ.get("B4MAD_RACING_CLIENT_USER", ""),
            os.environ.get("B4MAD_RACING_CLIENT_PASSWORD", ""),
        )
        self.mqttc = mqttc
        self.active_topics = set()
        self.active_drivers = set()
        self.active_coaches = {}

    def on_message(self, mqttc, obj, msg):
        """Handle incoming messages, we are only interested in the telemetry.

        Args:
            mqttc (_type_): the mqtt client
            obj (_type_): the userdata
            msg (_type_): the message received
        """

        # _LOGGER.debug(
        #     "%s: qos='%s',payload='%s'", msg.topic, str(msg.qos), str(msg.payload)
        # )

        if msg.topic not in self.active_topics:
            print(f"New topic: {msg.topic}")
            prefix, driver, session, game, track, car, session_type = msg.topic.split(
                "/"
            )
            self.active_topics.add(msg.topic)

            record = json.loads(msg.payload.decode("utf-8"))
            print(record)

            rgame, created = Game.objects.get_or_create(name=game)
            rdriver, created = Driver.objects.get_or_create(name=driver)
            rcar, created = Car.objects.get_or_create(name=car, game=rgame)
            rtrack, created = Track.objects.get_or_create(name=track, game=rgame)
            rsession_type, created = SessionType.objects.get_or_create(
                type=session_type
            )
            t = datetime.datetime.fromtimestamp(record["time"] / 1000)

            rsession, created = rdriver.session_set.get_or_create(
                session_id=session,
                session_type=rsession_type,
                car=rcar,
                track=rtrack,
                game=rgame,
                defaults={"start": t, "end": t},
            )
            # maybe already create a lap?

            if driver.lower() != "jim":
                if driver not in self.active_drivers:
                    print(f"New coach for {driver}")
                    if not rdriver.coach:
                        Coach.objects.create(driver=driver)
                    self.active_drivers.add(rdriver)

    def on_connect(self, mqttc, obj, flags, rc):
        _LOGGER.debug("rc: %s", str(rc))

    def on_publish(self, mqttc, obj, mid):
        _LOGGER.debug("mid: %s", str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        _LOGGER.debug(
            "subscribed: mid='%s', granted_qos='%s'", str(mid), str(granted_qos)
        )

    def on_log(self, mqttc, obj, level, string):
        # print(string)
        pass

    def watch_coaches(self):
        while True:
            time.sleep(10)
            _LOGGER.info("checking coaches")
            coaches = Coach.objects.filter(driver__in=self.active_drivers)
            for coach in coaches:
                _LOGGER.info(f"checking coach for {coach.driver}")
                if coach.enabled:
                    if coach.driver.name not in self.active_coaches.keys():
                        _LOGGER.debug(f"activating coach for {coach.driver}")
                        self.start_coach(coach.driver.name, coach)
                else:
                    if coach.driver.name in self.active_coaches.keys():
                        _LOGGER.debug(f"deactivating coach for {coach.driver}")
                        self.stop_coach(coach.driver)

    def stop_coach(self, driver):
        self.active_coaches[driver.name][0].disconnect()
        self.active_coaches[driver.name][1].disconnect()
        del self.active_coaches[driver.name]

    def start_coach(self, driver, coach):
        history = History()
        coach = PitCrewCoach(history, coach)
        mqtt = Mqtt(coach, driver)

        def history_thread():
            _LOGGER.info(f"History thread starting for {driver}")
            history.run()
            _LOGGER.info(f"History thread stopped for {driver}")

        h = threading.Thread(target=history_thread)

        def mqtt_thread():
            _LOGGER.info(f"MQTT thread starting for {driver}")
            mqtt.run()
            _LOGGER.info(f"MQTT thread stopped for {driver}")

        c = threading.Thread(target=mqtt_thread)

        threads = list()
        threads.append(h)
        threads.append(c)
        c.start()
        h.start()
        self.active_coaches[driver] = [history, mqtt]

    def run(self):
        self.mqttc.connect("telemetry.b4mad.racing", 31883, 60)
        topic = "crewchief/#"
        s = self.mqttc.subscribe(topic, 0)
        if s[0] == mqtt.MQTT_ERR_SUCCESS:
            threading.Thread(target=self.watch_coaches).start()
            _LOGGER.info(f"Subscribed to {topic}")

            self.mqttc.loop_forever()
        else:
            _LOGGER.error(f"Failed to subscribe to {topic}")
            exit(1)
