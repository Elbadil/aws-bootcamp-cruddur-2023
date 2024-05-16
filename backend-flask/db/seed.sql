
INSERT INTO public.users (display_name, handle, cognito_user_id)
VALUES
    ('Adel Elb', 'elbadil' ,'MOCK'),
    ('Andrew Brown', 'andrew' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES (
    (SELECT uuid from public.users WHERE users.handle = 'elbadil' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
);
