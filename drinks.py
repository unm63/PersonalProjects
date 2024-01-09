# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 10:52:05 2023

@author: ujwal
"""
#import mysql.connector
import math
import os
import pyodbc
import pymongo
print("So far so good");

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

mycol.drop();

mycol2 = mydb["orders"]

def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

connection = pyodbc.connect(driver='{SQL Server}', server='DESKTOP-48GBL2R\SQLEXPRESS', database='drinks',               
               trusted_connection='yes');
cursor = connection.cursor();

#if checkTableExists(connection, 'CustomerTable') == False:
    #print("It exists");
    #cursor.execute("DROP TABLE CustomerTable");
    #connection.commit();
#else:
   # cursor.execute(
   #     "CREATE TABLE CustomerTable(FirstName varchar(15), LastName varchar(15), GuestID varchar(15), AmountSpent float)");  # creates new table
   # connection.commit();

if checkTableExists(connection, 'CustomerTable') == True:
    cursor.execute("DROP TABLE CustomerTable");
    print("It's dropped");
    connection.commit();
cursor.execute(
    "CREATE TABLE CustomerTable(FirstName varchar(15), LastName varchar(15), GuestID varchar(15), AmountSpent float, DiscountPercentage float, BonusBucks integer)");  # creates new table
connection.commit();

CustomerArray = [];
PreferredCustomerArray = [];
print("Still good");
class Customer:
  def __init__(self, firstname, lastname, guestID, amountSpent):
    self.firstname = firstname
    self.lastname = lastname
    self.guestID = guestID
    self.amountSpent = amountSpent
    
  def set_Customer(self, customer):
      self.__make = customer
      
  def get_Customer(self):
      return self.__make
    
class PreferredCustomerGold(Customer):
  def __init__(self, firstname, lastname, guestID, amountSpent, discountPercentage):
    self.discountPercentage = discountPercentage
    Customer.__init__(self, firstname, lastname, guestID, amountSpent)
    
  def set_PreferredCustomerGold(self, customer):
       self.__gold = customer
       
  def get_PreferredCustomerGold(self):
       return self.__gold
   
    
class PreferredCustomerPlanum(Customer):
  def __init__(self, firstname, lastname, guestID, amountSpent, bonusBucks):
    self.bonusBucks = bonusBucks
    Customer.__init__(self, firstname, lastname, guestID, amountSpent)
    
  def set_PreferredCustomerPlanum(self, customer):
       self.__planum = customer
        
  def get_PreferredCustomerPlanum(self):
       return self.__planum

print("STILL GOOD");
if os.path.exists("customerarray.txt"):
    print("Welp");
    arrayy = [];
    with open("customerarray.txt") as file:
        for item in file:
            print("Yes");
            dictt = eval(item[:len(item)-1]);
            dicty = list(dictt.values());
            CustomerArray.append(Customer(dicty[0], dicty[1], dicty[2], dicty[3]));
    for i in range(len(CustomerArray)):
        print(CustomerArray[i].firstname);

if os.path.exists("preferredcustomerarray.txt"):
    print("WELP");
    arrayy = [];
    with open("preferredcustomerarray.txt") as file:
        for item in file:
            dictt = eval(item[:len(item)-1]);
            dicty = list(dictt.values());
            if dicty[0] == .05 or dicty[0] == .1 or dicty[0] == .15:
                PreferredCustomerArray.append(PreferredCustomerGold(dicty[1], dicty[2], dicty[3], dicty[4], dicty[0]));
            else:
                PreferredCustomerArray.append(PreferredCustomerPlanum(dicty[1], dicty[2], dicty[3], dicty[4], dicty[0]));

print("Still great");
ending = "No";
"""file = open('sampleorders.txt', 'r');
while True:
    line = file.readline().split();
    if not line:
        break
    if len(line) != 6 or line[3] not in ['S','M','L'] or line[4] not in ['Tea','Punch','Soda'] or line[5].isdecimal() == False:
        continue
    print(line);
    print(line[0]);
    print(type(line[0]));
    custID = line[0];
    firstname = line[1];
    lastname = line[2];
    size = line[3];
    drink = line[4];
    quantity = int(line[5]);"""
while ending == "No":
    custID = input("Customer ID:");
    firstname = input("First name:");
    lastname = input("Last name:");
    while True:
        size = input("size (S, M, L):");
        if size not in ['S','M','L']:
            print("Try again. Type S, M, or L");
            continue
        else:
            break
    while True:
        drink = input("drink (Tea, Soda, Punch):");
        if drink not in ['Tea','Punch','Soda']:
            print("Try again. Type Tea, Punch, or Soda");
            continue
        else:
            break
    while True:
        quantity = input("quantity (type a whole number):");
        if quantity.isdecimal() == False:
            print("Try again. Please type a whole number");
            continue
        else:
            quantity = int(quantity);
            break
    x = mycol2.insert_one({"CustomerID": custID, "FirstName": firstname, "LastName": lastname, "Size": size, "Drink": drink, "Quantity": quantity});
    oz = 0;
    match size:
        case "S":
            oz = 12;
        case "M":
            oz = 20;
        case "L":
            oz = 32;
        
    price = 0;
    match drink:
        case "Soda":
            price = .2;
        case "Tea":
            price = .12;
        case "Punch":
            price = .15;
            
    saprice = 0;
    match saprice:
        case "S":
            saprice = 4*math.pi*4.5;
        case "M":
            saprice = 4.5*math.pi*5.75;
        case "L":
            saprice = 5.5*math.pi*7;

    totalCost = oz*price*quantity + saprice;
    print(totalCost);
    
    changeIndex = None;
    changeeIndex = None;
    
    for i in range(len(CustomerArray)):
        if CustomerArray[i].guestID == custID:
            changeIndex = i;
            
    for i in range(len(PreferredCustomerArray)):
        if PreferredCustomerArray[i].guestID == custID:
            changeeIndex = i;
    
    if changeIndex == None and changeeIndex == None:
        CustomerArray.append(Customer(firstname, lastname, custID, totalCost));
    elif changeIndex != None:
        CustomerArray[changeIndex].amountSpent = CustomerArray[changeIndex].amountSpent + totalCost;
    else:
        print(type(PreferredCustomerArray[changeeIndex]));
        if type(PreferredCustomerArray[changeeIndex] == "__main__.PreferredCustomerGold"):
            print("it's gold!");
            PreferredCustomerArray[changeeIndex].amountSpent = PreferredCustomerArray[changeeIndex].amountSpent + totalCost*(1-PreferredCustomerArray[changeeIndex].discountPercentage);
        elif type(PreferredCustomerArray[changeeIndex] == "__main__.PreferredCustomerPlanum"):
            print("It's planum!");
            PreferredCustomerArray[changeeIndex].amountSpent = PreferredCustomerArray[changeeIndex].amountSpent + totalCost;
            PreferredCustomerArray[changeeIndex].bonusBucks = math.ceil((CustomerArray[changeeIndex].amountSpent - 200)/5);
        if PreferredCustomerArray[changeeIndex].amountSpent >= 50 and PreferredCustomerArray[changeeIndex].amountSpent < 100:
            print("50 to 100");
            PreferredCustomerArray[changeeIndex].amountSpent = PreferredCustomerArray[changeeIndex].amountSpent + totalCost*PreferredCustomerArray[changeeIndex].discountPercentage;
            PreferredCustomerArray[changeeIndex].discountPercentage = .05;
            PreferredCustomerArray[changeeIndex].amountSpent = PreferredCustomerArray[changeeIndex].amountSpent - totalCost*(PreferredCustomerArray[changeeIndex].discountPercentage);
            print(PreferredCustomerArray[changeeIndex].amountSpent);
        elif PreferredCustomerArray[changeeIndex].amountSpent >= 100 and PreferredCustomerArray[changeeIndex].amountSpent < 150:
            print("100 to 150");
            PreferredCustomerArray[changeeIndex].amountSpent = PreferredCustomerArray[changeeIndex].amountSpent + totalCost*PreferredCustomerArray[changeeIndex].discountPercentage;
            PreferredCustomerArray[changeeIndex].discountPercentage = .1;
            PreferredCustomerArray[changeeIndex].amountSpent = PreferredCustomerArray[changeeIndex].amountSpent - totalCost*(PreferredCustomerArray[changeeIndex].discountPercentage);
            print(PreferredCustomerArray[changeeIndex].amountSpent);
        elif PreferredCustomerArray[changeeIndex].amountSpent >= 150 and PreferredCustomerArray[changeeIndex].amountSpent < 200:
            print("150 to 200");
            PreferredCustomerArray[changeeIndex].amountSpent = PreferredCustomerArray[changeeIndex].amountSpent + totalCost*PreferredCustomerArray[changeeIndex].discountPercentage;
            PreferredCustomerArray[changeeIndex].discountPercentage = .15;
            PreferredCustomerArray[changeeIndex].amountSpent = PreferredCustomerArray[changeeIndex].amountSpent - totalCost*(PreferredCustomerArray[changeeIndex].discountPercentage);
            print(PreferredCustomerArray[changeeIndex].amountSpent);
        elif PreferredCustomerArray[changeeIndex].amountSpent >= 200:
            if type(PreferredCustomerArray[changeeIndex] == "__main__.PreferredCustomerGold"):
                PreferredCustomerArray[changeeIndex].amountSpent = PreferredCustomerArray[changeeIndex].amountSpent + totalCost*PreferredCustomerArray[changeeIndex].discountPercentage;
                print("Gold?");
            PreferredCustomerArray[changeeIndex] = PreferredCustomerPlanum(PreferredCustomerArray[changeeIndex].firstname, PreferredCustomerArray[changeeIndex].lastname, PreferredCustomerArray[changeeIndex].guestID, PreferredCustomerArray[changeeIndex].amountSpent, math.ceil((PreferredCustomerArray[changeeIndex].amountSpent - 200)/5)); 
            print("Planum");
    
    i = 0;
    while i < len(CustomerArray): 
        print(i);
        if CustomerArray[i].amountSpent >= 200:
            pc = PreferredCustomerPlanum(CustomerArray[i].firstname, CustomerArray[i].lastname, CustomerArray[i].guestID, CustomerArray[i].amountSpent, math.ceil((CustomerArray[i].amountSpent - 200)/5));
            PreferredCustomerArray.append(pc);
            del(CustomerArray[i]);
            i = i-1;
        if CustomerArray[i].amountSpent >= 150:
            pc = PreferredCustomerGold(CustomerArray[i].firstname, CustomerArray[i].lastname, CustomerArray[i].guestID, CustomerArray[i].amountSpent - totalCost*.15, .15);
            PreferredCustomerArray.append(pc);
            del(CustomerArray[i]);
            i = i-1;
        elif CustomerArray[i].amountSpent >= 100:
            pc = PreferredCustomerGold(CustomerArray[i].firstname, CustomerArray[i].lastname, CustomerArray[i].guestID, CustomerArray[i].amountSpent - totalCost*.1, .1);
            PreferredCustomerArray.append(pc);
            del(CustomerArray[i]);
            i = i-1;
        elif CustomerArray[i].amountSpent >= 50:
            pc = PreferredCustomerGold(CustomerArray[i].firstname, CustomerArray[i].lastname, CustomerArray[i].guestID, CustomerArray[i].amountSpent - totalCost*.05, .05);
            PreferredCustomerArray.append(pc);
            del(CustomerArray[i]);
            i = i-1;
        i = i + 1;    
    
        
    ending = input("Do you want to end the loop? Answer yes or no");

myclient = pymongo.MongoClient("mongodb://localhost:27017/");
mydb = myclient["mydatabase"];
mycol = mydb["customers"];
file = open('customerarray.txt','w');
#connection = pyodbc.connect(driver='{SQL Server}', server='DESKTOP-48GBL2R\SQLEXPRESS', database='drinks',               
#               trusted_connection='yes');
for i in range(len(CustomerArray)):
    x = mycol.insert_one({"Type": "Regular customer", "FirstName": CustomerArray[i].firstname, "LastName": CustomerArray[i].lastname, "GuestID": CustomerArray[i].guestID, "AmountSpent": CustomerArray[i].amountSpent});
    file.write(str(vars(CustomerArray[i])) + '\n');
    params = (CustomerArray[i].firstname, CustomerArray[i].lastname, CustomerArray[i].guestID, CustomerArray[i].amountSpent, None, None);
    cursor.execute(
       "INSERT INTO CustomerTable (FirstName, LastName, GuestID, AmountSpent, DiscountPercentage, BonusBucks) VALUES (?,?,?,?,?,?)", params);
connection.commit();
file.close();

file = open('preferredcustomerarray.txt','w');
for i in range(len(PreferredCustomerArray)):
    file.write(str(vars(PreferredCustomerArray[i])) + '\n');
    print(i);
    print(type(PreferredCustomerArray[i]));
    if hasattr(PreferredCustomerArray[i], "discountPercentage"):
        x = mycol.insert_one({"Type": "Gold customer", "FirstName": PreferredCustomerArray[i].firstname, "LastName": PreferredCustomerArray[i].lastname, "GuestID": PreferredCustomerArray[i].guestID, "AmountSpent": PreferredCustomerArray[i].amountSpent, "DiscountPercentage": PreferredCustomerArray[i].discountPercentage});
        print("Goldd");
        params = (PreferredCustomerArray[i].firstname, PreferredCustomerArray[i].lastname, PreferredCustomerArray[i].guestID, PreferredCustomerArray[i].amountSpent, PreferredCustomerArray[i].discountPercentage, None);
        cursor.execute(
            "INSERT INTO CustomerTable (FirstName, LastName, GuestID, AmountSpent, DiscountPercentage, BonusBucks) VALUES (?,?,?,?,?,?)", params);
    elif hasattr(PreferredCustomerArray[i], "bonusBucks"):
        x = mycol.insert_one({"Type": "Planum customer", "FirstName": PreferredCustomerArray[i].firstname, "LastName": PreferredCustomerArray[i].lastname, "GuestID": PreferredCustomerArray[i].guestID, "AmountSpent": PreferredCustomerArray[i].bonusBucks, "BonusBucks": PreferredCustomerArray[i].bonusBucks});
        print("Planumm");
        params = (PreferredCustomerArray[i].firstname, PreferredCustomerArray[i].lastname, PreferredCustomerArray[i].guestID, PreferredCustomerArray[i].amountSpent, None, PreferredCustomerArray[i].bonusBucks);
        cursor.execute(
            "INSERT INTO CustomerTable (FirstName, LastName, GuestID, AmountSpent, DiscountPercentage, BonusBucks) VALUES (?,?,?,?,?,?)", params);
connection.commit();
connection.close();
file.close();







