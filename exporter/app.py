#!/usr/bin/python3

import os, sys, time, logging, signal, random, uptime, prometheus_client
from prometheus_client import start_http_server, Gauge, Enum

logging.basicConfig(
  level    = logging.INFO,
  format   = "%(asctime)s [%(levelname)s] %(message)s",
  handlers = [
    logging.StreamHandler(sys.stdout)
  ]
)

prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)

class AppMetrics:

  def __init__(self, app_port=80, interval=5):
    self.app_port = app_port
    self.interval = interval

    # Prometheus metrics to collect
    self.current_requests = Gauge("app_requests_current", "Current requests")
    self.pending_requests = Gauge("app_requests_pending", "Pending requests")
    self.total_uptime     = Gauge("app_uptime", "Uptime")
    self.health           = Enum("app_health", "Health", states=["healthy", "unhealthy"])

  def fetch(self):
    # Example Prometheus metric values.
    app_data = {
      "current_requests": random.randint(20, 40),
      "pending_requests": random.randint(5, 15),
      "total_uptime": uptime.uptime(),
      "health": "healthy"
    }

    # Update Prometheus metrics with example values
    self.current_requests.set(app_data["current_requests"])
    self.pending_requests.set(app_data["pending_requests"])
    self.total_uptime.set(app_data["total_uptime"])
    self.health.state(app_data["health"])

  def run(self):
    # Metrics fetching loop
    while True:
      self.fetch()
      time.sleep(self.interval)

def handler(signum, frame):
  res = input("Ctrl-c was pressed. Do you want to exit? y/n ")
  if res == 'y':
    exit(1)

def main():
  logging.info("Starting exporter...")

  interval = int(os.getenv("INTERVAL", "5"))
  app_port = int(os.getenv("APP_PORT", "80"))
  exp_port = int(os.getenv("EXP_PORT", "9877"))

  app_metrics = AppMetrics(
    app_port  = app_port,
    interval  = interval
  )

  signal.signal(signal.SIGINT, handler)

  start_http_server(exp_port)
  app_metrics.run()

if __name__ == "__main__":
  main()
