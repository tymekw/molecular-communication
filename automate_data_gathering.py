import re
import subprocess
with open('template.txt', 'r') as file:
    template = file.readlines()

template_str = "".join(template)
k = template_str.replace("$SEED$", str(current_seed))

# for i in range(0, 10):
#     command = ['./waf', '--run "--nWifiJammers={}"'.format(str(i))]
#     th = []
#     for _ in range(10):
#         output = subprocess.check_output(command)
#         result = re.findall(" .* Mbit/s", str(output))[0].split(" ")[-2]
#         th.append(result)
#     results[str(i)] = th

    with open("wyniki.txt", 'a+') as file:
        file.writelines(str(results[str(i)]))