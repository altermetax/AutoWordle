from flask import Flask, request, render_template, session, abort
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix
from .session_game_manager import SessionGameManager
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    
    Session(app)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def root():
        return render_template("index.html")

    @app.route("/play/<game_type_id>")
    def play(game_type_id):
        if game_type_id not in ["wordle", "absurdle"]:
            abort(400, "Invalid game type id")
            return

        if "game_manager" in session:
            game_manager = session.get("game_manager")
        else:
            game_manager = SessionGameManager()
            session["game_manager"] = game_manager

        game_id = game_manager.new_game(game_type_id, app.root_path)

        game_name = "AutoWordle" if game_type_id == "wordle" else "AutoAbsurdle"
        return render_template("game.html", game_id=game_id, game_type_id=game_type_id, game_name=game_name)

    @app.route("/guess/<game_id>")
    def guess(game_id):
        if "game_manager" not in session:
            abort(400, "No games started")
            return
        game_manager = session["game_manager"]

        word = request.args.get("word")
        if word is None:
            abort(400, "No word given")
            return

        game_id = int(game_id)

        result = game_manager.try_word(game_id, word)
        if result is None:
            abort(400, "Game doesn't exist")
        return result

    @app.route("/solve", methods=["POST"])
    def solve():
        return { "word": "QUICK" }

    return app