import re


PATTERN = {
    'timestamp': r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [A-Z]{3,4}$',
}
PATTERN = { name: re.compile(regex) for name, regex in PATTERN.items() }

