from graphql_app import create_app

application = app = create_app()

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5042)
