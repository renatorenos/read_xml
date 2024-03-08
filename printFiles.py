def calc_sum(l: list, sum: float) -> float:
    if l:
        for t in l:
            sum += t[1]
    return round(sum, 4)

# xml = [(113643, 0.32), (113642, 0.37)]

# print(type(xml))
# for i in xml:
#     print(type(i))
#     print(i[1])

total_xml = 0.0
total_fiscal = 0.0

xml = [(1194, 0.54), (1194, 0.54), (119094, 0.62), (119094, 0.62)]
nfc = [(1194, 0.54), (1194, 0.54), (119094, 0.62), (119094, 0.62)]

total_xml = calc_sum(xml, total_xml)
total_fiscal = calc_sum(nfc, total_fiscal)

print(total_xml)
print(total_fiscal)

xml = [(1194, 0.54), (1194, 0.54), (119094, 0.62), (119094, 0.62)]
nfc = [(1194, 0.54), (1194, 0.54), (119094, 0.62), (119094, 0.62)]

total_xml = calc_sum(xml, total_xml)
total_fiscal = calc_sum(nfc, total_fiscal)

print(total_xml)
print(total_fiscal)