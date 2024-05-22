
INSERT INTO public.users (display_name, handle, email, cognito_user_id)
VALUES
    ('Adel Elb', 'elbadil', 'adel@blog.com', 'MOCK'),
    ('Andrew Brown', 'andrew', 'andrew@blog.com', 'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES (
    (SELECT uuid from public.users WHERE users.handle = 'elbadil' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
);

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES (
    (SELECT uuid from public.users WHERE users.handle = 'andrew' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '12 day'
);
