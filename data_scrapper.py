import re
result_name = 'result\\accord_ES_SYNC_SEED5.txt'
with open(result_name, 'r') as file:
    data = ''.join(file.readlines())

x = re.findall(r'Count:\n\t\t\t\t(.*)\n\tPassiveActor 3:', data)
resulted_data = x[0]

print(resulted_data)