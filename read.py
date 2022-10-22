from parser import Crypto

def read_crypto():
    f = open("output.out", "r")
    i = 0
    set = []
    for line in f:
        if i % 2 == 0:
            q = line[:-1:].split(";")
            a = Crypto(q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7], q[8])
            set.append(a)
        else:
            q = line[:-2:].split(";")
            for j in q:
                jj = j.split(":")
                if len(jj) > 2:
                    strr = jj[1] + ":"
                    for kk in range(2, len(jj)):
                        strr += jj[kk]
                    jj[1] = strr
                set[i // 2].more_info[jj[0]] = jj[1]
        i += 1
    return set