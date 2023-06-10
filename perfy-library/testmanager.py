import sys

import requests
import time
import threading
import argparse
import matplotlib.pyplot as plt
import numpy as np
from jinja2 import Environment, FileSystemLoader

from json_loader.generators.json_schema_generator import generate
from json_loader.json_schema_loader import JSONSchemaLoader

# Set constants
# CONCURRENT_REQUESTS = int(args.cr or 1)
# WAITING_TIME = int(args.wt or 1)
# METHOD = (args.method or 'GET')
# URL = (args.url or "https://www.google.com")
# DURATION = int(args.duration or 7)
# HAS_BODY = bool(args.body or False)
# TIMEOUT = int(args.timeout or 60)


def execute_test(task=None, tasks_results_collection=None, tasks_collection=None):
    CONCURRENT_REQUESTS = None
    WAITING_TIME = None
    METHOD = None
    URL = None
    DURATION = None
    HAS_BODY = None
    TIMEOUT = None
    BODY_SCHEMA_FILENAME = None
    IS_FROM_EXECUTOR = False
    EXPECTED_ERROR_RATE = None
    EXPECTED_MAX_TIME_P90 = None
    EXPECTED_MAX_TIME_P95 = None
    EXPECTED_MAX_TIME_P99 = None
    IS_PIPELINE = None

    if task is None:
        parser = argparse.ArgumentParser()
        parser.add_argument('--cr', type=int, help='Number of concurrent requests to send (default 1)')
        parser.add_argument('--wt', type=int, help='Number of seconds to wait between requests (default 1)')
        parser.add_argument('--url', help='URL to send requests to')
        parser.add_argument('--method', help='HTTP Method required for URL tested')
        parser.add_argument('--duration', type=int, help='Duration of the test in seconds')
        parser.add_argument('--body', type=bool, help='Do requests use request-body')
        parser.add_argument('--timeout', type=int,
                            help='Number of seconds to wait as timeout for requests (default 60)')
        parser.add_argument('--expected_error_rate', type=int, help='Expected percentage of error status codes (from '
                                                                    '0 to 1)')
        parser.add_argument('--expected_max_response_time_p90', type=float, help='Maximum time for P90 percentile')
        parser.add_argument('--expected_max_response_time_p95', type=float, help='Maximum time for P95 percentile')
        parser.add_argument('--expected_max_response_time_p99', type=float, help='Maximum time for P99 percentile')
        parser.add_argument('--is_pipeline', type=bool, help='Does test run in a CI CD pipeline')
        args = parser.parse_args()

        CONCURRENT_REQUESTS = int(args.cr or 1)
        WAITING_TIME = int(args.wt or 1)
        METHOD = (args.method or 'GET')
        URL = (args.url or "https://www.google.com")
        DURATION = int(args.duration or 7)
        HAS_BODY = bool(args.body or False)
        TIMEOUT = int(args.timeout or 60)
        BODY_SCHEMA_FILENAME = 'schema.json'
        EXPECTED_ERROR_RATE = int(args.expected_error_rate or 1)
        EXPECTED_MAX_TIME_P90 = float(args.expected_max_response_time_p90 or TIMEOUT + 1)
        EXPECTED_MAX_TIME_P95 = float(args.expected_max_response_time_p95 or TIMEOUT + 1)
        EXPECTED_MAX_TIME_P99 = float(args.expected_max_response_time_p99 or TIMEOUT + 1)
        IS_PIPELINE = bool(args.is_pipeline or False)

    else:
        CONCURRENT_REQUESTS = task['cr']
        WAITING_TIME = task['wt']
        METHOD = task['method']
        URL = task['url']
        DURATION = task['duration']
        HAS_BODY = task['body']
        TIMEOUT = task['timeout']
        BODY_SCHEMA_FILENAME = task['schema_filename']
        IS_FROM_EXECUTOR = True
        EXPECTED_ERROR_RATE = 1
        EXPECTED_MAX_TIME_P90 = TIMEOUT + 1
        EXPECTED_MAX_TIME_P95 = TIMEOUT + 1
        EXPECTED_MAX_TIME_P99 = TIMEOUT + 1
        IS_PIPELINE = False

    # Define empty lists to store response data
    response_times = []
    response_statuses = []
    schema_loader = JSONSchemaLoader(BODY_SCHEMA_FILENAME)
    request_body_schema = None
    if HAS_BODY:
        request_body_schema = schema_loader.parse_json_schema()

    # Send CONCURRENT_REQUESTS concurrent requests every WAITING_TIME seconds for one minute
    start_time = time.time()
    end_time = start_time + DURATION

    def send_requests():
        # Send request and measure response time

        request_body = None
        if HAS_BODY:
            request_body = generate(request_body_schema)

        start_time = time.time()
        try:
            if METHOD == 'GET':
                response = requests.get(URL, timeout=TIMEOUT)
            elif METHOD == 'POST':
                response = requests.post(URL, json=request_body, timeout=TIMEOUT)
            elif METHOD == 'PUT':
                response = requests.put(URL, json=request_body, timeout=TIMEOUT)
            elif METHOD == 'PATCH':
                response = requests.patch(URL, json=request_body, timeout=TIMEOUT)
            elif METHOD == 'DELETE':
                response = requests.delete(URL, json=request_body, timeout=TIMEOUT)
            else:
                raise NotImplemented("Method " + METHOD + " not supported yet")
        except:
            response = requests.Response()
            response.status_code = 500
        finally:
            end_time = time.time()

        # Store response status and response time
        status = response.status_code
        response_time = end_time - start_time
        response_statuses.append(status)
        response_times.append(response_time)

        print(f"Request: Status {status}, Response Time {response_time:.2f}s")

    threads = []
    while time.time() < end_time:
        for i in range(CONCURRENT_REQUESTS):
            # Start CONCURRENT_REQUESTS threads to send concurrent requests
            thread = threading.Thread(target=send_requests)
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Wait WAITING_TIME seconds before sending the next batch of requests
        time.sleep(WAITING_TIME)

    # Print the total duration of the test
    total_time = time.time() - start_time
    print(f"Test duration: {total_time:.5f}s")

    test_result = 'PASSED'

    # Create bar graph of response statuses and their counts
    all_statuses = [200, 400, 404, 500]

    # Calculate counts for each status code
    counts = [response_statuses.count(s) for s in all_statuses]
    error_status_codes = float(counts[1] + counts[2] + counts[3])
    total_status_codes = float(sum(counts))

    if error_status_codes / total_status_codes > EXPECTED_ERROR_RATE:
        test_result = 'FAILED'

    # Create bar graph with all status codes and their counts
    plt.bar(range(len(all_statuses)), counts)
    plt.title("Response Statuses and Their Counts")
    plt.xlabel("Response Statuses")
    plt.ylabel("Counts")
    plt.xticks(range(len(all_statuses)), all_statuses)
    plt.savefig('bar_graph.png')

    # Calculate response time percentiles
    p90 = np.percentile(response_times, 90)
    p95 = np.percentile(response_times, 95)
    p99 = np.percentile(response_times, 99)
    print(f"P90: {p90:.5f}s")
    print(f"P95: {p95:.5f}s")
    print(f"P99: {p99:.5f}s")

    if p90 > EXPECTED_MAX_TIME_P90:
        test_result = 'FAILED'

    if p95 > EXPECTED_MAX_TIME_P95:
        test_result = 'FAILED'

    if p99 > EXPECTED_MAX_TIME_P99:
        test_result = 'FAILED'

    print("Test result: " + test_result)
    if IS_PIPELINE:
        if test_result == 'PASSED':
            sys.exit(0)
        else:
            sys.exit(1)

    # Create line graph of response time evolution
    plt.clf()
    x_ticks = np.arange(len(response_times))
    plt.plot(x_ticks, response_times)
    plt.title("Response Time Evolution")
    plt.xlabel("Requests")
    plt.ylabel("Response Time (s)")
    plt.savefig('line_graph.png')

    # Render the template with the data
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('result_template.html')
    html_output = template.render(p90=p90, p95=p95, p99=p99, total_time=total_time,
                                  bar_graph='bar_graph.png', line_graph='line_graph.png',
                                  num_requests=CONCURRENT_REQUESTS, request_interval=WAITING_TIME, url=URL,
                                  test_duration=DURATION, http_method=METHOD, request_timeout=TIMEOUT)

    # Write the HTML output to a file
    with open('output.html', 'w') as f:
        if IS_FROM_EXECUTOR is False:
            f.write(html_output)
        else:
            tasks_results_collection.insert_one({
                'data': html_output,
                'results': {
                    'p90': p90,
                    'p95': p95,
                    'p99': p99,
                    'status_counts': counts,
                    'time_evolution': response_times
                },
                'task_id': task['_id']
            })

            update = {'$set': {'status': 'COMPLETED'}}
            tasks_collection.update_one({'_id': task['_id']}, update)


if __name__ == "__main__":
    execute_test()
