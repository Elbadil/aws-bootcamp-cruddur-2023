SELECT 
    uuid,
    display_name,
    handle
FROM users
WHERE cognito_user_id = %s LIMIT 1
