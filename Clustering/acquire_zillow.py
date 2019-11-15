import pandas as pd
import env

def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

# - only include properties with a transaction in 2016 &/or 2017 (along with zestimate error and date of transaction).
# - only include properties that include a latitude and longitude value

def get_zillow_2016_data():
    return pd.read_sql(
    'SELECT prop16.id, parcelid,actype.airconditioningdesc, \
            archtype.architecturalstyledesc, basementsqft, bathroomcnt, \
            bedroomcnt, bldgclass.buildingclassdesc, \
            buildingqualitytypeid, calculatedbathnbr, decktypeid, \
            finishedfloor1squarefeet,calculatedfinishedsquarefeet, \
            finishedsquarefeet12, finishedsquarefeet13, \
            finishedsquarefeet15, finishedsquarefeet50, \
            finishedsquarefeet6, fips, fireplacecnt, fullbathcnt, \
            garagecarcnt, garagetotalsqft, hashottuborspa,\
            heattype.heatingorsystemdesc, latitude, longitude, \
            lotsizesquarefeet, poolcnt, poolsizesum, pooltypeid10, \
            pooltypeid2, pooltypeid7, propertycountylandusecode,\
            proplandusetype.propertylandusedesc, propertyzoningdesc, \
            rawcensustractandblock, regionidcity, regionidcounty, \
            regionidneighborhood, regionidzip, roomcnt, \
            storytype.storydesc, threequarterbathnbr, \
            typeconstr.typeconstructiondesc, unitcnt, yardbuildingsqft17,\
            yardbuildingsqft26, yearbuilt, numberofstories, fireplaceflag,\
            structuretaxvaluedollarcnt,taxvaluedollarcnt, assessmentyear,\
            landtaxvaluedollarcnt, taxamount, taxdelinquencyflag,\
            taxdelinquencyyear, censustractandblock, logerror, transactiondate\
     FROM properties_2016 AS prop16 \
     LEFT JOIN airconditioningtype AS actype \
     USING (airconditioningtypeid) \
     LEFT JOIN architecturalstyletype AS archtype \
     USING (architecturalstyletypeid) \
     LEFT JOIN buildingclasstype AS bldgclass \
     USING (buildingclasstypeid) \
     LEFT JOIN heatingorsystemtype AS heattype \
     USING (heatingorsystemtypeid) \
     LEFT JOIN propertylandusetype AS proplandusetype \
     USING (propertylandusetypeid) \
     LEFT JOIN storytype \
     USING (storytypeid) \
     LEFT JOIN typeconstructiontype AS typeconstr \
     USING (typeconstructiontypeid) \
     INNER JOIN predictions_2016 AS pred16 \
     USING (parcelid) \
     WHERE transactiondate IS NOT NULL \
     AND latitude IS NOT NULL \
     AND longitude IS NOT NULL;', 
     get_connection('zillow'))

def get_zillow_2017_data():
    return pd.read_sql(
    'SELECT prop17.id, parcelid,actype.airconditioningdesc, \
            archtype.architecturalstyledesc, basementsqft, bathroomcnt, \
            bedroomcnt, bldgclass.buildingclassdesc, \
            buildingqualitytypeid, calculatedbathnbr, decktypeid, \
            finishedfloor1squarefeet,calculatedfinishedsquarefeet, \
            finishedsquarefeet12, finishedsquarefeet13, \
            finishedsquarefeet15, finishedsquarefeet50, \
            finishedsquarefeet6, fips, fireplacecnt, fullbathcnt, \
            garagecarcnt, garagetotalsqft, hashottuborspa,\
            heattype.heatingorsystemdesc, latitude, longitude, \
            lotsizesquarefeet, poolcnt, poolsizesum, pooltypeid10, \
            pooltypeid2, pooltypeid7, propertycountylandusecode,\
            proplandusetype.propertylandusedesc, propertyzoningdesc, \
            rawcensustractandblock, regionidcity, regionidcounty, \
            regionidneighborhood, regionidzip, roomcnt, \
            storytype.storydesc, threequarterbathnbr, \
            typeconstr.typeconstructiondesc, unitcnt, yardbuildingsqft17,\
            yardbuildingsqft26, yearbuilt, numberofstories, fireplaceflag,\
            structuretaxvaluedollarcnt,taxvaluedollarcnt, assessmentyear,\
            landtaxvaluedollarcnt, taxamount, taxdelinquencyflag,\
            taxdelinquencyyear, censustractandblock, logerror, transactiondate\
     FROM properties_2017 AS prop17 \
     LEFT JOIN airconditioningtype AS actype \
     USING (airconditioningtypeid) \
     LEFT JOIN architecturalstyletype AS archtype \
     USING (architecturalstyletypeid) \
     LEFT JOIN buildingclasstype AS bldgclass \
     USING (buildingclasstypeid) \
     LEFT JOIN heatingorsystemtype AS heattype \
     USING (heatingorsystemtypeid) \
     LEFT JOIN propertylandusetype AS proplandusetype \
     USING (propertylandusetypeid) \
     LEFT JOIN storytype \
     USING (storytypeid) \
     LEFT JOIN typeconstructiontype AS typeconstr \
     USING (typeconstructiontypeid) \
     INNER JOIN predictions_2017 AS pred17 \
     USING (parcelid) \
     WHERE transactiondate IS NOT NULL \
     AND latitude IS NOT NULL \
     AND longitude IS NOT NULL;', 
     get_connection('zillow'))


def get_zillow_data():
    zillow_2016_df = get_zillow_2016_data()
    zillow_2017_df = get_zillow_2017_data()
    full_df = zillow_2016_df.append(zillow_2017_df, ignore_index=True)
    full_df.to_csv("zillow_data.csv", index=False)
