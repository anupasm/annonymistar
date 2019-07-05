import math
import Levenshtein as lev

COST_WEIGHTS = {
    "insert":1,
    "replace":3,
    "delete": 2
}

def get_consecutive_count(word,char):
    count=0
    for i in word:
        if i == char:
            count+=1
        else:
            break
    return count

def exec_op(op,source_word,pos,char):
    part1 = source_word[:pos]
    part2 = source_word[pos:] if op == 'insert' else source_word[pos+1:]#if pos < len(source_word) else ''  
    print("parts",part1,part2)
    consecutive_count_1 = get_consecutive_count(part1[::-1],char)
    consecutive_count_2 = 0 #get_consecutive_count(part2,char)
    total = consecutive_count_1+consecutive_count_2+1 #min 1 (denote the inserted char)
    cost = (COST_WEIGHTS[op]*len(source_word))/total
    # cost = (COST_WEIGHTS[op])/total
    print(op,"total",total,"weight",COST_WEIGHTS[op],"cost",cost)
    # print(part1,part2,cost)
    return part1,part2,cost

def exec_ops(source_word,target_word,cost):
    
    adjusted_word = source_word
    ops = lev.editops(adjusted_word,target_word)
    print(ops,adjusted_word)    

    if not ops: 
        return cost
    op = ops[0]
    action = op[0]
    source_pos = op[1]
    target_pos = op[2]
    char = source_word[source_pos] if op[0] == 'delete' else target_word[target_pos]
    part1,part2,op_cost = exec_op(action,adjusted_word,source_pos,char)
    char = '' if op[0]=='delete' else char #remove char from adjusted word
    adjusted_word = part1 + char + part2 
    cost += op_cost
    return exec_ops(adjusted_word,target_word,cost)
        
# def exec_insert(op,source_word,target_word):
#     insert_pos = op[1]
#     insert_char = target_word[op[2]]
#     part1 = source_word[:insert_pos-1] if insert_pos != 0 else ''
#     part2 = source_word[insert_pos+1:] if insert_pos+1 < len(source_word) else ''  
#     consecutive_count_1 = get_consecutive_count(part1[::-1],insert_char)
#     consecutive_count_2 = get_consecutive_count(part2,insert_char)
#     total = consecutive_count_1+consecutive_count_2+1 #min 1 (denote the inserted char)
#     cost = COST_WEIGHTS['insert']/(total)
#     adjusted_word = part1 + insert_char + part2

#     return adjusted_word,cost

flag = 0

def cost_to_create(source,size):
    return get_cost(source,'') * size

def get_cost(source_word,target_word,action_count=None):
    ops = lev.editops(source_word,target_word)
    if flag: print(ops)
    total_cost = 0
    for op in ops:
        action = op[0]
        if action_count: action_count[action] +=1 
        source_pos = op[1]
        target_pos = op[2]
        char = source_word[source_pos] if action == 'delete' else target_word[target_pos]
        if flag: print(char)
        part1 = source_word[:source_pos]
        part2 = source_word[source_pos:] if action == 'insert' else source_word[source_pos+1:]#if pos < len(source_word) else ''  
        if flag: print(action,part1,part2)
        consecutive_count_1 = get_consecutive_count(part1[::-1],char)
        consecutive_count_2 = get_consecutive_count(part2,char)
        total = consecutive_count_1+consecutive_count_2+1 #min 1 (denote the inserted/replaced/deleted char)
        source_len = len(source_word)
        if flag: print(op,"total",total,"weight",COST_WEIGHTS[action],"source len",source_len)
        cost = COST_WEIGHTS[action]/(total/source_len) #if action == 'delete' else COST_WEIGHTS[action]*(total/source_len)
        total_cost += cost
        if flag: print("cost",cost)
    if flag: print(total_cost)
    if not action_count:
        return total_cost
    return total_cost,action_count 


if __name__ == "__main__":
    n1_e ='ssss'
    n2_e = 'sssst'

    x = [1,2,3,4,5]
    print(get_cost(n1_e,n2_e))

    n1_e ='sssst'
    n2_e = 'ssss'

    x = [1,2,3,4,5]
    print(get_cost(n1_e,n2_e))

    n1_e ='sssst'
    n2_e = 'sssstt'

    x = [1,2,3,4,5]
    print(get_cost(n1_e,n2_e))