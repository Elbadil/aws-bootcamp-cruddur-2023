SELECT
    activities.uuid,
    users.display_name,
    users.handle,
    activities.message,
    activities.created_at,
    activities.expires_at
FROM activities
LEFT JOIN users
ON users.uuid = activities.user_uuid
WHERE activities.uuid = %s
