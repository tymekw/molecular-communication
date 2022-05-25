import random
import subprocess
import re
from main import Demodulator
from main import calculate_ber

sychro_map = {'1': [1, 0, 0] * 3,
              '2': [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0] * 3,
              '3': [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0] * 3
              }

TEMPLATE_NAME = 'template_dist8.txt'
RESULTS_NAME = 'results_dist8.txt'
current_seed = 1

# BIT_SEQUENCE_LIST
results = ''
try:
    ACCORD_HOME = "D:\\AGH\\II STOPIEŃ\\es\\molecular_dist8"
    ACCORD_EXEC = ACCORD_HOME + "\\bin\\accord_win.exe"
    with open(TEMPLATE_NAME, 'r') as file:
        template = file.readlines()

    modulation_strength = [25, 50, 75, 100, 125]
    modulation_bits = [1, 2, 3]
    template_str = "".join(template)

    template_with_seed = template_str.replace("$SEED$", str(current_seed))
    for mod_str in modulation_strength:
        print("!!!RUN NEXT MOD STR!!!")
        template_with_mod_str = template_with_seed.replace("$MODULATION_STR$", str(mod_str))
        for m_bit in modulation_bits:
            # BIT_SEQUENCE_LIST
            results = ''
            template_str_withM_mod_level = template_with_mod_str.replace("$MODULATION_BITS$", str(m_bit))
            automate_result_output_filename = "automate_results_SEED_{}_MOD_LVL_{}_MOD_STR_{}".format(
                str(current_seed), str(m_bit), str(mod_str))
            expected_bits = [random.randint(0, 1) for _ in range(256)]
            if m_bit == 3:
                expected_bits.append(0)
                expected_bits.append(0)
            bits = sychro_map[str(m_bit)] + expected_bits
            replaced_bits = template_str_withM_mod_level.replace("$BIT_SEQUENCE_LIST$", str(bits))

            final_config = replaced_bits.replace("$OUTPUT_FILENAME$", automate_result_output_filename)
            config_name = "automate_config_{}_{}.txt".format(str(m_bit), str(mod_str))
            print("Write conf file")
            with open(ACCORD_HOME + "\\config\\{}".format(config_name), 'w+') as file:
                file.write(final_config)
            # for i in range(0, 10):
            command = [ACCORD_EXEC, config_name]
            print("run command")
            print('SEED: {}; MOD_LVL:{} MOD_STR: {}\n'.format(str(current_seed), str(m_bit),
                                                                                 str(mod_str)))
            try:
                output = subprocess.check_output(command, cwd=ACCORD_HOME + "\\bin", timeout=60*60*2)
            except subprocess.TimeoutExpired:
                results += 'RESULTS_SEED_{}_MOD_LVL_{}_MOD_STR_{}\nBER: 1\n'.format(str(current_seed), str(m_bit),
                                                                                 str(mod_str))
                results += "TIMED OUT!!!!!\n\n"
                print('RESULTS_SEED_{}_MOD_LVL_{}_MOD_STR_{}\nBER: 1\n'.format(str(current_seed), str(m_bit),str(mod_str)))
                print("TIMED OUT")
                with open(RESULTS_NAME, 'a+') as file:
                    file.write(results)
                continue

            result_full_path = ACCORD_HOME + '\\bin\\results\\' + automate_result_output_filename + \
                               '_SEED{}.txt'.format(current_seed)

            print("read file")
            with open(result_full_path, 'r') as file:
                data = ''.join(file.readlines())

            x = re.findall(r'Count:\n\t\t\t\t(.*) ', data)
            resulted_data = x[0]
            print("Demodulator")
            demodulator = Demodulator(raw_data=resulted_data,
                                      symbol_len=100,
                                      modulation_bits=m_bit,
                                      sync_seq_rep=3)
            print("Thresholds")
            demodulator.calculate_thresholds()
            print("sum")
            demodulator.sum_received_molecules()
            print("decode")
            decoded = demodulator.decode()
            print("Demodulate")
            demodulated = demodulator.demodulate(decoded)
            print("ber")
            ber = calculate_ber([int(i) for i in list(demodulated)], expected_bits)
            results += 'RESULTS_SEED_{}_MOD_LVL_{}_MOD_STR_{}\nBER: {}\n'.format(str(current_seed), str(m_bit),
                                                                                 str(mod_str), str(ber))
            results += "len:{}\n".format(len(demodulated))
            results += "d:{}\n".format(" ".join(demodulated))
            results += "e:{}\n\n".format(" ".join([str(i) for i in expected_bits]))
            print(results)
            print("Write res")
            with open(RESULTS_NAME, 'a+') as file:
                file.write(results)

except Exception as e:
    print(e)
    with open(RESULTS_NAME, 'a+') as file:
        file.write(results)
