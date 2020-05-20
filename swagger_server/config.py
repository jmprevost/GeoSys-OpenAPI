import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from flask_admin import Admin


os.environ["GAPI_PGIS_CONNECT_READ_ONLY_STRING"] = "postgresql://jmp_view:dev@v-she-olrik:14180/metriques_dev"

engine_view = create_engine(os.environ.get("GAPI_PGIS_CONNECT_READ_ONLY_STRING"), convert_unicode=True)
db_view_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine_view))

os.environ["GAPI_PGIS_CONNECT_ADMIN_STRING"] = "postgresql://jmp_api:dev@v-she-olrik:14180/metriques_dev"
os.environ["GAPI_CRYPTO_ITERATION"] = "121394"
os.environ["GAPI_CRYPTO_SALT"] = "GeoSys API salt for crypto!!!"
os.environ["GAPI_JWT_ALGORITHM"] = "HS256"

os.environ["GAPI_ENV"] = "DEV"

os.environ["GAPI_EPSG"] = "4617"
os.environ["GAPI_GEOJSON_MAX_DECIMAL"] = "7"
os.environ["GAPI_GEOJSON_PGIS_OPTION"] = "2"
os.environ["GAPI_GEOJSON_TOL_FILTRAGE"] = "0.000005"

os.environ["GAPI_AWS_REGION"] = "ca-central-1"
os.environ["GAPI_AWS_S3_BUCKET_NAME"] = "mytestjmp"
os.environ["AWS_CA_BUNDLE"] = "D:\\GeoSys\\certificats\\NRCan-RootCA.cer" #il faudrait essayer de mettre le certificat dans le docker et ensuite donner son path
os.environ["GAPI_AWS_S3_MULTI_PART_CHUNK_SIZE"] = "10485760"

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir='./swagger/')

# Get the underlying Flask app instance
app = connex_app.app

# L'application flask gère le CORS. Chaque requête à l'API passe par CORS
CORS(app)

# Build the Sqlite ULR for SqlAlchemy
#pgis_url = "postgresql://jmp_api:dev@v-she-olrik:14180/metriques_dev"
pgis_url = os.environ.get("GAPI_PGIS_CONNECT_ADMIN_STRING")

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = False #À True, il permet de voir les requêtes SQL exécutées par SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = pgis_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_SORT_KEYS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
#app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app, session_options={'autocommit': False})

# Initialize Marshmallow
ma = Marshmallow(app)





# set optional bootswatch theme
# see http://bootswatch.com/3/ for available swatches
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create admin
admin = Admin(app, 'Geosys Admin', template_mode='bootstrap3')
