from locust import HttpUser, task, between

class ReportSimUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def report_sales_pdf(self):
        self.client.get("/reports/sales/pdf")

    @task(2)
    def report_users_excel(self):
        self.client.get("/reports/users/excel")
