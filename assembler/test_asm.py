import util
import asm

def do_test_asm(src, expected):
    a = asm.Assembler(src)
    insts = a.process_asm_inst()
    if insts != expected:
        print "      BYTE | EXPECTED | GOT"
        
        count = 0 
        for (a, b) in zip(expected, insts):
            
            if a != b:
                print "----> %04x   %02x         %02x" % (count, a[1], b[1])
            else:
                print ":     %04x   %02x         %02x" % (count, a[1], b[1])
            count += 1
        util.die("test fails")
        
def do_test_asm_file(srcFile, expected):
    src = open("./tests/asm/" + srcFile + ".uasm").read()
    do_test_asm(src, expected)

def addrfy(xs): return zip(range(len(xs)), xs)
    
def test_1(): do_test_asm_file("test1", addrfy([32,123,123]))
def test_2(): do_test_asm_file("test2", addrfy([42, 0, 0, 42]))
def test_3(): do_test_asm_file("test3", addrfy([42, 0, 0, 0, 42]))
def test_4(): do_test_asm_file("test4", addrfy([0, 0, 0, 0, 42]))
def test_5(): do_test_asm_file("test5", addrfy([0, 0, 0, 0, 42]))
def test_7(): do_test_asm_file("test7", addrfy([0, 0, 1]))
def test_8(): do_test_asm_file("test8", addrfy([0, 0, 0, 8]))
def test_9(): do_test_asm_file("test9", addrfy([2, 3, 5]))
def test_10(): do_test_asm_file("test10", addrfy([7, 11, 13]))

def test_10_1():
    do_test_asm_file("test10_1", addrfy([
        0x00, 0x08, 0x5f, 0x94,
    ]))
    
def test_10_2():
    '''
    CMPLT(r31, r1, r2)
    '''
    do_test_asm_file("test10_2", addrfy([0x00, 0x08, 0x5f, 0x94]))

def test_10_3():
    do_test_asm_file("test10_3", addrfy([0xff, 0xff, 0xe2, 0x73]))

def test_10_4():
    '''//
    . = 12
    start:
    temp = start + start
    ADD(temp, temp, temp)
    
    the problem is that temp is not being added to the symbol
    table. Why?

    '''
    do_test_asm_file("test10_4", addrfy([
        0x00, 0x00, 0x00, 0x00, 
        0x00, 0x00, 0x00, 0x00, 
        0x00, 0x00, 0x00, 0x00, 
        0x00, 0xc0, 0x18, 0x83,
    ]))
    
def test_10_5():
    do_test_asm_file("test10_5", addrfy([0x00, 0x50, 0x4a, 0x81]))
    
def test_11():
    do_test_asm_file("test11", addrfy([0x00, 0x10, 0x61, 0x80,
                                       0x00, 0x18, 0x82, 0x84,
                                       0x00, 0x20, 0xa3, 0xa8]))

def expand_word(s):
    bs = []
    while s != "":
        bs.append(int("0x" + s[:2], 16))
        s = s[2:]
    bs.reverse()
    return bs
    
def test_12(): do_test_asm_file("test12", addrfy(expand_word("7000ffff")))
def test_13(): do_test_asm_file("test13", addrfy(expand_word("7000ffff")))

def test_14(): do_test_asm_file("test14", addrfy(expand_word("00000000") +
                                                 expand_word("7084ffff")))

# def test_15(): do_test_asm_file("fact", addrfy(expand_word("00000014") +
#                                                expand_word("00000000") +
#                                                expand_word("c01f0001") +
#                                                expand_word("641f0004") +
#                                                expand_word("603f0000") +
#                                                expand_word("945f0800") +
#                                                expand_word("73e20008") +
#                                                expand_word("607f0004") +
#                                                expand_word("603f0000") +
#                                                expand_word("88611800") +
#                                                expand_word("647f0004") +
#                                                expand_word("603f0000") +
#                                                expand_word("c4210001") +
#                                                expand_word("643f0000") +
#                                                expand_word("73fffff5")))


def test_16(): do_test_asm_file("test16", addrfy(expand_word("00000000") +
                                                 expand_word("73e4ffff")))

# def test_17(): do_test_asm_file("fact2", addrfy(expand_word("603f0001") +
#                                                 expand_word("945f0800") +
#                                                 expand_word("73e20000")))

