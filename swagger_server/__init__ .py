import os

print("Dans init")

os.environ["GAPI_PGIS_CONNECT_STRING"] = "postgresql://jmp_api:dev@v-she-olrik:14180/metriques_dev"

os.environ["GAPI_CRYPTO_ITERATION"] = "121394"

os.environ["GAPI_CRYPTO_SALT"] = "GeoSys API salt for crypto!!!"
