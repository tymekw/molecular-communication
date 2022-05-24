import os
import re
import subprocess

ACCORD_HOME = "C:\\Users\\P1\\Desktop\\AcCoRD-1.4.2"
ACCORD_EXEC = ACCORD_HOME + "\\bin\\accord_win.exe"
with open('template.txt', 'r') as file:
    template = file.readlines()

modulation_strength = [25, 50, 75, 100, 125, 150]
template_str = "".join(template)

for current_seed in range(1, 3):
    template_str_withM_mod_level = template_str.replace("$MODULATION_BITS$", str(2))
    template_with_seed = template_str_withM_mod_level.replace("$SEED$", str(current_seed))
    for mod_str in modulation_strength:
        print("dupa")
        template_with_mod_str = template_with_seed.replace("$MODULATION_STR$", str(mod_str))
        automate_result_output_filename = "automate_results_SEED_{}_MOD_LVL_{}_MOD_STR_{}.txt".format(str(current_seed), str(2), str(mod_str))
        final_config = template_with_mod_str.replace("$OUTPUT_FILENAME$", automate_result_output_filename)
        config_name = "automate_config_{}_{}.txt".format(str(2), str(mod_str))
        with open(ACCORD_HOME + "\\config\\{}".format(config_name), 'w+') as file:
            file.write(final_config)
        # for i in range(0, 10):
        command = [ACCORD_EXEC, config_name]
        output = subprocess.check_output(command, cwd=ACCORD_HOME + "\\bin", shell=True)
        print("output: ", str(output))

