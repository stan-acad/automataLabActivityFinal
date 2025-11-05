from typing import Dict, Tuple
import json

mealy: Dict[str, Dict[str, Tuple[str, str]]] = {
    'A': {'0': ('A', 'A'), '1': ('A', 'B')},
    'B': {'0': ('C', 'A'), '1': ('D', 'B')},
    'C': {'0': ('D', 'C'), '1': ('B', 'B')},
    'D': {'0': ('B', 'B'), '1': ('C', 'C')},
    'E': {'0': ('D', 'C'), '1': ('E', 'C')},
}

initial_mealy = 'A'
example_inputs = ["00110", "11001", "1010110", "101111"]

def simulate_mealy(machine, start, input_str):
    s = start
    outputs = []
    for ch in input_str:
        s, out = machine[s][ch]
        outputs.append(out)
    return ''.join(outputs)

def convert_mealy_to_moore(mealy, initial):
    moore_states = {"START": '-'}
    for q, trans in mealy.items():
        for a, (r, o) in trans.items():
            moore_states[f"{r}__{o}"] = o

    moore_to_mealy = {name: (initial if name == "START" else name.split("__", 1)[0])
                      for name in moore_states}
    moore_trans = {name: {} for name in moore_states}

    for a in ['0', '1']:
        r, o = mealy[initial][a]
        moore_trans["START"][a] = f"{r}__{o}"

    for ms in moore_states:
        if ms == "START": continue
        mealy_state = moore_to_mealy[ms]
        for a in ['0', '1']:
            r, o = mealy[mealy_state][a]
            moore_trans[ms][a] = f"{r}__{o}"

    return {'states': moore_states, 'start': 'START', 'trans': moore_trans}

def simulate_moore(moore, input_str):
    s = moore['start']
    outputs = [moore['states'][s]]
    for ch in input_str:
        s = moore['trans'][s][ch]
        outputs.append(moore['states'][s])
    return ''.join(outputs), outputs

moore = convert_mealy_to_moore(mealy, initial_mealy)

results = []
for inp in example_inputs:
    mealy_out = simulate_mealy(mealy, initial_mealy, inp)
    moore_raw, moore_list = simulate_moore(moore, inp)
    moore_aligned = ''.join(moore_list[1:])
    results.append({
        'input': inp,
        'mealy_output': mealy_out,
        'moore_output': moore_aligned
    })

print(json.dumps(results, indent=2))
