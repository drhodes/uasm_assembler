import uasm_assembler


def test_1():
    app = uasm_assembler.App(as_main=False)
    app.set_endian_little()
    app.set_includes(["./test/src"])    
    app.set_infiles(["./test/src/test_1.uasm"])
    app.set_outfile("/tmp/out1.bin")

    fileset = app.discover_all_sources()
    assert fileset == set(['./test/src/beta.uasm',
                           './test/src/test_2.uasm',
                           './test/src/test_3.uasm',
                           './test/src/test_1.uasm'])
    return app

def test_12():
    app = test_1()
    app.assemble()
    
