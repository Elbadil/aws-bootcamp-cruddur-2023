UPDATE users
SET cognito_user_id = %(cognito_id)s
WHERE handle = %(handle)s
