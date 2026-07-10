1. Read the file `/app/access.log` and parse each non-empty line.
2. Write `/app/report.json` as a valid JSON object with exactly these fields:
   - `total_requests` (integer): the number of non-empty log lines
   - `unique_ips` (integer): the number of distinct client IP addresses (the first whitespace-separated field on each non-empty line)
   - `top_path` (string): the request path occurring most often, extracted from the quoted HTTP request (e.g., `"GET /index.html HTTP/1.1"`); if counts tie, use the path that appears first in the log
3. All numeric fields must be JSON integers and `top_path` must be a JSON string.
4. Do not include any additional fields beyond the three listed above.
