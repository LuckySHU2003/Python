def transpose(matrix):
    # 获取矩阵的行数和列数
    rows = len(matrix)
    cols = len(matrix[0])
    
    # 创建一个空的转置矩阵
    transposed_matrix = [[0] * rows for _ in range(cols)]
    
    # 遍历原矩阵，并将对应元素放入转置矩阵中
    for i in range(rows):
        for j in range(cols):
            transposed_matrix[j][i] = matrix[i][j]
    
    return transposed_matrix

# 示例矩阵
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]

# 打印转置矩阵
result = transpose(matrix)
for row in result:
    print(row)
