def main():
    td = [[0,0,0],[0,1,0],[1,0,0],[1,1,1]]
    w1,w2,t = 0.7,0.2,0.5

    print("training data set \n x1 \t x2 \t y \n ")
    for i in range(4):
        for j in range(3):
            print(f'{td[i][j]} \t ')
        print("\n")

if __name__ == '__main__':
    main()
    