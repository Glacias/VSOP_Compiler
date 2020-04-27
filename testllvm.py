import llvmlite.ir as ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE


def main():
    m = ir.Module()
    func_ty = ir.FunctionType(ir.VoidType(), []) #defining printer function as type void
    func = ir.Function(m, func_ty, name="printer") #define function as printer
    builder = ir.IRBuilder(func.append_basic_block('entry')) #defining the entry point of the function printer

    fmt = "%s\n\0" #in function printf allows for inserting arg in, next global_fmt statements allow for creating @"fstr" assignment
    c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                        bytearray(fmt.encode("utf8")))
    global_fmt = ir.GlobalVariable(m, c_fmt.type, name="fstr")
    global_fmt.linkage = 'internal'
    global_fmt.global_constant = True
    global_fmt.initializer = c_fmt

    arg = "Hello, World!\0" #args will be passed into printf function.
    c_str_val = ir.Constant(ir.ArrayType(ir.IntType(8), len(arg)),
                            bytearray(arg.encode("utf8"))) #creates the c_str_value as a constant

    printf_ty = ir.FunctionType(ir.IntType(32), [], var_arg=True) #creation of the printf function begins here and specifies the passing of a argument
    printf = ir.Function(m, printf_ty, name="printf")    

    c_str = builder.alloca(c_str_val.type) #creation of the allocation of the %".2" variable
    builder.store(c_str_val, c_str) #store as defined on the next line below %".2"

    voidptr_ty = ir.IntType(8).as_pointer() 
    fmt_arg = builder.bitcast(global_fmt, voidptr_ty) #creates the %".4" variable with the point pointing to the fstr
    builder.call(printf, [fmt_arg, c_str]) #We are calling the prinf function with the fmt and arg and returning the value as defiend on the next line
    builder.ret_void()

    #Next lines are for calling llvm and returning the assembly.
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    print(str(m)) #PRINTING OUT THE ASSEMBLY
    llvm_module = llvm.parse_assembly(str(m)) #Parsing teh assembly
    tm = llvm.Target.from_default_triple().create_target_machine() #creating the target machine

    with llvm.create_mcjit_compiler(llvm_module, tm) as ee:
        ee.finalize_object() #Making sure all modules owned by the execution engine are fully processed and usable for execution
        fptr = ee.get_function_address("printer") #fptr will reference the printer function
        py_func = CFUNCTYPE(None)(fptr)
        py_func() #run the function printer

if __name__ == "__main__":
    main()
