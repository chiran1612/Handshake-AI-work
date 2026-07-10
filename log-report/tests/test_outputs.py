import json
import re
from collections import Counter
from pathlib import Path


REPORT = Path("/app/report.json")
ACCESS_LOG = Path("/app/access.log")


def expected_report():
    paths = Counter()
    ips = set()
    total = 0

    for raw_line in ACCESS_LOG.read_text().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        total += 1
        ips.add(line.split()[0])
        request = re.search(r'"[A-Z]+\s+(\S+)\s+HTTP/[^\"]+"', line)
        assert request is not None, f"malformed fixture line: {line}"
        paths[request.group(1)] += 1

    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0],
    }


def _load_report():
    assert REPORT.is_file(), "report.json not found"
    try:
        return json.loads(REPORT.read_text())
    except json.JSONDecodeError as exc:
        raise AssertionError(f"report.json is not valid JSON: {exc}") from exc


# Criterion 1: Read /app/access.log and parse each non-empty line.
# Criterion 2: Write /app/report.json as a valid JSON object with
#              total_requests, unique_ips, and top_path.
def test_report_exists_and_is_valid_json():
    """Verify criterion 1+2: report.json is produced and is parseable JSON."""
    data = _load_report()
    assert isinstance(data, dict), "report must be a JSON object"


# Criterion 2 (values): total_requests, unique_ips, and top_path
#                        must match the ground truth derived from access.log.
def test_report_values_are_correct():
    """Verify criterion 2: field values match the access log."""
    actual = _load_report()
    assert actual == expected_report(), (
        f"expected {expected_report()}, got {actual}"
    )


# Criterion 3: total_requests and unique_ips are JSON integers,
#              top_path is a JSON string.
def test_report_field_types():
    """Verify criterion 3: integer types for counts, string for top_path."""
    actual = _load_report()
    assert isinstance(actual["total_requests"], int), "total_requests must be int"
    assert isinstance(actual["unique_ips"], int), "unique_ips must be int"
    assert isinstance(actual["top_path"], str), "top_path must be str"


# Criterion 4: No additional fields beyond the three listed.
def test_report_has_no_extra_fields():
    """Verify criterion 4: only total_requests, unique_ips, top_path."""
    actual = _load_report()
    assert set(actual) == {"total_requests", "unique_ips", "top_path"}, (
        f"unexpected keys: {set(actual) - {'total_requests', 'unique_ips', 'top_path'}}"
    )
