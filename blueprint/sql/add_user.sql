insert into users(u_id,
                  name,
                  surname,
                  email,
                  login,
                  hash_password)
values (DEFAULT,
        '$name',
        '$surname',
        '$email',
        '$login',
        '$hash_password')