# CH-perspective-generation
Perspective generation from a CSV referential

I’ve written a python script to create perspectives based on data from a referential in a CSV file. I needed to create it for a customer who was using a tag to link assets with application. This customer is using AWS and Azure. This tag that I will use in the example was named ATEMI. The point was that the value of the tag are codes to identify the application. However the customer wanted to have in the reports the application name (label) and not the code. They have an external referential that they were able to share on CSV format to link the application code to the label but also to the internal customer using it and to the billed customer who can be different. And as usual the ATEMI tag can be found with different spelling.

So I wrote this script to read a CSV file containing the different tag key I can expect for AWS and for Azure, the value that is in fact the key to associate the assets with each group of each perspective (in my exemple: Application, Operational Customer, Billed Customer ). 

Then expected format of the CSV file is the following:

separator has to be ';'

First column header has to be aws tags, second column has to be azure tags and each row just contains the different tag key that we’ll use to filter the assets

Third column header has to be key and each row contains the key value that the tag has to be equal to for the assets to be part of the group. 

From the forth column the header is the name of the perspective to be created and each row contains the name of the group who has to receive the assets who are tagged with one of the tag referenced in column 1 for AWS assets, column 2 for azure assets with value coming from key column

Here is an exemple of a CSV file that the script can parse:


aws tags;azure tags;key;Application;Operational Customer;Billed Customer
atemi-id,ATEMI;atemi,ATEMI;5062;PDT MOTRICE;VOYAGES;DSI VOYAGES
atemi-id,ATEMI;atemi,ATEMI;4939;ORME;GARES ET CONNEXIONS;DSI G&C
atemi-id,ATEMI;atemi,ATEMI;4960;RESERVATION;GARES ET CONNEXIONS;DSI VOYAGES
Running the script on this sample will create 3 perspectives:

Application

PDT MOTRICE
AwsAsset - Amazon Asset (EC2 & RDS Instances, …) where tag_atmi-id Equals 5062
Amazon Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 5062
Azure Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 5062

ORME
AwsAsset - Amazon Asset (EC2 & RDS Instances, …) where tag_atmi-id Equals 4939
Amazon Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 4939
Azure Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 4939

RESERVATION
AwsAsset - Amazon Asset (EC2 & RDS Instances, …) where tag_atmi-id Equals 4960
Amazon Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 4960
Azure Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 4960

Operational Customer

VOYAGES
AwsAsset - Amazon Asset (EC2 & RDS Instances, …) where tag_atmi-id Equals 5062
Amazon Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 5062
Azure Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 5062

GARES ET CONNEXIONS
AwsAsset - Amazon Asset (EC2 & RDS Instances, …) where tag_atmi-id Equals 4939
Amazon Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 4939
Azure Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 4939
AwsAsset - Amazon Asset (EC2 & RDS Instances, …) where tag_atmi-id Equals 4960
Amazon Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 4960
Azure Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 4960

Billed Customer

DSI VOYAGE
AwsAsset - Amazon Asset (EC2 & RDS Instances, …) where tag_atmi-id Equals 5062
Amazon Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 5062
Azure Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 5062
AwsAsset - Amazon Asset (EC2 & RDS Instances, …) where tag_atmi-id Equals 4960
Amazon Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 4960
Azure Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 4960

DSI G&C
AwsAsset - Amazon Asset (EC2 & RDS Instances, …) where tag_atmi-id Equals 4939
Amazon Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 4939
Azure Taggable Asset (Does not gather associated assets) where tag_atmi-id Equals 4939

The following script has been used and tested with python 3.8.5.
