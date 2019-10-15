## Take-Home Test - Game Review Site

#### Requirements

- Docker (tested with 18.09)
- Make

#### Brief Overview

This simple gaming review blog is written in Python with the Django Web Framework. The project uses `make` with `docker` to create and run the images required for running the application and its tests.

Most (but not all) of the dev work can be found under the `blog/` subfolder in the following files:

```
project root
-- ...
-- blog
---- ...
---- admin.py
---- models.py
---- tests.py
---- urls.py
---- views.py
```

#### Running

```
# will build the application container and run it
# the project can be seen at localhost:8000
make run
```

#### Testing

```
# builds the test containers and runs the backend tests
make test
```

#### Note

An admin panel can be found at `localhost:8000/admin`. For your convenience you can login with the credentials: 

`u: nick p: eagamingblog`

#### Frontend

The frontend is pretty sweet tell me what you think of that wicked UX I've come up with (please forgive me).