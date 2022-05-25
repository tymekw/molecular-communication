import os
import re
from main import Demodulator, calculate_ber


def get_dist(seed):
    if 9 > int(seed) > 4:
        return '4'
    elif int(seed) > 8:
        return '8'
    else:
        return '2'


directory = os.fsencode('results/')
resultaty = ''
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    tmp = filename.split("_")
    seed = tmp[3]
    dist = get_dist(seed)
    mod_lvl = tmp[6]
    mod_str = tmp[9]

    with open('big_res.txt', 'r') as res:
        data = ''.join(res.readlines())
    expected = re.findall(r'{}\nBER: .*\nd:.*\n(.*)\n\n'.format('RESULTS_'+ '_'.join(tmp[2:-1])), data)
    # x = re.findall(r'{}\nBER: .*\n(.*)\ne:.*\n'.format('RESULTS_'+ '_'.join(tmp[2:-1])), data)

    exp_data = expected[0][3:]
    # if mod_lvl == 3:
    #     exp_data = exp_data[-258:]
    # else:
    #     exp_data = exp_data[-256:]
    with open('results/'+filename, 'r') as res:
        data = ''.join(res.readlines())
    x = re.findall(r'Count:\n\t\t\t\t(.*)\n\tPassiveActor 3:', data)
    resulted_data = x[0]
    print(resulted_data)
    print("Demodulator")
    demodulator = Demodulator(raw_data=resulted_data,
                              symbol_len=100,
                              modulation_bits=int(mod_lvl),
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
    exp_data = exp_data.strip().split(" ")
    ber = calculate_ber([int(i) for i in list(demodulated)], [int(i) for i in exp_data])
    resultaty += str(ber) + '\n'
    print('ok')
print(resultaty)
print('OK')
