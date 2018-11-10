# installation instructions
clone the repo
make a virtualenv
install python requirements
```
pip install -r requirements.txt
```
create database:
install postgresql
create database and grant permissions
```
psql -h localhost -U postgres postgres
```
in the psql shell:
```
create database abbeyroadhack;
create user abbeyroadhack with password 'abbeyroadhack';
alter role abbeyroadhack set client_encoding to 'utf8';
alter role abbeyroadhack SET default_transaction_isolation TO 'read committed';
alter role abbeyroadhack SET timezone TO 'UTC';
grant all privileges on database abbeyroadhack to abbeyroadhack;
```
