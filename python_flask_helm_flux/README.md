My Project features :

- In-memory SQL-lite connection
- Flask based basic CRUD operations
- Pyetest based taste code
- pylint support 
- guicorn spawns our flask app
- Helm support (TBD)
- Flux GitOps (TBD)

NOTES :

- SQLAlchemy() vs sqlalchemy.orm
------------------------------
If we use sqlalchemy.orm instead of SQLAlchemy(), we need to explicitly manage our database connections and sessions. 
SQLAlchemy() (from flask_sqlalchemy) provides a higher-level abstraction for Flask, handling session lifecycle, model registration, and database integration seamlessly. 
However, using sqlalchemy.orm directly gives you more control but requires manual session management.

- Very boot-strap initial stage sqlalchemy engine was created as 'create_engine(DB_URI,connect_args={"check_same_thread": False})' to make SqlLite connections shareable across threads
- but when guicorn spawns multiple processes , under which each process, this flask app is running. so SqlLite connections was turned into very thread local/ scoped_session



