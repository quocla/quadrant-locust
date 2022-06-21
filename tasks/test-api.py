from locust import HttpUser, task


class MyReqRes(HttpUser):
    host = "https://reqres.in"

    @task
    def get_list_user(self):
        url = "/users?page=2"
        res = self.client.get(url, headers={"accept": "*/*"}, name="GET List User")
        print(res.status_code)
        if res.status_code == 200:
            print("GET List User Successfully")

    @task
    def get_single_user(self):
        url = "/api/users/2"
        res = self.client.get(url, headers={"accept": "*/*"}, name="GET Single User")
        print(res.status_code)
        if res.status_code == 200:
            print("GET Single User Successfully")

    @task
    def get_unknown_user(self):
        url = "/api/unknown"
        res = self.client.get(url, headers={"accept": "*/*"}, name="GET Unknown User")
        print(res.status_code)
        if res.status_code == 200:
            print("GET Unknown User Successfully")


