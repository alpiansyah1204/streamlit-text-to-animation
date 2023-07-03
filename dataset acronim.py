def longest_common_substring(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)
    lcs_matrix = [[0] * (len_str2 + 1) for _ in range(len_str1 + 1)]

    for i in range(1, len_str1 + 1):
        for j in range(1, len_str2 + 1):
            if str1[i-1] == str2[j-1]:
                lcs_matrix[i][j] = lcs_matrix[i-1][j-1] + 1
            else:
                lcs_matrix[i][j] = max(lcs_matrix[i-1][j], lcs_matrix[i][j-1])

    return lcs_matrix[len_str1][len_str2]

def choose_string(input_string, string_list):
    max_lcs = 0
    selected_string = ''

    for string in string_list:
        lcs_length = longest_common_substring(input_string, string)
        if lcs_length > max_lcs:
            max_lcs = lcs_length
            selected_string = string

    return selected_string

print(choose_string('lapr',['lapi','lapar']))