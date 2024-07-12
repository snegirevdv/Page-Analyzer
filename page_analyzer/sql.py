URLS = """
SELECT
    urls.id AS id,
    urls.name AS name,
    urls.created_at AS created_at,
    MAX(url_checks.created_at) AS last_check_date,
    (
        SELECT status_code
        FROM url_checks
        WHERE url_checks.url_id = urls.id
        ORDER BY id DESC
        LIMIT 1
    ) AS last_check_status_code
FROM
    urls
LEFT JOIN
    url_checks
ON
    urls.id = url_checks.url_id
GROUP BY
    urls.id, urls.name, urls.created_at
ORDER BY
    urls.id;
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
