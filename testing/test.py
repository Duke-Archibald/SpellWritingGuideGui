def genbin(n, bs = ''):
    if n-1:
        genbin(n-1, bs + '0')
        genbin(n-1, bs + '1')
    else:
        print('1' + bs)

genbin(3)
