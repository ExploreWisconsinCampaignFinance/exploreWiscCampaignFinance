options(stringsAsFactors=F)
library(RSQLite)
setwd("~/Documents/exploreWiscCampaignFinance")
con = dbConnect(SQLite(), dbname = "db.sqlite3")
dbListTables(con)
dbListFields(con, "blog_legenddata")
statement = "SELECT * FROM blog_legenddata"
res = dbSendQuery(con, statement)
dbGetInfo(res)
dbFetch(res, 100)
dbGetInfo(res)
dbColumnInfo(res)
# ftched = fetch(res, n = 100)
# 
# df = dbGetQuery(con, "SELECT * FROM  blog_post")

line_id=c(
    "Vos_Robin",
    "Steineke_Jim",
    "Knodl_Dan",
    "August_Tyler",
    "Murtha_John",
    "Nerison_LeeA",
    "Barca_Peter",
    "Shankland_Katrina",
    "Jorgensen_Andy",
    "Zamarripa_JoCasta")
line_name=c(
    "Vos, Speaker of the House",
    "Steineke, Majority Leader",
    "Knodl, Asst. Majority Leader",
    "August, Speaker Pro Tempore",
    "Murtha, Majority Caucus Chair",
    "Nerison, Majority Caucus Vice-Chair",
    "Barca, Minority Leader",
    "Shankland, Asst. Minority Leader",
    "Joregensen, Minority Caucus Chair",
    "Zamarripa, Minorty Caucus Vice-Chair"
)
id = 1:length(line_name)
campaign_legend_data = cbind(id, line_id, line_name)

dbWriteTable(
    con,
    "blog_legenddata",
    data.frame(campaign_legend_data),
    append=FALSE,
    overwrite=TRUE,
    field.types=c("INTEGER", "TEXT", "TEXT")
)

dbDisconnect(con)

### For contribution sources table
library(DBI)
con = dbConnect(RSQLite::SQLite(), dbname = 'db.sqlite3')
dbListTables(con)
statement = "SELECT * FROM blog_contribsourcesbyparty"
res = dbSendQuery(con, statement)
dbGetInfo(res)
dbFetch(res, 100)
dbGetInfo(res)
dbColumnInfo(res)

toImport = read.delim("../../Documents/campaign_finance/raw_data/ASM_ContribSources.tsv", sep="\t")
names(toImport) = c("interest_cateogry", "democrat", "republican")
toImport = cbind(id = 1:nrow(toImport), toImport)

dbWriteTable(
    con,
    'blog_contribsourcesbyparty',
    toImport,
    append=FALSE,
    overwrite=TRUE,
    row.names=FALSE,
    field.types=c("INTEGER", "TEXT", "REAL", "REAL")
)
dbDisconnect(con)

### for all candidate table

con = dbConnect(SQLite(), dbname = "db.sqlite3")
dbListTables(con)
dbListFields(con, "blog_candidatedata")
statement = "SELECT * FROM blog_candidatedata"
res = dbSendQuery(con, statement)
# dbGetInfo(res)
dbFetch(res, 300)
dbGetInfo(res)
dbColumnInfo(res)
legisInfo = read.delim("~/Documents/campaign_finance/raw_data/candidate_data.tsv")
### Get into same order as Db
id = 1:nrow(legisInfo)
dat = data.frame(
    id = id,
    district = legisInfo$District,
    candidate = legisInfo$Candidate,
    house = legisInfo$House,
    party = legisInfo$Party,
    year_ran = as.Date(paste(legisInfo$YearRan, "1", "1", sep="-"), "%Y-%m-%d"),
    won = legisInfo$Won
)

dbWriteTable(
    con,
    "blog_candidatedata",
    dat,
    append=T,
    overwrite=F,
    field.types=c("INTEGER", "INTEGER", "TEXT", "TEXT", "TEXT", "DATE", "INTEGER")
)

dbDisconnect(con)

dbBegin(con)
rs <- dbSendQuery(con, "DELETE FROM blog_candidatedata WHERE 1>-1")
dbClearResult(rs)
dbCommit(con)
### for all contributor table
con = dbConnect(SQLite(), dbname = "db.sqlite3")
dbListTables(con)
dbListFields(con, "blog_contributordata")
statement = "SELECT * FROM blog_contributordata"
res = dbSendQuery(con, statement)
# dbGetInfo(res)
dbFetch(res, 10000)
dbGetInfo(res)
dbColumnInfo(res)
contribution = read.delim("~/Documents/campaign_finance/raw_data/contribution_data.tsv")
contribution = subset(contribution, contribution$Candidate != "Candidate")
contribution = subset(contribution, !is.na(contribution$ContributorName))
contribution$DATE = as.Date(contribution$DATE)
contribution$Amount = as.numeric(contribution$Amount)
contribution$City_State_Zip[is.na(contribution$City_State_Zip)] = "None"
contribution$Employer[is.na(contribution$Employer)] = "None"
write.table(
    contribution,
    "~/Documents/campaign_finance/raw_data/contribution_data.tsv",
    row.names=F,
    sep="\t")
### Get into same order as Db
id = 1:nrow(contribution)
dat = data.frame(
    id = id,
    date = contribution$DATE,
    candidate = contribution$Candidate,
    contributor = contribution$ContributorName,
    city_state_zip = contribution$City_State_Zip,
    employer = contribution$Employer,
    interest_category = contribution$InterestCategory,
    amount = contribution$Amount
)


dbWriteTable(
    con,
    "blog_contributordata",
    dat,
    append=T,
    overwrite=F,
    field.types=c("INTEGER", "DATE", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "INTEGER")
)

dbDisconnect(con)
