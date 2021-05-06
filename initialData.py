import sqlite3

class initialData:
    DATABASE = 'sjps5.db'
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    print('----------------------------Configuring Database-------------------------------------')
    # Create tables
    print("\n\nCreating Database tables ....")
    cur.execute('''DROP TABLE IF EXISTS Products''')
    cur.execute('''create table Products(
        maker varchar(35) not null,
        model integer,
        type varchar(35) not null,
        primary key(model)
    )''')

    cur.execute('''DROP TABLE IF EXISTS PCs''')
    cur.execute('''
    create table PCs(
        model integer,
        speed integer not null,
        ram integer not null,
        hd integer not null,
        price integer not null,
        foreign key(model) references Products(model)
    )''')
    cur.execute('''DROP TABLE IF EXISTS Laptops''')
    cur.execute('''
    create table Laptops(
        model integer,
        speed integer not null,
        ram integer not null,
        hd integer not null,
        screen integer not null,
        price integer not null,
        foreign key(model) references Products(model)
    )''')
    cur.execute('''DROP TABLE IF EXISTS Printers''')
    cur.execute('''
    create table Printers(
        model integer,
        color boolean not null,
        type varchar(35) not null,
        price integer not null,
        foreign key(model) references Products(model)
    )''')
    print('\nCreating initial data ....')
    cur.execute("INSERT INTO Products values('apple',11111,'PC')")
    cur.execute("INSERT INTO Products values('apple',11112,'Laptop')");
    cur.execute("INSERT INTO Products values('apple',11113,'Printer')");
    cur.execute("INSERT INTO Products values('apple',11114,'Laptop')");
    cur.execute("INSERT INTO Products values('microsoft',11115,'Laptop')");
    cur.execute("INSERT INTO Products values('microsoft',11116,'PC')");
    cur.execute("INSERT INTO Products values('microsoft',11117,'Printer')");
    cur.execute("INSERT INTO Products values('microsoft',11118,'PC')");
    cur.execute("INSERT INTO Products values('microsoft',11119,'PC')");
    cur.execute("INSERT INTO Products values('microsoft',11120,'PC')");
    cur.execute("INSERT INTO Products values('microsoft',11121,'PC')");
    cur.execute("INSERT INTO Products values('microsoft',11122,'Laptop')");
    cur.execute("INSERT INTO Products values('microsoft',11123,'Laptop')");
    cur.execute("INSERT INTO Products values('microsoft',11124,'Laptop')");
    cur.execute("INSERT INTO Products values('apple',11125,'Printer')");
    cur.execute("INSERT INTO Products values('apple',11126,'Printer')");
    cur.execute("INSERT INTO Products values('apple',11127,'Printer')");
    cur.execute("INSERT INTO PCs values(11111,100,100,100,300)");
    cur.execute("INSERT INTO Laptops values(11112,150,150,150,20,500)");
    cur.execute("INSERT INTO Printers values(11113,false,'laser',500)");
    cur.execute("INSERT INTO Laptops values(11114,250,120,250,20,600)");
    cur.execute("INSERT INTO Laptops values(11115,250,250,250,22,800)");
    cur.execute("INSERT INTO PCs values(11116,200,200,200,600)");
    cur.execute("INSERT INTO Printers values(11117,true,'ink-jet',300)");
    cur.execute("INSERT INTO PCs values(11118,300,200,300,700)");
    cur.execute("INSERT INTO PCs values(11119,300,300,300,800)");
    cur.execute("INSERT INTO PCs values(11120,400,400,400,900)");
    cur.execute("INSERT INTO PCs values(11121,500,500,500,1000)");
    cur.execute("INSERT INTO Laptops values(11122,350,350,350,23,800)");
    cur.execute("INSERT INTO Laptops values(11123,350,350,450,24,800)");
    cur.execute("INSERT INTO Laptops values(11124,450,350,550,24,800)");
    cur.execute("INSERT INTO Printers values(11125,true,'laser',600)");
    cur.execute("INSERT INTO Printers values(11126,true,'ink-jet',500)");
    cur.execute("INSERT INTO Printers values(11127,false,'ink-jet',500)");
    print("\nSetting Database Successfully!!\n\n")
    print('-------------------------------------------------------------------------------------')
    # Save (commit) the changes
    conn.commit()

    cur = conn.cursor()
    cur.close()
    conn.close()
