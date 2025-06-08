from locust import HttpUser, task, between

class SearchApiUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def check_latency_all(self):
        self.client.get("/check_latency?module=all")

    @task(2)
    def check_availability_all(self):
        self.client.get("/check_availability?module=all")

    @task(1)
    def render_graph_latency(self):
        self.client.get("/render_graph?metric=latency&module=all&period=Last5Days")

    @task(1)
    def render_graph_availability(self):
        self.client.get("/render_graph?metric=availability&module=all&period=Last7Days")