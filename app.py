from __future__ import annotations
from flask import Flask, render_template, abort
import requests
from typing import Any, Dict, List

API = "https://apifakedelivery.vercel.app"
app = Flask(__name__)

# ------- Helpers de API (com tolerância a campos) -------

def fetch_json(path: str) -> Any:
    url = f"{API}{path}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[ERRO] GET {url}: {e}")
        return None

def field(d: Dict[str, Any], *names, default=""):
    """Pega o primeiro campo existente entre vários possíveis."""
    for n in names:
        if d.get(n) not in (None, "", []):
            return d.get(n)
    return default

# ------- Rotas de páginas -------

@app.route("/")
def home():
    # Carrega um “resumo” para a home (recomendados)
    foods = fetch_json("/foods") or []
    restaurants = fetch_json("/restaurants") or []

    # Pega alguns itens para vitrines
    recommended_foods = foods[:8]
    recommended_restaurants = restaurants[:10]

    return render_template(
        "home.html",
        foods=recommended_foods,
        restaurants=recommended_restaurants,
        field=field
    )

# ----- Users -----

@app.route("/users")
def users():
    data = fetch_json("/users")
    if data is None:
        abort(502)
    return render_template("users.html", users=data, field=field)

@app.route("/users/<int:user_id>")
def user_detail(user_id: int):
    data = fetch_json(f"/users/{user_id}")
    if data is None:
        abort(404)
    return render_template("user_detail.html", user=data, field=field)

# ----- Restaurants -----

@app.route("/restaurants")
def restaurants():
    data = fetch_json("/restaurants")
    if data is None:
        abort(502)
    return render_template("restaurants.html", restaurants=data, field=field)

@app.route("/restaurants/<int:rest_id>")
def restaurant_detail(rest_id: int):
    data = fetch_json(f"/restaurants/{rest_id}")
    if data is None:
        abort(404)
    return render_template("restaurant_detail.html", restaurant=data, field=field)

# ----- Foods -----

@app.route("/foods")
def foods():
    data = fetch_json("/foods")
    if data is None:
        abort(502)
    return render_template("foods.html", foods=data, field=field)

@app.route("/foods/<int:food_id>")
def food_detail(food_id: int):
    data = fetch_json(f"/foods/{food_id}")
    if data is None:
        abort(404)
    return render_template("food_detail.html", food=data, field=field)

# ------- Run local -------
if __name__ == "__main__":
    app.run(debug=True)
