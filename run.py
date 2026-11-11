from app import create_app, db
from app.models import Product
from seed import run_seed

app = create_app()

with app.app_context():
    if Product.query.count() == 0:
        run_seed()

if __name__ == '__main__':
    app.run(debug=True)
