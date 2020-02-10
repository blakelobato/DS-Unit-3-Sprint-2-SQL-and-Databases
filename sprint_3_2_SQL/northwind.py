import sqlite3
conn = sqlite3.connect('northwind_small.sqlite3')
cursor = conn.cursor()
#if connected there should be demo_data.sqlite3 file where we are currently working so print this if that is the case
print('No errors on connection')


#### SPRINT PART 2 ####


#---------------------------------------
#- What are the ten most expensive items (per unit price) in the database?
cursor.execute('''SELECT ProductName, UnitPrice FROM Product ORDER BY UnitPrice DESC Limit 10;''')
print(cursor.fetchall())

# SELECT ProductName, UnitPrice
# FROM Product
# ORDER BY UnitPrice DESC
# LIMIT 10



#------------------------------------------------------
#What is the average age of an employee at the time of their hiring? (Hint: a lot of arithmetic works with dates.)
cursor.exectue('''SELECT ROUND(AVG(HireDate - BirthDate))
FROM Employee);'''
print(cursor.fetchall())

# SELECT ROUND(AVG(HireDate - BirthDate))
# FROM Employee




#-------------------------------------------------------
#(*Stretch*) How does the average age of employee at hire vary by city?
cursor.execute('''SELECT City, ROUND(AVG(HireDate - BirthDate)) FROM Employee GROUP BY City''';)
print(cursor.fetchall())

# SELECT City, ROUND(AVG(HireDate - BirthDate))
# FROM Employee
# GROUP BY City;




#### SPRINT PART 3 ####

#What are the ten most expensive items (per unit price) in the database *and* their suppliers?
cursor.execute('''SELECT ProductName, UnitPrice, CompanyName FROM Product JOIN Supplier ON product.SupplierId = supplier.Id ORDER BY UnitPrice DESC LIMIT 10;''')
print(cursor.fetchall())

# SELECT ProductName, UnitPrice, CompanyName
# FROM Product
# JOIN Supplier ON product.SupplierId = supplier.Id
# ORDER BY UnitPrice DESC
# LIMIT 10


#What is the largest category (by number of unique products in it)?
cursor.execute('''SELECT COUNT(ProductName), CategoryName FROM Product JOIN Category ON Product.CategoryId=Category.Id GROUP BY CategoryId ORDER BY COUNT(CategoryId) DESC LIMIT 1;''')
print(cursor.fetchall())

# SELECT COUNT(ProductName), CategoryName
# FROM Product
# JOIN Category ON Product.CategoryId=Category.Id
# GROUP BY CategoryId
# ORDER BY COUNT(CategoryId) DESC
# LIMIT 1



#(*Stretch*) Who's the employee with the most territories? Use `TerritoryId` (not name, region, or other fields) as the unique identifier for territories.
cursor.execute('''SELECT COUNT(TerritoryID), FirstName, LastName FROM Employee JOIN EmployeeTerritory ON Employee.Id = EmployeeTerritory.EmployeeId GROUP BY Employee.Id ORDER BY COUNT(TerritoryId) DESC;''')
print(cursor.fetchall())

# SELECT COUNT(TerritoryID), FirstName, LastName
# FROM Employee
# JOIN EmployeeTerritory ON Employee.Id = EmployeeTerritory.EmployeeId
# GROUP BY Employee.Id
# ORDER BY COUNT(TerritoryId) DESC