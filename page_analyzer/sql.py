URLS = """
SELECT
    id,
    name,
    created_at
FROM
    urls;
"""

LAST_CHECKS = """
SELECT DISTINCT ON (url_id)
    url_id as id,
    created_at as last_check_date,
    status_code as last_check_status_code
FROM
    url_checks
ORDER BY
    url_id,
    created_at DESC;
"""

DETAIL = """
SELECT
    id,
    name,
    created_at
FROM
    urls
WHERE
    id = %s
"""

FIND_ID = """
SELECT
    id
FROM
    urls
WHERE
    name = %s
LIMIT
    1;
"""

FIND_URL = """
SELECT
    name
FROM
    urls
WHERE
    id = %s
LIMIT
    1;
"""

CHECKS = """
SELECT
    id,
    created_at,
    status_code,
    h1,
    title,
    description
FROM
    url_checks
WHERE
    url_id = %s
ORDER BY
    id
"""

NEW_ENTRY = """
INSERT INTO
    urls (name, created_at)
VALUES
    (%s, %s)
RETURNING
    id;
"""

NEW_CHECK = """
INSERT INTO
    url_checks (url_id, created_at, status_code, title, h1, description)
VALUES
    (%s, %s, %s, %s, %s, %s)
RETURNING
    id;
"""
