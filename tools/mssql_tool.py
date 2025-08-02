import pyodbc
import os
from typing import Optional, List
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

MSSQL_SERVER = os.getenv("MSSQL_SERVER")
MSSQL_DATABASE = os.getenv("MSSQL_DATABASE")
MSSQL_USERNAME = os.getenv("MSSQL_USERNAME")
MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD")




def get_mssql_connection():
    """
    Establish and return a connection to the MSSQL database using pyodbc.
    """
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={MSSQL_SERVER};"
        f"DATABASE={MSSQL_DATABASE};"
        f"UID={MSSQL_USERNAME};"
        f"PWD={MSSQL_PASSWORD}"
    )
    return pyodbc.connect(conn_str)


@tool
def get_employee_login_details(emp_code: Optional[str] = None) -> List[tuple]:
    """
    Fetch login-related employee details from [LOGIN_APP] table.

    Args:
        emp_code: Optional employee code to filter specific employee's login info.

    Returns:
        List of tuples containing:
        ID, LoginAPPCode, EmpCode, UserName, Password, IMEI, CompanyCode, Company,
        BranchCode, Branch, Mobile, Email, Region, Designation, DOJ, CreatedDate,
        UnitCode, UnitName, BILLABLETYPE
    """
    conn = get_mssql_connection()
    cursor = conn.cursor()

    query = """
        SELECT TOP 1000 [ID], [LoginAPPCode], [EmpCode], [UserName], [Password],
        [IMEI], [CompanyCode], [Company], [BranchCode], [Branch], [Mobile], [Email],
        [Region], [Designation], [DOJ], [CreatedDate], [UnitCode], [UnitName], [BILLABLETYPE]
        FROM [Monitoring_DB_Live].[dbo].[LOGIN_APP]
    """

    if emp_code:
        query += " WHERE EmpCode = ?"
        cursor.execute(query, emp_code)
    else:
        cursor.execute(query)

    result = cursor.fetchall()
    conn.close()
    return [tuple(row) for row in result]


@tool
def get_employee_personal_details(emp_id: Optional[int] = None) -> List[tuple]:
    """
    Fetch personal details from [Employee_PersonalDetails] table.

    Args:
        emp_id: Optional EmployeeID to fetch a specific employee's personal info.

    Returns:
        List of tuples containing:
        EmployeeID, FathersName, MothersName, Religion,
        BloodRelationWithExistingEmployee, NameOfFamilyMember
    """
    conn = get_mssql_connection()
    cursor = conn.cursor()

    query = """
        SELECT TOP 1000 [EmployeeID], [FathersName], [MothersName],
        [Religion], [BloodRelationWithExistingEmployee], [NameOfFamilyMember]
        FROM [Monitoring_DB_Live].[dbo].[Employee_PersonalDetails]
    """

    if emp_id:
        query += " WHERE EmployeeID = ?"
        cursor.execute(query, emp_id)
    else:
        cursor.execute(query)

    result = cursor.fetchall()
    conn.close()
    return [tuple(row) for row in result]


@tool
def get_unit_details(unit_code: Optional[str] = None) -> List[tuple]:
    """
    Fetch full unit/site details from [UnitMaster] table.

    Args:
        unit_code: Optional UnitCode to filter specific site details.

    Returns:
        List of tuples containing:
        ID, companyId, compname, officeTypeID, officename, ClientCode, ClientName,
        UnitCode, UnitName, IsActive, CreatedDate, CreatedBy, fk_branchId, fk_stateid,
        fk_cityid, address, Area_Locality, land_mark, district_address, pincode_address,
        fk_empid, FoEmpCode, FoEmpName, FoEmpDesig, FoMobileNo, FoEmail, FoCompany,
        FoBranch, FoRegion, fk_companyId_sup, fk_ClientId, pk_locid, CityName, RegionName,
        StateName, OpeningDate, AppDesignation
    """
    conn = get_mssql_connection()
    cursor = conn.cursor()

    query = """
        SELECT TOP 1000 [ID], [companyId], [compname], [officeTypeID], [officename],
        [ClientCode], [ClientName], [UnitCode], [UnitName], [IsActive], [CreatedDate],
        [CreatedBy], [fk_branchId], [fk_stateid], [fk_cityid], [address], [Area_Locality],
        [land_mark], [district_address], [pincode_address], [fk_empid], [FoEmpCode],
        [FoEmpName], [FoEmpDesig], [FoMobileNo], [FoEmail], [FoCompany], [FoBranch],
        [FoRegion], [fk_companyId_sup], [fk_ClientId], [pk_locid], [CityName], [RegionName],
        [StateName], [OpeningDate], [AppDesignation]
        FROM [Monitoring_DB_Live].[dbo].[UnitMaster]
    """

    if unit_code:
        query += " WHERE UnitCode = ?"
        cursor.execute(query, unit_code)
    else:
        cursor.execute(query)

    result = cursor.fetchall()
    conn.close()
    return [tuple(row) for row in result]


@tool
def mssql_query_tool(query: str) -> List[tuple]:
    """
    Execute a custom SQL query directly on the connected MSSQL database.
    
    Args:
        query: The full SQL SELECT query to run.
    
    Returns:
        List of result rows (tuples).
    """
    conn = get_mssql_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return [tuple(row) for row in result]


@tool
def list_all_mssql_objects() -> List[str]:
    """
    List all tables and views in the connected MSSQL database.

    Returns:
        List of object (table/view) names.
    """
    conn = get_mssql_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE IN ('BASE TABLE', 'VIEW')
    """)
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results]


@tool
def get_table_columns(table_name: str) -> List[str]:
    """
    Get all column names for a specific table.

    Args:
        table_name: Name of the table to inspect.

    Returns:
        List of column names.
    """
    conn = get_mssql_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = ?
    """, table_name)
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results]


# Exported tool list
__all__ = [
    "get_employee_login_details",
    "get_employee_personal_details",
    "get_unit_details",
    "mssql_query_tool",
    "list_all_mssql_objects",
    "get_table_columns"
]
