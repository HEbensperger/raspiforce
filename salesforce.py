from simple_salesforce import Salesforce
import ConfigParser

#
# Read configuration from file
#
config = ConfigParser.RawConfigParser()
config.read('salesforce_login.cfg')

#
# Lookup Salesforce demo org credentials and configuration
#
sf_lookup = Salesforce(username=config.get('Salesforce', 'username'), password=config.get('Salesforce', 'password'), security_token=config.get('Salesforce', 'security_token'))
result = sf_lookup.query("SELECT tegeling_dev__Username__c, tegeling_dev__Password__c, tegeling_dev__Security_Token__c, tegeling_dev__Case_Account_Id__c, tegeling_dev__Case_Contact_Id__c, tegeling_dev__Case_Status__c, tegeling_dev__Case_Subject__c FROM tegeling_dev__Raspberry_Pi_Demo__c WHERE tegeling_dev__Active__c = true")

myUsername = result.get('records')[0].get('tegeling_dev__Username__c')
myPassword =  result.get('records')[0].get('tegeling_dev__Password__c')
myToken = result.get('records')[0].get('tegeling_dev__Security_Token__c')

accountid = result.get('records')[0].get('tegeling_dev__Case_Account_Id__c')
contactid = result.get('records')[0].get('tegeling_dev__Case_Contact_Id__c')
status = result.get('records')[0].get('tegeling_dev__Case_Status__c')
subject = result.get('records')[0].get('tegeling_dev__Case_Subject__c')

#
# Check the AccountId and ContactId if they are empty and set to None
#
if accountid is None:
   print "AccountId is empty"
   accountid = ""

if contactid is None:
   print "ContactId is empty"
   contactid = ""

#
# Create new connection to demo org and create a case
#

sf = Salesforce(username=myUsername, password=myPassword, security_token=myToken)
sf.Case.create({'Subject':subject,'Status':status,'AccountId':accountid,'ContactId':contactid})
