import logging
import os
from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional

import garth
from withings_sync import fit

logger = logging.getLogger(__name__)

garth.http.USER_AGENT = {"User-Agent": "GCM-iOS-5.7.2.1"}


class Garmin:
    def __init__(
        self, email=None, password=None, is_cn=False, prompt_mfa=None
    ):
        self.username = email
        self.password = password
        self.is_cn = is_cn
        self.prompt_mfa = prompt_mfa

        self.garmin_connect_upload = "/upload-service/upload"
        self.garmin_connect_weight_url = "/weight-service"
        self.garmin_connect_user_settings_url = (
            "/userprofile-service/userprofile/user-settings"
        )

        self.garth = garth.Client(
            domain="garmin.cn" if is_cn else "garmin.com",
            pool_connections=20,
            pool_maxsize=20,
        )

        self.display_name = None
        self.full_name = None
        self.unit_system = None

    def connectapi(self, path, **kwargs):
        return self.garth.connectapi(path, **kwargs)

    def download(self, path, **kwargs):
        return self.garth.download(path, **kwargs)

    def login(self, /, tokenstore: Optional[str] = None):
        tokenstore = tokenstore or os.getenv("GARMINTOKENS")

        if tokenstore:
            if len(tokenstore) > 512:
                self.garth.loads(tokenstore)
            else:
                self.garth.load(tokenstore)
        else:
            self.garth.login(
                self.username, self.password, prompt_mfa=self.prompt_mfa
            )

        self.display_name = self.garth.profile["displayName"]
        self.full_name = self.garth.profile["fullName"]

        settings = self.garth.connectapi(self.garmin_connect_user_settings_url)
        self.unit_system = settings["userData"]["measurementSystem"]

        return True

    def add_body_composition(
        self,
        timestamp: Optional[str],
        weight: float,
        percent_fat: Optional[float] = None,
        percent_hydration: Optional[float] = None,
        visceral_fat_mass: Optional[float] = None,
        bone_mass: Optional[float] = None,
        muscle_mass: Optional[float] = None,
        basal_met: Optional[float] = None,
        active_met: Optional[float] = None,
        physique_rating: Optional[float] = None,
        metabolic_age: Optional[float] = None,
        visceral_fat_rating: Optional[float] = None,
        bmi: Optional[float] = None,
    ):
        dt = datetime.fromisoformat(timestamp) if timestamp else datetime.now()
        fitEncoder = fit.FitEncoderWeight()
        fitEncoder.write_file_info()
        fitEncoder.write_file_creator()
        fitEncoder.write_device_info(dt)
        fitEncoder.write_weight_scale(
            dt,
            weight=weight,
            percent_fat=percent_fat,
            percent_hydration=percent_hydration,
            visceral_fat_mass=visceral_fat_mass,
            bone_mass=bone_mass,
            muscle_mass=muscle_mass,
            basal_met=basal_met,
            active_met=active_met,
            physique_rating=physique_rating,
            metabolic_age=metabolic_age,
            visceral_fat_rating=visceral_fat_rating,
            bmi=bmi,
        )
        fitEncoder.finish()

        url = self.garmin_connect_upload
        files = {
            "file": ("body_composition.fit", fitEncoder.getvalue()),
        }
        return self.garth.post("connectapi", url, files=files, api=True)

    def add_weigh_in(
        self, weight: int, unitKey: str = "kg", timestamp: str = ""
    ):
        """Add a weigh-in (default to kg)"""

        url = f"{self.garmin_connect_weight_url}/user-weight"
        dt = datetime.fromisoformat(timestamp) if timestamp else datetime.now()
        # Apply timezone offset to get UTC/GMT time
        dtGMT = dt.astimezone(timezone.utc)
        payload = {
            "dateTimestamp": dt.isoformat()[:19] + ".00",
            "gmtTimestamp": dtGMT.isoformat()[:19] + ".00",
            "unitKey": unitKey,
            "sourceType": "MANUAL",
            "value": weight,
        }
        logger.debug("Adding weigh-in")

        return self.garth.post("connectapi", url, json=payload)
