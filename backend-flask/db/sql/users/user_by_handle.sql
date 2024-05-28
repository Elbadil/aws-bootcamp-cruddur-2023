SELECT
    uuid,
    display_name,
    handle
FROM users
WHERE handle = %s LIMIT 1
