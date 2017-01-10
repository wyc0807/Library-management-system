CREATE TABLE bookinfo(
	ISBN CHAR(20) PRIMARY KEY,
	title CHAR(50),
	title_id CHAR(30),
	author CHAR(30),
	publisher CHAR(50),
	location CHAR(30),
	available INT,
	lent INT);
CREATE TABLE buys(
	ISBN CHAR(50),
	title CHAR(50),
	num INT,
	time CHAR(50)
	);
CREATE TABLE dies(
	ISBN CHAR(50),
	title CHAR(50),
	num INT,
	time CHAR(50)
	);
CREATE TABLE borrows(
	ISBN CHAR(50),
	title CHAR(50),
	reader_ID CHAR(20),
	reader_name CHAR(50),
	time CHAR(50)
	);
CREATE TABLE readers(
	ID CHAR(20),
	name CHAR(30),
	password CHAR(20)
	);
CREATE TABLE admin(
	ID CHAR(20),
	password CHAR(20)
	);
CREATE TABLE reader_borrows(
	reader_ID CHAR(20),
	ISBN CHAR(50),
	title CHAR(50),
	title_id CHAR(30),
	author CHAR(30),
	publisher CHAR(50),
	location CHAR(30),
	borrow_time CHAR(50),
	return_time CHAR(50)
	);