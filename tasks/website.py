import requests
from locust import HttpUser, task, SequentialTaskSet, TaskSet, constant


class MyReqResWebSite(HttpUser):
    host = "https://platform.quadrant.io"

    @task
    def forget_password(self):
        res = self.client.get('/Login/resetPassword.htm')
        print(res.status_code)
        if res.status_code == 200:
            print("Reset password page load successfully")

    @task
    def login(self):
        res = self.client.get('/Login/requestAccess.htm')
        print(res.status_code)
        if res.status_code == 200:
            print("Request login page load successfully")