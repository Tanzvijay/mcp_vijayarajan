from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastmcp import FastMCP
from sqlalchemy import text


mcp = FastMCP()


URL_DATABASE = 'postgresql://postgres:Amma123@localhost:5432/Data1'

engine = create_engine(URL_DATABASE)



@mcp.tool()
def list_tables(self, schema: str = "public") -> list:
    """List all tables in a specific PostgreSQL schema using a raw query."""
    # Use :schema as a named parameter to prevent SQL injection
    query = text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = :schema 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """)
    
    with engine.connect() as connection:
        # Execute and fetch all results
        result = connection.execute(query, {"schema": schema})
        # Use .scalars() to get a flat list of names if using SQLAlchemy 2.0+
        return [row[0] for row in result.fetchall()]



@mcp.tool()
def select_from_table(self, table_name: str, limit: int = 10) -> list:
    """Select and display rows from a specific table."""
    # We use a f-string for table_name because identifiers cannot be parameterized 
    # in standard SQL, but we should validate it or use quoted identifiers for safety.
    query = text(f'SELECT * FROM "{table_name}" LIMIT :limit')
    
    with engine.connect() as connection:
        result = connection.execute(query, {"limit": limit})
        
        # result.mappings() converts each row into a dictionary-like object 
        # that uses column names as keys.
        return [dict(row) for row in result.mappings().all()]



if __name__ == "__main__":
    print("🚀 Starting Calculator MCP Server on http://localhost:8123")
    print("📋 Available tools: add, subtract, multiply, send_all_results")
    mcp.run(
        transport="http",
        port=8126
    )
