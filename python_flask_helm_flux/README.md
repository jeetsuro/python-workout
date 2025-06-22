SQLAlchemy() vs sqlalchemy.orm
------------------------------
If we use sqlalchemy.orm instead of SQLAlchemy(), we need to explicitly manage our database connections and sessions. 
SQLAlchemy() (from flask_sqlalchemy) provides a higher-level abstraction for Flask, handling session lifecycle, model registration, and database integration seamlessly. 
However, using sqlalchemy.orm directly gives you more control but requires manual session management.

Features :
- In-memory SQL-lite connection
- Flask based CRUD operations
- Pyetest based taste code
- pylint support 
- guicorn spawns our flask app
- Flask support


