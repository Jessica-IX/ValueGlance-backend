import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, Float, Date, DateTime
from sqlalchemy import extract, asc, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from dotenv import load_dotenv

#from flask_migrate import Migrate
from sqlalchemy.pool import NullPool

app = Flask(__name__)

'''if 'DATABASE_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financial_data.db' 
'''
load_dotenv() 
'''db_url = os.environ.get('DATABASE_URL', '')
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)'''
#app.config['SQLALCHEMY_DATABASE_URI'] = db_url

db_url = os.environ.get('DATABASE_URL')
engine = create_engine(db_url, client_encoding='utf8', poolclass=NullPool)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES_URL')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
#migrate = Migrate(app, db)

# Frondend request only
CORS(app, resources={r"/*": {"origins": "https://jessica-ix.github.io/ValueGlance-fronend"}})
API_KEY = os.getenv('API_KEY')

"""class FinancialData(db.Model):
    __tablename__ = 'income_statement'
    date = db.Column(db.Date, primary_key=True)
    revenue = db.Column(db.BigInteger)
    grossProfit = db.Column(db.BigInteger)
    operatingIncome = db.Column(db.BigInteger)
    netIncome = db.Column(db.BigInteger)
    eps = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, date, revenue, grossProfit, operatingIncome, netIncome, eps):
        self.date = date
        self.revenue = revenue
        self.grossProfit = grossProfit
        self.operatingIncome = operatingIncome
        self.netIncome = netIncome
        self.eps = eps
        
    # For jsonify
    def to_dict(self):
        return {
            'date': self.date.strftime('%Y-%m-%d'),
            'revenue': self.revenue,
            'grossProfit': self.grossProfit,
            'operatingIncome': self.operatingIncome,
            'netIncome': self.netIncome,
            'eps': self.eps
        }
        
def init_db():
    db.create_all()
        
@app.route('/get_income-statement', methods=['GET'])
def get_data():
    last_updated_entry = db.session.query(FinancialData).order_by(FinancialData.last_updated.desc()).first()
    # At most 1 API request per day
    if last_updated_entry and (datetime.utcnow() - last_updated_entry.last_updated) < timedelta(days=1):
        data = FinancialData.query.all()
        print('use cached records')
        return jsonify([entry.to_dict() for entry in data])
    
    url = f'https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=annual&apikey={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        #print(f"Status Code: {response.status_code}")
        data = response.json()
        
        # Usually date-desc
        for item in data:
            date_obj=datetime.strptime(item['date'], '%Y-%m-%d').date()
            existing_entry = FinancialData.query.filter_by(date=date_obj).first()
            
            # Replace outdated
            if existing_entry:
                db.session.delete(existing_entry)
                db.session.commit()
                
            new_entry = FinancialData(
                date=date_obj,
                revenue=item['revenue'],
                grossProfit=item['grossProfit'],
                operatingIncome=item['operatingIncome'],
                netIncome=item['netIncome'],
                eps=item['eps'],
            )
            db.session.add(new_entry)
        db.session.commit()
        
        all_entries = db.session.query(FinancialData).all()
        return jsonify([entry.to_dict() for entry in all_entries])

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/filter', methods=['GET'])
def filter_data():
    # args are parsed properly by the frontend
    year_start = request.args.get('dateRange.start', type=int)
    year_end = request.args.get('dateRange.end', type=int)
    revenue_min = request.args.get('revenue.min', type=float)
    revenue_max = request.args.get('revenue.max', type=float)
    netIncome_min = request.args.get('netIncome.min', type=float)
    netIncome_max = request.args.get('netIncome.max', type=float)
    sort_by = request.args.get('sortBy')
    order = request.args.get('order')
    
    query = FinancialData.query.filter(
        extract('year', FinancialData.date) >= year_start,
        extract('year', FinancialData.date) <= year_end,
        FinancialData.revenue >= revenue_min,
        FinancialData.revenue <= revenue_max,
        FinancialData.netIncome >= netIncome_min,
        FinancialData.netIncome <= netIncome_max
    )
    
    if sort_by in ['date', 'revenue', 'netIncome']:
        column = getattr(FinancialData, sort_by, None)
        if column:
            query = query.order_by(asc(column) if order == 'asc' else desc(column))
            
    filtered_data = query.all()

    data_to_return = [entry.to_dict() for entry in filtered_data]
    #print(data_to_return)
    return jsonify(data_to_return)
"""
class FinancialData(Base):
    __tablename__ = 'income_statement'
    date = Column(Date, primary_key=True)
    revenue = Column(Integer)
    grossProfit = Column(Integer)
    operatingIncome = Column(Integer)
    netIncome = Column(Integer)
    eps = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)

    def __init__(self, date, revenue, grossProfit, operatingIncome, netIncome, eps):
        self.date = date
        self.revenue = revenue
        self.grossProfit = grossProfit
        self.operatingIncome = operatingIncome
        self.netIncome = netIncome
        self.eps = eps

    def to_dict(self):
        return {
            'date': self.date.strftime('%Y-%m-%d'),
            'revenue': self.revenue,
            'grossProfit': self.grossProfit,
            'operatingIncome': self.operatingIncome,
            'netIncome': self.netIncome,
            'eps': self.eps
        }

def init_db():
    Base.metadata.create_all(engine)

@app.route('/get_income-statement', methods=['GET'])
def get_data():
    last_updated_entry = session.query(FinancialData).order_by(FinancialData.last_updated.desc()).first()
    if last_updated_entry and (datetime.utcnow() - last_updated_entry.last_updated) < timedelta(days=1):
        data = session.query(FinancialData).all()
        print('use cached records')
        return jsonify([entry.to_dict() for entry in data])
    
    url = f'https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=annual&apikey={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        for item in data:
            date_obj = datetime.strptime(item['date'], '%Y-%m-%d').date()
            existing_entry = session.query(FinancialData).filter_by(date=date_obj).first()

            # Replace outdated
            if existing_entry:
                session.delete(existing_entry)
                session.commit()

            new_entry = FinancialData(
                date=date_obj,
                revenue=item['revenue'],
                grossProfit=item['grossProfit'],
                operatingIncome=item['operatingIncome'],
                netIncome=item['netIncome'],
                eps=item['eps'],
            )
            session.add(new_entry)
        session.commit()

        all_entries = session.query(FinancialData).all()
        return jsonify([entry.to_dict() for entry in all_entries])

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/filter', methods=['GET'])
def filter_data():
    # args are parsed properly by the frontend
    year_start = request.args.get('dateRange.start', type=int)
    year_end = request.args.get('dateRange.end', type=int)
    revenue_min = request.args.get('revenue.min', type=float)
    revenue_max = request.args.get('revenue.max', type=float)
    netIncome_min = request.args.get('netIncome.min', type=float)
    netIncome_max = request.args.get('netIncome.max', type=float)
    sort_by = request.args.get('sortBy')
    order = request.args.get('order')

    query = session.query(FinancialData).filter(
        extract('year', FinancialData.date) >= year_start,
        extract('year', FinancialData.date) <= year_end,
        FinancialData.revenue >= revenue_min,
        FinancialData.revenue <= revenue_max,
        FinancialData.netIncome >= netIncome_min,
        FinancialData.netIncome <= netIncome_max
    )

    if sort_by in ['date', 'revenue', 'netIncome']:
        column = getattr(FinancialData, sort_by, None)
        if column:
            query = query.order_by(asc(column) if order == 'asc' else desc(column))

    filtered_data = query.all()

    data_to_return = [entry.to_dict() for entry in filtered_data]
    return jsonify(data_to_return)

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run()
else:
    with app.app_context():
        init_db()