# def test_fact_18(): do_test_asm_file("fact3", addrfy(expand_word("73e20000")))
# def test_fact_19(): do_test_asm_file("fact4", addrfy(expand_word("73e20000")))
# def test_fact_19_1(): do_test_asm_file("BEQ", addrfy(expand_word("73e20000"))
# def test_fact_19_2(): do_test_asm_file("BEQ_expanded", addrfy(expand_word("73e20000")))
# def test_long_1(): do_test_asm_file("LONG", addrfy(expand_word("73e20000")))
# def test_dot_1(): do_test_asm_file("dot_1", addrfy(expand_word("03020100")))
# def test_dot_2(): do_test_asm_file("dot_2", addrfy(expand_word("06040200")))
# def test_dot_3(): do_test_asm_file("dot_3", addrfy(expand_word("04ff0100")))

def test_fact_20(): do_test_asm_file("fact20", addrfy(expand_word("04821800")))
def test_fact_21():
    do_test_asm_file("fact21", addrfy(expand_word("80611000") +
                                      expand_word("80611000")))



def test_all_instructions_2():
    do_test_asm_file("all_instructions2",
                     addrfy( expand_word("80a21800") +
                             expand_word("c0a2000b") +
                             expand_word("a0a21800") +
                             expand_word("e0a2000b") +
                             expand_word("88a21800") +
                             expand_word("c8a2000b") +
                             expand_word("8ca21800") +
                             expand_word("cca2000b") +
                             expand_word("a4a21800") +
                             expand_word("e4a2000b") +
                             expand_word("b0a21800") +
                             expand_word("f0a2000b") +
                             expand_word("b4a21800") +
                             expand_word("f4a2000b") +
                             expand_word("b8a21800") +
                             expand_word("f8a2000b") +
                             expand_word("84a21800") +
                             expand_word("c4a2000b") +
                             expand_word("a8a21800") +
                             expand_word("e8a2000b") +
                             expand_word("aca21800") +
                             expand_word("eca2000b") +
                             expand_word("90a21800") +
                             expand_word("d0a2000b") +
                             expand_word("98a21800") +
                             expand_word("d8a2000b") +
                             expand_word("94a21800") +
                             expand_word("d4a2000b") +
                             expand_word("34a2ffe7") +
                             expand_word("70a2ffe6") +
                             expand_word("73e2ffe5") +
                             expand_word("70a2ffe4") +
                             expand_word("73e2ffe3") +
                             expand_word("74a2ffe2") +
                             expand_word("77e2ffe1") +
                             expand_word("74a2ffe0") +
                             expand_word("77e2ffdf") +
                             expand_word("70bfffde") +
                             expand_word("73ffffdd") +
                             expand_word("6ca20000") +
                             expand_word("6fe20000")))


# def test_fact_22():
#     do_test_asm_file("all_instructions",
#                      addrfy( expand_word("80a21800") +
#                              expand_word("c0a2000b") +
#                              expand_word("a0a21800") +
#                              expand_word("e0a2000b") +
#                              expand_word("88a21800") +
#                              expand_word("c8a2000b") +
#                              expand_word("8ca21800") +
#                              expand_word("cca2000b") +
#                              expand_word("a4a21800") +
#                              expand_word("e4a2000b") +
#                              expand_word("b0a21800") +
#                              expand_word("f0a2000b") +
#                              expand_word("b4a21800") +
#                              expand_word("f4a2000b") +
#                              expand_word("b8a21800") +
#                              expand_word("f8a2000b") +
#                              expand_word("84a21800") +
#                              expand_word("c4a2000b") +
#                              expand_word("a8a21800") +
#                              expand_word("e8a2000b") +
#                              expand_word("aca21800") +
#                              expand_word("eca2000b") +
#                              expand_word("90a21800") +
#                              expand_word("d0a2000b") +
#                              expand_word("98a21800") +
#                              expand_word("d8a2000b") +
#                              expand_word("94a21800") +
#                              expand_word("d4a2000b") +
#                              expand_word("34a2ffe7") +
#                              expand_word("70a2ffe6") +
#                              expand_word("73e2ffe5") +
#                              expand_word("70a2ffe4") +
#                              expand_word("73e2ffe3") +
#                              expand_word("74a2ffe2") +
#                              expand_word("77e2ffe1") +
#                              expand_word("74a2ffe0") +
#                              expand_word("77e2ffdf") +
#                              expand_word("70bfffde") +
#                              expand_word("73ffffdd") +
#                              expand_word("6ca20000") +
#                              expand_word("6fe20000")))
    
