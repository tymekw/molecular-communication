import random
import subprocess

sychro_map = {'1': [1,0,0,1,0,0,1,0,0],
              '2': [1,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,
                    1,0,0,0,0],
              '3': [1,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,
                    0,0,0,0,0,0,10,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,
                    1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,10,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,1,0,0,0,
                    0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,10,0,0,0,0,0]}


# BIT_SEQUENCE_LIST

ACCORD_HOME = "C:\\Users\\P1\\Desktop\\AcCoRD-1.4.2"
ACCORD_EXEC = ACCORD_HOME + "\\bin\\accord_win.exe"
with open('template.txt', 'r') as file:
    template = file.readlines()

modulation_strength = [25, 50, 75, 100, 125, 150]
modulation_bits = [1,2,3]
template_str = "".join(template)

for current_seed in range(1, 4):
    template_with_seed = template_str.replace("$SEED$", str(current_seed))
    for mod_str in modulation_strength:
        print("dupa")
        template_with_mod_str = template_with_seed.replace("$MODULATION_STR$", str(mod_str))
        for m_bit in modulation_bits:
            template_str_withM_mod_level = template_with_mod_str.replace("$MODULATION_BITS$", str(2))
            automate_result_output_filename = "automate_results_SEED_{}_MOD_LVL_{}_MOD_STR_{}_MOD_BITS_{}.txt".format(str(current_seed), str(2), str(mod_str), str(m_bit))
            bits = sychro_map[str(m_bit)] + [random.randint(0,1) for _ in range(256)]
            replaced_bits = template_str_withM_mod_level.replace("$BIT_SEQUENCE_LIST$", str(bits))

            final_config = replaced_bits.replace("$OUTPUT_FILENAME$", automate_result_output_filename)
            config_name = "automate_config_{}_{}_{}.txt".format(str(2), str(mod_str), str(m_bit))
            with open(ACCORD_HOME + "\\config\\{}".format(config_name), 'w+') as file:
                file.write(final_config)
            # for i in range(0, 10):
            command = [ACCORD_EXEC, config_name]
            output = subprocess.check_output(command, cwd=ACCORD_HOME + "\\bin", shell=True)

            print("output: ", str(output))

