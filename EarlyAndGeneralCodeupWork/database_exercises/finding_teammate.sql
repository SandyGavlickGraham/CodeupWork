USE ada_students;

SELECT group_id, first_name, last_name, modules.module_id
FROM student_groups
JOIN students
ON student_groups.student_id = students.student_id
JOIN modules
ON  student_groups.module_id = modules.module_id
WHERE modules.module_id = 6 and group_id = 2
ORDER BY group_id;


-- USE employees;
-- SELECT title, COUNT(emp_no) AS num_emp
--     FROM titles
--     GROUP BY title;

USE zillow;

SELECT prop16.id, parcelid, actype.airconditioningdesc, archtype.architecturalstyledesc, 
       basementsqft, bathroomcnt, bedroomcnt, bldgclass.buildingclassdesc,
       buildingqualitytypeid, calculatedbathnbr, decktypeid, finishedfloor1squarefeet,
       calculatedfinishedsquarefeet, finishedsquarefeet12, finishedsquarefeet13, 
       finishedsquarefeet15, finishedsquarefeet50, finishedsquarefeet6, fips,
       fireplacecnt, fullbathcnt, garagecarcnt, garagetotalsqft, hashottuborspa,
       heattype.heatingorsystemdesc, latitude, longitude, lotsizesquarefeet, poolcnt,
       poolsizesum, pooltypeid10, pooltypeid2, pooltypeid7, propertycountylandusecode,
       proplandusetype.propertylandusedesc, propertyzoningdesc, rawcensustractandblock, regionidcity,
       regionidcounty, regionidneighborhood, regionidzip, roomcnt, storytype.storydesc,
       threequarterbathnbr, typeconstr.typeconstructiondesc, unitcnt, yardbuildingsqft17, 
       yardbuildingsqft26, yearbuilt, numberofstories, fireplaceflag, structuretaxvaluedollarcnt,
       taxvaluedollarcnt, assessmentyear, landtaxvaluedollarcnt, taxamount, taxdelinquencyflag,
       taxdelinquencyyear, censustractandblock, logerror, transactiondate
FROM properties_2016 AS prop16
LEFT JOIN airconditioningtype AS actype 
USING (airconditioningtypeid)
LEFT JOIN architecturalstyletype AS archtype
USING (architecturalstyletypeid)
LEFT JOIN buildingclasstype AS bldgclass
USING (buildingclasstypeid)
LEFT JOIN heatingorsystemtype AS heattype
USING (heatingorsystemtypeid)
LEFT JOIN propertylandusetype AS proplandusetype
USING (propertylandusetypeid)
LEFT JOIN storytype
USING (storytypeid)
LEFT JOIN typeconstructiontype AS typeconstr
USING (typeconstructiontypeid)
INNER JOIN predictions_2016 AS pred16
USING (parcelid)
WHERE transactiondate IS NOT NULL
AND latitude IS NOT NULL
AND longitude IS NOT NULL;


SELECT * 
FROM properties_2016 as prop16
JOIN properties_2017 as prop17
USING (parcelid)
LIMIT 10;

parcelid -- unique_properties -- parcelid already in properties dbs
airconditioningtypeid -- airconditioningtype -- airconditioningdesc
architecturalstyletypeid -- architecturalstyletype -- architecturalstyledesc
buildingclasstypeid -- buildingclasstype -- buildingclassdesc
heatingorsystemtypeid -- heatingorsystemtype -- heatingorsytemdesc
propertylandusetypeid -- propertylandusetype -- propertylandusedesc
storytypeid -- storytype -- storydesc
typeconstructiontypeid -- typeconstructiontype -- typeconstructiondesc



ALL except excluded typeid columns:
id, parcelid, airconditioningtype.airconditioningdesc
architecturalstyletype.architecturalstyledesc
basementsqft
bathroomcnt
bedroomcnt
buildingclasstype.buildingclassdesc
buildingqualitytypeid
calculatedbathnbr
decktypeid
finishedfloor1squarefeet
calculatedfinishedsquarefeet
finishedsquarefeet12
finishedsquarefeet13
finishedsquarefeet15
finishedsquarefeet50
finishedsquarefeet6
fips
fireplacecnt
fullbathcnt
garagecarcnt
garagetotalsqft
hashottuborspa
heatingorsystemtype.heatingorsytemdesc
latitude
longitude
lotsizesquarefeet
poolcnt
poolsizesum
pooltypeid10
pooltypeid2
pooltypeid7
propertycountylandusecode
propertylandusetype.propertylandusedesc
propertyzoningdesc
rawcensustractandblock
regionidcity
regionidcounty
regionidneighborhood
regionidzip
roomcnt
storytype.storydesc
threequarterbathnbr
typeconstructiontype.typeconstructiondesc
unitcnt
yardbuildingsqft17
yardbuildingsqft26
yearbuilt
numberofstories
fireplaceflag
structuretaxvaluedollarcnt
taxvaluedollarcnt
assessmentyear
landtaxvaluedollarcnt
taxamount
taxdelinquencyflag
taxdelinquencyyear
censustractandblock



IDs without matching tables:
buildingqualitytypeid 
decktypeid 
pooltypeid10 
pooltypeid2 
pooltypeid7 
propertycountylandusecode 
propertyzoningdesc 
rawcensustractandblock 
regionidcity 
regionidcounty 
regionidneighborhood 
regionidzip 