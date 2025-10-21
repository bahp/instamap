""""""
# Library
import re
import json


def response_extract_json(content):
    """"""
    # Libraries
    import re
    # Get response
    # Use regular expression to find the JSON string
    json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)

    if json_match:
        json_string = json_match.group(1)
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No JSON found in the response.")
        return None

def response_extract_code(code):
    """"""
    return json.loads(code)



# Important notes
#
# We are using bard to query information. Note that there might be many
# reasons why the response cannot be parse properly. Some of these reasons
# are:
#
# 1. The cookies expired and a weird result is obtained.
# 2. The json provided in the result is not complete (missing closing quotes)
# 3. The json is directly an array with dictionaries
# 4. The json might also have a key locations with an array of dictinaries.

# Load file
with open('bard.json', 'r') as f:
    response = json.load(f)

# Show

print(response)
print(response['status_code'])
print(response['content'])
#print(json.dumps(response, indent=4))

# Extract
extracted_json = response_extract_json(response['content'])
extracted_code = response_extract_code(response['code'])

# Show
print("\n\n\n Showing response from <content>")
print(json.dumps(extracted_json, indent=4))

print("\n\n\n Showing response from <code>")
print(json.dumps(extracted_code, indent=4))