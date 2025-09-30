import json
import boto3

#constant for table name
TABLE_NAME = "portfolio-data"
AWS_REGION = "eu-central-1"

#initialize DynamoDB and create table
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)

#update user about opening projects.json…
print("Reading from contents/projects.json…")
with open("contents/projects.json", "r") as f:
    projects = json.load(f)

#…and how many items are in projects
print(f"Found {len(projects)} projects to upload.")

#loop through projects
for project in projects:
    #define project item template
    item = {
        "PK": "USER#dgoossens",
        "SK": f"PROJ#{project["id"]}",
        "type": "ProjectType",
        "projectName": project["projectName"],
        "description": project["description"],
        "technologiesUsed": project["technologiesUsed"],
    }

    #inform user about current addition to table
    print(f"Uploading project: {item["projectName"]}…")

    try:
        #add to DynamoDB table
        response = table.put_item(Item=item)
        #inform about success
        print("…success!")

    #error handling and informing about the cause
    except Exception as e:
        print(f"…FAILED to upload {item["projectName"]}. Error:{e}")

print("Database seeding complete.")
    
    