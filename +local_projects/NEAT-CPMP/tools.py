import sys

def progressbar(it, prefix="", size=60, file=sys.stdout, out=['None']):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %s\r" % (prefix, "#"*x, "."*(size-x), out[0]))
        file.flush()
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    #file.write("\n")
    file.write(prefix + out[0] + " "*2*size+"\n")
    file.flush()