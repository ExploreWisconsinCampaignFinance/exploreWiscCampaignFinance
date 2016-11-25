import os
import sqlite3
#os.chdir(os.path.expanduser("~") + \
#	"/Documents/exploreWiscCampaignFinance")

db_name = "db.sqlite3"
conn = sqlite3.connect(db_name)
c = conn.cursor()



#### Populating ContributorData table
### field names
dte = "date"
cand = "candidate"
cont = "contributor"
c_s_z = "city_state_zip"
emp = "employer"
int_cat = "interest_category"
amt = "amount"
id_fld = "id"
cum = "cumulative"

cont_name = "blog_contributordata"
cont_data = "contribution_data.tsv"

#returns tuple with
###(id, name, type, notnull, default_value, primary_key)
c.execute('PRAGMA TABLE_INFO({})'.format(cont_name))

for tup in c.fetchall(): print tup[1] + ": " + tup[2] 
names = [tup[1] for tup in c.fetchall()]
print names



c.execute("DELETE FROM " + cont_name)
conn.commit()


f = open(cont_data, "rt")
field_string = "INSERT INTO {tn} ({dte}, {cand}, {cont}, {c_s_z}, {emp}, {int_cat}, {amt}, {cum}) VALUES "
val_string = "(DATE('{dte_val}'), '{cand_val}', '{cont_val}', '{c_s_z_val}', '{emp_val}', '{int_cat_val}', {amt_val}, {cum_val})"
exec_string = field_string + val_string

for i, line in enumerate(f):
	if i == 0: continue
	if i % 1000 == 0: print "Record:", i
	line = line.replace("\n", "")
	
	line = line.replace("'", "").replace('"', "")
	flds = line.split("\t")
	if (flds[6] == ''):
		continue
	ready = exec_string.format(tn=cont_name, \
		dte=dte, cand=cand, cont=cont, c_s_z=c_s_z, emp=emp, int_cat=int_cat, amt=amt, cum=cum, \
		dte_val=flds[0], \
		cand_val=flds[1], \
		cont_val=flds[2], \
		c_s_z_val=flds[3], \
		emp_val=flds[4], \
		int_cat_val=flds[5], \
		amt_val=flds[6], \
		cum_val=0)
	
	c.execute(ready)

f.close()
conn.commit()

#### Populating Candidate Table
cand_name = "blog_candidatedata"
c.execute("DELETE FROM " + cand_name)
conn.commit()
dist = "district" # models.IntegerField()
cand = "candidate" # models.CharField(max_length=200)
hous = "house" # models.CharField(max_length=200)
party = "party" # models.CharField(max_length=200)
year = "year_ran" # models.DateField(null=True)
won = "won" # models.IntegerField()

cand_data = "candidate_data.tsv"

f = open(cand_data, "rb")
field_string = "INSERT INTO {tn} ('{hous}', '{dist}', '{party}', '{won}', '{year}', '{cand}') VALUES "
val_string = "('{hous_val}', {dist_val}, '{party_val}', {won_val}, DATE('{year_val}'), '{cand_val}')"
exec_string = field_string + val_string

for i, line in enumerate(f):
	if i == 0: continue
	if i % 20 == 0: print "Record:", i
	line = line.replace("\n", "")
	line = line.replace("'", "").replace('"', "")
	flds = line.split("\t")
	ready = exec_string.format(tn=cand_name, \
		hous=hous, dist=dist, party=party, year=year, won=won, cand=cand,\
		hous_val=flds[0], \
		dist_val=flds[1], \
		party_val=flds[2], \
		won_val=flds[3], \
		year_val=flds[4] + "-01-01", \
		cand_val=flds[5])
	
	c.execute(ready)

f.close()
conn.commit()

conn.close()



### Testing...
#val_string = "("
#	for j, fld in enumerate(flds):
#		if j == 0:
#			val_string += "DATE('" + fld + "'),"
#		elif j < 6:
#			val_string += "'" + fld + "',"
#		else:
#			val_string += str(fld) + ")"
	#print exec_string + val_string



#conn = sqlite3.connect(db_name)
#c = conn.cursor()
#c.execute("INSERT INTO {tn} \
#	({cand}, {cont}, {int_cat}, {emp}, {amt}, {c_s_z}, {dte}) \
#	VALUES \
#	('Bush', 'George Bush', 'Politics', 'None', 100000, 'Texax', DATE('2014-01-01'))".\
#	format(tn=cont_name, \
#		cand=cand, cont=cont, int_cat=int_cat, emp=emp, amt=amt, c_s_z=c_s_z, dte=dte))
#conn.commit()
#conn.close()




## return db info
#%run db_info.py db.sqlite3 blog_contributordata
#%run db_info.py db.sqlite3 blog_candidatedata

### select querys
#conn = sqlite3.connect(db_name)
#c = conn.cursor()
#c.execute('SELECT * FROM {tn}'.format(tn=cand_name))
#all_rows = c.fetchall()
#for i, rw in enumerate(all_rows):
#	print rw
#	if i % 50 == 0:
#		raw_input("Push enter to proceed")
	
#conn.close()

#returns tuple with
###(id, name, type, notnull, default_value, primary_key)
#c.execute('PRAGMA TABLE_INFO({})'.format(cont_name))

#for tup in c.fetchall():
#	print tup[1] + ": " + tup[2] 
#names = [tup[1] for tup in c.fetchall()]
#print names
#conn.close()

##
#conn = sqlite3.connect(db_name)
#c = conn.cursor()
#c.execute("DELETE FROM " + cand_name)
#conn.commit()
###conn.close()
