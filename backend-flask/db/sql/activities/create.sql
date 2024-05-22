INSERT INTO activities (user_uuid, message, expires_at)
VALUES (
    (SELECT uuid FROM public.users
    WHERE users.handle = %s LIMIT 1),
    %s,
    %s
)
