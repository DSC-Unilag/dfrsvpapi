import time
import psycopg2
import os
import random
from dotenv import load_dotenv
from locust import HttpUser, task, between


load_dotenv()


URL = os.getenv('API_URL')

# conn = psycopg2.connect(
#     host=os.getenv('host'),
#     dbname=os.getenv('dbname'),
#     password=os.getenv('password'),
#     user='root'
# )
# cur = conn.cursor()


class ProductionTrackUser(HttpUser):
    wait_time = between(1, 5)

    URL = os.getenv('API_URL')
    # # fetch locations
    # cur.execute(
    #     f"""
    #     SELECT id FROM location WHERE organization_id = 4 AND
    #     EXISTS (SELECT 1 FROM license_plate WHERE location_id = location.id);
    #     """
    # )
    # locs = [x[0] for x in cur.fetchall()]

    # def prepare_headers(self):
    #     token = self.client.post(
    #         url=os.getenv('API_LOGIN'),
    #         data={
    #             'email': 'mercy@lexcorp.com',
    #             'password': 'vishwa'
    #         }
    #     ).json()['data']['access_token']
    #     return {
    #         "Authorization": f"Bearer {token}"
    #     }
    
    # def getData(self):
    #     loc_pair = random.choices(ProductionTrackUser.locs, k=2)
    #     src = random.choice(loc_pair)
    #     cur.execute(
    #         f"""
    #         SELECT id FROM license_plate WHERE organization_id = 4 AND location_id = {src}
    #         """
    #     )
    #     res = cur.fetchone()
    #     if res:
    #         res = res[0]
    #     else:
    #         res = 2315
    #     payload_schema = {
    #         "dest_location_id": loc_pair[0] if loc_pair.index(src) else loc_pair[1],
    #         "license_plate_id": res
    #     }

    #     print({'src_loc': src, **payload_schema})

    #     return payload_schema

    def getData(self):
        ticNos = [
            "DSCA231975844",
            "DSCA231921621",
            "DSCA231923114",
            "DSCA231926593",
            "DSCA231975556",
            "DSCA231922755",
            "DSCA231950519",
            "DSCA231938572",
            "DSCA231970670",
            "DSCA231957894"
        ]
        
        events = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        uid = random.choice(ticNos)
        events = random.sample(events, k=3)

        resp = {
            "ticket_id": uid,
            "event_ids": events
        }

        print(resp)

        return resp

    @task
    def rsvp(self):
        _path = f"rsvp/"

        resp = self.client.post(
            url=URL+f"/{_path}",
            json=self.getData(),
        )

        print("resp:: ", resp.json())
        

    # def on_start(self):
    #     self.client.post("/login", json={"username":"foo", "password":"bar"})