def test_add_1():
    do_test_asm_file("add",
                     addrfy( expand_word("82a21800") +
                             expand_word("82b66800") +
                             expand_word("80128000") +
                             expand_word("82e0b000") +
                             expand_word("818a3800") +
                             expand_word("83039000") +
                             expand_word("82b43800") +
                             expand_word("80351000") +
                             expand_word("81981000") +
                             expand_word("80e89000") +
                             expand_word("806b5800") +
                             expand_word("82166000") +
                             expand_word("81b18000") +
                             expand_word("82d59800") +
                             expand_word("8143c800") +
                             expand_word("810c9800") +
                             expand_word("81e00800") +
                             expand_word("81362800") +
                             expand_word("8152a000") +
                             expand_word("8024a800")))
    
def test_assn_1():
    do_test_asm_file("assn1", addrfy( expand_word("80611000")))

def test_assn_2():
    do_test_asm_file("assn2", addrfy( expand_word("80611000")))




    





# def test_1fact():
#     do_test_asm_file("fact", addrfy(
#         [ 0x14, 0x00, 0x00, 0x00,
#           0x00, 0x00, 0x00, 0x00,
#           0x01, 0x00, 0x1f, 0xc0,
#           0x04, 0x00, 0x1f, 0x64,
#           0x00, 0x00, 0x3f, 0x60,
#           0x00, 0x08, 0x5f, 0x94,
#           0x08, 0x00, 0xe2, 0x73,
#           0x04, 0x00, 0x7f, 0x60,
#           0x00, 0x00, 0x3f, 0x60,
#           0x00, 0x18, 0x61, 0x88,
#           0x04, 0x00, 0x7f, 0x64,
#           0x00, 0x00, 0x3f, 0x60,
#           0x01, 0x00, 0x21, 0xc4,
#           0x00, 0x00, 0x3f, 0x64,
#           0xf5, 0xff, 0xff, 0x73,
#       ]))
    
# def test_fact():
#     do_test_asm_file("fact", addrfy(
#         [ 0x14, 0x00, 0x00, 0x00,
#           0x00, 0x00, 0x00, 0x00,
#           0x01, 0x00, 0x1f, 0xc0,
#           0x04, 0x00, 0x1f, 0x64,
#           0x00, 0x00, 0x3f, 0x60,
#           0x00, 0x08, 0x5f, 0x94,
#           0x08, 0x00, 0xe2, 0x73,
#           0x04, 0x00, 0x7f, 0x60,
#           0x00, 0x00, 0x3f, 0x60,
#           0x00, 0x18, 0x61, 0x88,
#           0x04, 0x00, 0x7f, 0x64,
#           0x00, 0x00, 0x3f, 0x60,
#           0x01, 0x00, 0x21, 0xc4,
#           0x00, 0x00, 0x3f, 0x64,
#           0xf5, 0xff, 0xff, 0x73,
#       ]))

# def test_fact():
#     do_test_asm_file("fact", addrfy(
#         [ 0x14, 0x00, 0x00, 0x00,
#           0x00, 0x00, 0x00, 0x00,
#           0x01, 0x00, 0x1f, 0xc0,
#           0x04, 0x00, 0x1f, 0x64,
#           0x00, 0x00, 0x3f, 0x60,
#           0x00, 0x08, 0x5f, 0x94,
#           0x08, 0x00, 0xe2, 0x73,
#           0x04, 0x00, 0x7f, 0x60,
#           0x00, 0x00, 0x3f, 0x60,
#           0x00, 0x18, 0x61, 0x88,
#           0x04, 0x00, 0x7f, 0x64,
#           0x00, 0x00, 0x3f, 0x60,
#           0x01, 0x00, 0x21, 0xc4,
#           0x00, 0x00, 0x3f, 0x64,
#           0xf5, 0xff, 0xff, 0x73,
#       ]))


    
# def test_include():
#     do_test_asm_file("test_include", [])




