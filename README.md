# Backend

## Deployed Link
[Access Backend API](https://value-glance-backend.vercel.app/)
By default, the backend is configured to allow requests only from the deployed frontend (`https://value-glance-frontend.vercel.app`) and from any local `localhost` domains.
If you want to modify the CORS policy to allow requests from other domains, you can update the `CORS` configuration in the backend code.

## Run Locally
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. Create a `.env` file and add the following environment variables:
    ```bash
    DATABASE_URL=your-database-url
    API_KEY=your-api-key
    ```
    Get your free API key at [Financial Modeling Prep](https://site.financialmodelingprep.com/developer/docs#income-statements-financial-statements)
   
4. Install backend dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Run the backend:
    ```bash
    python app.py
    ```
    or
   ```bash
    flask run
    ```

### API Documentation

#### Get Income Statement
- **URL**: `/get_income-statement`
- **Method**: `GET`
- **Description**: Retrieve the latest financial data.

#### Filter Data
- **URL**: `/filter`
- **Method**: `GET`
- **Query Parameters**:
  - `dateRange.start`: Start year
  - `dateRange.end`: End year
  - `revenue.min`: Minimum revenue
  - `revenue.max`: Maximum revenue
  - `netIncome.min`: Minimum net income
  - `netIncome.max`: Maximum net income
  - `sortBy`: Sort by field (`date`, `revenue`, `netIncome`)
  - `order`: Sort order (`asc` or `desc`)

### Backend Database

The project uses **PostgreSQL** as the database. To run the backend locally, you need to configure the database connection.

1. Install PostgreSQL and create a database.
2. Update the `DATABASE_URL` in the `.env` file to point to your own database.
