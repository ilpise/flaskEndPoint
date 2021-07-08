import os

# from flask_migrate import MigrateCommand
# from flask_script import Manager

from app import create_app
# app = create_app("config.DevelopmentConfig")
# from app.commands import InitDbCommand

app = create_app()

# # Setup Flask-Script with command line commands
# manager = Manager(create_app)
# # manager.add_command('db', MigrateCommand)
# manager.add_command('init_db', InitDbCommand)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # manager.run(host='0.0.0.0', port=port)