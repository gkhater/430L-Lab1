from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost:3306/exchange"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    usd_amount = db.Column(db.Float, nullable=False)
    lbp_amount = db.Column(db.Float, nullable=False)
    usd_to_lbp = db.Column(db.Boolean, nullable=False)

@app.route("/hello", methods=["GET"])
def hello_world():
    return "Hello World!"

@app.route("/transaction", methods=["POST"])
def create_transaction():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    for k in ["usd_amount", "lbp_amount", "usd_to_lbp"]:
        if k not in data:
            return jsonify({"error": f"Missing field: {k}"}), 400

    tx = Transaction(
        usd_amount=float(data["usd_amount"]),
        lbp_amount=float(data["lbp_amount"]),
        usd_to_lbp=bool(data["usd_to_lbp"]),
    )

    db.session.add(tx)
    db.session.commit()

    return jsonify({"message": "Transaction created", "id": tx.id}), 201

if __name__ == "__main__":
    app.run(debug=True)
