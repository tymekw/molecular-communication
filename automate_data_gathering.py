import random
import subprocess
import re
from main import Demodulator
from main import calculate_ber

sychro_map = {'1': [1, 0, 0, 1, 0, 0, 1, 0, 0],
              '2': [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0,
                    0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                    1, 0, 0, 0, 0],
              '3': [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1,
                    0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0,
                    0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0,
                    0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10,
                    0, 0, 0, 0, 0]}

# BIT_SEQUENCE_LIST
results = ''
try:
    ACCORD_HOME = "D:\\AGH\\II STOPIEŃ\\es\\molecular"
    ACCORD_EXEC = ACCORD_HOME + "\\bin\\accord_win.exe"
    with open('template.txt', 'r') as file:
        template = file.readlines()

    modulation_strength = [25, 50, 75, 100, 125, 150]
    modulation_bits = [1, 2, 3]
    template_str = "".join(template)

    for current_seed in range(1, 4):
        template_with_seed = template_str.replace("$SEED$", str(current_seed))
        for mod_str in modulation_strength:
            print("dupa")
            template_with_mod_str = template_with_seed.replace("$MODULATION_STR$", str(mod_str))
            for m_bit in modulation_bits:
                template_str_withM_mod_level = template_with_mod_str.replace("$MODULATION_BITS$", str(m_bit))
                automate_result_output_filename = "automate_results_SEED_{}_MOD_LVL_{}_MOD_STR_{}".format(
                    str(current_seed), str(m_bit), str(mod_str))
                expected_bits = [random.randint(0, 1) for _ in range(256)]
                bits = sychro_map[str(m_bit)] + expected_bits
                replaced_bits = template_str_withM_mod_level.replace("$BIT_SEQUENCE_LIST$", str(bits))

                final_config = replaced_bits.replace("$OUTPUT_FILENAME$", automate_result_output_filename)
                config_name = "automate_config_{}_{}.txt".format(str(m_bit), str(mod_str))
                with open(ACCORD_HOME + "\\config\\{}".format(config_name), 'w+') as file:
                    file.write(final_config)
                # for i in range(0, 10):
                command = [ACCORD_EXEC, config_name]
                output = subprocess.check_output(command, cwd=ACCORD_HOME + "\\bin", shell=True)

                result_full_path = ACCORD_HOME + '\\bin\\result\\' + automate_result_output_filename + \
                                   '_SEED{}.txt'.format(m_bit)

                with open(result_full_path, 'r') as file:
                    data = ''.join(file.readlines())

                x = re.findall(r'Count:\n\t\t\t\t(.*)\n\tPassiveActor 3:', data)
                resulted_data = x[0]
                print(resulted_data)
                demodulator = Demodulator(raw_data=resulted_data,
                                          symbol_len=100,
                                          modulation_bits=m_bit,
                                          sync_seq_rep=3)
                demodulator.calculate_thresholds()
                demodulator.sum_received_molecules()
                decoded = demodulator.decode()
                demodulated = demodulator.demodulate(decoded)

                ber = calculate_ber([int(i) for i in list(demodulated)], expected_bits)
                results += 'RESULTS_SEED_{}_MOD_LVL_{}_MOD_STR_{}\nBER: {}\n\n'.format(str(current_seed), str(m_bit),
                                                                                       str(mod_str), str(ber))
                print(results)
                with open('results.txt', 'w+') as file:
                    file.write(results)
except Exception as e:
    print(e)
    with open('results.txt', 'w+') as file:
        file.write(results)
