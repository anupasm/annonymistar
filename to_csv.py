import json
out = [{2: {0: {'action_counts': {'delete': 53, 'insert': 13, 'replace': 7}, 'iterations': 4, 'total': 458.5583583083583}, 1: {'action_counts': {'delete': 206, 'insert': 76, 'replace': 38}, 'iterations': 10, 'total': 1358.1670995670995}, 2: {'action_counts': {'delete': 306, 'insert': 70, 'replace': 29}, 'iterations': 6, 'total': 1363.700912842387}, 3: {'action_counts': {'delete': 664, 'insert': 95, 'replace': 51}, 'iterations': 6, 'total': 2396.9374329577076}, 4: {'action_counts': {'delete': 230, 'insert': 55, 'replace': 36}, 'iterations': 7, 'total': 1390.430390473454}, 5: {'action_counts': {'delete': 399, 'insert': 243, 'replace': 43}, 'iterations': 5, 'total': 2983.5052589581455}, 6: {'action_counts': {'delete': 390, 'insert': 124, 'replace': 36}, 'iterations': 5, 'total': 2057.09944996591}, 7: {'action_counts': {'delete': 364, 'insert': 85, 'replace': 58}, 'iterations': 5, 'total': 2306.6701191600523}, 8: {'action_counts': {'delete': 339, 'insert': 137, 'replace': 26}, 'iterations': 5, 'total': 1973.9016605657782}, 9: {'action_counts': {'delete': 415, 'insert': 256, 'replace': 47}, 'iterations': 4, 'total': 3638.1644285591383}, 10: {'action_counts': {'delete': 421, 'insert': 104, 'replace': 27}, 'iterations': 4, 'total': 3007.2633779870707}, 11: {'action_counts': {'delete': 242, 'insert': 60, 'replace': 37}, 'iterations': 5, 'total': 2690.7729802479794}}},
{3: {0: {'action_counts': {'replace': 8, 'delete': 71, 'insert': 16}, 'total': 499.04926739926736, 'iterations': 4}, 1: {'action_counts': {'replace': 41, 'delete': 354, 'insert': 98}, 'total': 1721.2137265512267, 'iterations': 13}, 2: {'action_counts': {'replace': 36, 'delete': 428, 'insert': 106}, 'total': 1652.9915076463822, 'iterations': 7}, 3: {'action_counts': {'replace': 54, 'delete': 579, 'insert': 268}, 'total': 2401.9892717228495, 'iterations': 8}, 4: {'action_counts': {'replace': 35, 'delete': 300, 'insert': 88}, 'total': 1624.3345091415367, 'iterations': 10}, 5: {'action_counts': {'replace': 42, 'delete': 680, 'insert': 245}, 'total': 3765.883455906951, 'iterations': 7}, 6: {'action_counts': {'replace': 37, 'delete': 542, 'insert': 173}, 'total': 2524.324633275134, 'iterations': 9}, 7: {'action_counts': {'replace': 71, 'delete': 456, 'insert': 176}, 'total': 2843.8276037809355, 'iterations': 7}, 8: {'action_counts': {'replace': 26, 'delete': 558, 'insert': 180}, 'total': 2461.3937121786716, 'iterations': 9}, 9: {'action_counts': {'replace': 46, 'delete': 752, 'insert': 210}, 'total': 5866.389210476531, 'iterations': 11}, 10: {'action_counts': {'replace': 21, 'delete': 565, 'insert': 113}, 'total': 4827.100482378019, 'iterations': 6}, 11: {'action_counts': {'replace': 46, 'delete': 305, 'insert': 97}, 'total': 2968.858501396766, 'iterations': 7}}},
{4: {0: {'total': 549.2222471972472, 'iterations': 8, 'action_counts': {'replace': 5, 'insert': 19, 'delete': 79}}, 1: {'total': 1823.4403018764867, 'iterations': 14, 'action_counts': {'replace': 40, 'insert': 103, 'delete': 379}}, 2: {'total': 1761.5493165041908, 'iterations': 11, 'action_counts': {'replace': 33, 'insert': 117, 'delete': 464}}, 3: {'total': 2868.348261344339, 'iterations': 11, 'action_counts': {'replace': 54, 'insert': 279, 'delete': 766}}, 4: {'total': 1721.188406665581, 'iterations': 12, 'action_counts': {'replace': 35, 'insert': 104, 'delete': 347}}, 5: {'total': 3843.9027430301503, 'iterations': 9, 'action_counts': {'replace': 42, 'insert': 289, 'delete': 682}}, 6: {'total': 2676.2026674398708, 'iterations': 10, 'action_counts': {'replace': 37, 'insert': 221, 'delete': 595}}, 7: {'total': 3247.8609360067626, 'iterations': 10, 'action_counts': {'replace': 59, 'insert': 205, 'delete': 615}}, 8: {'total': 2653.7712700176303, 'iterations': 12, 'action_counts': {'replace': 26, 'insert': 248, 'delete': 631}}, 9: {'total': 6025.16746289346, 'iterations': 15, 'action_counts': {'replace': 51, 'insert': 233, 'delete': 934}}, 10: {'total': 4734.5041716998485, 'iterations': 7, 'action_counts': {'replace': 19, 'insert': 152, 'delete': 575}}, 11: {'total': 2890.390149460032, 'iterations': 8, 'action_counts': {'replace': 48, 'insert': 108, 'delete': 305}}}},
{5: {0: {'action_counts': {'replace': 5, 'delete': 81, 'insert': 22}, 'iterations': 8, 'total': 555.7500249750249}, 1: {'action_counts': {'replace': 44, 'delete': 364, 'insert': 108}, 'iterations': 15, 'total': 1789.7131920582}, 2: {'action_counts': {'replace': 29, 'delete': 479, 'insert': 152}, 'iterations': 13, 'total': 1789.9374743989283}, 3: {'action_counts': {'replace': 56, 'delete': 679, 'insert': 347}, 'iterations': 11, 'total': 2751.4144656433405}, 4: {'action_counts': {'replace': 38, 'delete': 343, 'insert': 120}, 'iterations': 14, 'total': 1799.7530114725384}, 5: {'action_counts': {'replace': 47, 'delete': 694, 'insert': 314}, 'iterations': 10, 'total': 3801.5693768048723}, 6: {'action_counts': {'replace': 35, 'delete': 641, 'insert': 228}, 'iterations': 10, 'total': 2819.168601505805}, 7: {'action_counts': {'replace': 63, 'delete': 531, 'insert': 278}, 'iterations': 12, 'total': 3109.1831978061214}, 8: {'action_counts': {'replace': 26, 'delete': 616, 'insert': 281}, 'iterations': 11, 'total': 2677.224833679475}, 9: {'action_counts': {'replace': 46, 'delete': 945, 'insert': 248}, 'iterations': 16, 'total': 5929.424720768743}, 10: {'action_counts': {'replace': 20, 'delete': 651, 'insert': 188}, 'iterations': 12, 'total': 4767.717726512255}, 11: {'action_counts': {'replace': 46, 'delete': 322, 'insert': 115}, 'iterations': 8, 'total': 3089.1417340803678}}}]

print('k week insert_count delete_count replace_count cost iterations')
for k in out:
    for w,d1 in k.items():
        for m,d2 in d1.items(): 
            print(w,m,d2['action_counts']['insert'],d2['action_counts']['delete'],d2['action_counts']['replace'],d2['total'],d2['iterations'])

