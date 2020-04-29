	.text
	.file	"llvmTest.ll"
	.globl	Object_print            # -- Begin function Object_print
	.p2align	4, 0x90
	.type	Object_print,@function
Object_print:                           # @Object_print
	.cfi_startproc
# %bb.0:
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset %rbx, -16
	movq	%rdi, %rbx
	movl	$.str, %edi
	xorl	%eax, %eax
	callq	printf
	movq	%rbx, %rax
	popq	%rbx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	Object_print, .Lfunc_end0-Object_print
	.cfi_endproc
                                        # -- End function
	.globl	Object_printBool        # -- Begin function Object_printBool
	.p2align	4, 0x90
	.type	Object_printBool,@function
Object_printBool:                       # @Object_printBool
	.cfi_startproc
# %bb.0:
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset %rbx, -16
	movq	%rdi, %rbx
	movl	$.str.1, %ecx
	movl	$.str.2, %eax
	testl	%esi, %esi
	cmovneq	%rcx, %rax
	movl	$.str, %edi
	movq	%rax, %rsi
	xorl	%eax, %eax
	callq	printf
	movq	%rbx, %rax
	popq	%rbx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	Object_printBool, .Lfunc_end1-Object_printBool
	.cfi_endproc
                                        # -- End function
	.globl	Object_printInt32       # -- Begin function Object_printInt32
	.p2align	4, 0x90
	.type	Object_printInt32,@function
Object_printInt32:                      # @Object_printInt32
	.cfi_startproc
# %bb.0:
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset %rbx, -16
	movq	%rdi, %rbx
	movl	$.str.3, %edi
	xorl	%eax, %eax
	callq	printf
	movq	%rbx, %rax
	popq	%rbx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end2:
	.size	Object_printInt32, .Lfunc_end2-Object_printInt32
	.cfi_endproc
                                        # -- End function
	.globl	Object_inputLine        # -- Begin function Object_inputLine
	.p2align	4, 0x90
	.type	Object_inputLine,@function
Object_inputLine:                       # @Object_inputLine
	.cfi_startproc
# %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	$is_eol, %edi
	callq	read_until
	testq	%rax, %rax
	je	.LBB3_1
# %bb.2:
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.LBB3_1:
	.cfi_def_cfa_offset 16
	movl	$.str.4, %eax
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end3:
	.size	Object_inputLine, .Lfunc_end3-Object_inputLine
	.cfi_endproc
                                        # -- End function
	.globl	Object_inputBool        # -- Begin function Object_inputBool
	.p2align	4, 0x90
	.type	Object_inputBool,@function
Object_inputBool:                       # @Object_inputBool
	.cfi_startproc
# %bb.0:
	pushq	%r14
	.cfi_def_cfa_offset 16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	pushq	%rax
	.cfi_def_cfa_offset 32
	.cfi_offset %rbx, -24
	.cfi_offset %r14, -16
	movl	$isspace, %edi
	callq	skip_while
	movl	$isspace, %edi
	callq	read_until
	testq	%rax, %rax
	je	.LBB4_8
# %bb.1:
	movq	%rax, %r14
	movq	%rax, %rdi
	callq	strlen
	movq	%rax, %rbx
	cmpq	$4, %rax
	jne	.LBB4_4
# %bb.2:
	movl	$.str.1, %esi
	movl	$4, %edx
	movq	%r14, %rdi
	callq	strncmp
	testl	%eax, %eax
	je	.LBB4_3
.LBB4_4:
	cmpq	$5, %rbx
	jne	.LBB4_9
# %bb.5:
	movl	$.str.2, %esi
	movl	$5, %edx
	movq	%r14, %rdi
	callq	strncmp
	testl	%eax, %eax
	jne	.LBB4_9
# %bb.6:
	movq	%r14, %rdi
	callq	free
	xorl	%eax, %eax
.LBB4_7:
                                        # kill: def $al killed $al killed $eax
	addq	$8, %rsp
	.cfi_def_cfa_offset 24
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%r14
	.cfi_def_cfa_offset 8
	retq
.LBB4_3:
	.cfi_def_cfa_offset 32
	movq	%r14, %rdi
	callq	free
	movb	$1, %al
	jmp	.LBB4_7
.LBB4_9:
	movq	stderr(%rip), %rdi
	movl	$.str.6, %esi
	movq	%r14, %rdx
	xorl	%eax, %eax
	callq	fprintf
	movq	%r14, %rdi
	callq	free
	movl	$1, %edi
	callq	exit
.LBB4_8:
	movq	stderr(%rip), %rdi
	movl	$.str.5, %esi
	xorl	%eax, %eax
	callq	fprintf
	movl	$1, %edi
	callq	exit
.Lfunc_end4:
	.size	Object_inputBool, .Lfunc_end4-Object_inputBool
	.cfi_endproc
                                        # -- End function
	.globl	Object_inputInt32       # -- Begin function Object_inputInt32
	.p2align	4, 0x90
	.type	Object_inputInt32,@function
Object_inputInt32:                      # @Object_inputInt32
	.cfi_startproc
# %bb.0:
	pushq	%rbx
	.cfi_def_cfa_offset 16
	subq	$16, %rsp
	.cfi_def_cfa_offset 32
	.cfi_offset %rbx, -16
	movl	$isspace, %edi
	callq	skip_while
	movl	$isspace, %edi
	callq	read_until
	testq	%rax, %rax
	je	.LBB5_20
# %bb.1:
	movq	%rax, %rbx
	movq	%rax, %rdi
	callq	strlen
	cmpq	$3, %rax
	jb	.LBB5_4
# %bb.2:
	cmpb	$48, (%rbx)
	jne	.LBB5_4
# %bb.3:
	movb	$1, %cl
	cmpb	$120, 1(%rbx)
	je	.LBB5_12
.LBB5_4:
	cmpq	$4, %rax
	jb	.LBB5_11
# %bb.5:
	cmpb	$43, (%rbx)
	je	.LBB5_7
# %bb.6:
	cmpb	$45, (%rbx)
	jne	.LBB5_11
.LBB5_7:
	cmpb	$48, 1(%rbx)
	jne	.LBB5_11
# %bb.8:
	cmpb	$120, 2(%rbx)
	sete	%cl
	jmp	.LBB5_12
.LBB5_11:
	xorl	%ecx, %ecx
.LBB5_12:
	leaq	8(%rsp), %rsi
	movq	%rbx, %rdi
	testb	%cl, %cl
	je	.LBB5_14
# %bb.13:
	movl	$16, %edx
	jmp	.LBB5_15
.LBB5_14:
	movl	$10, %edx
.LBB5_15:
	callq	strtoll
	movq	8(%rsp), %rcx
	cmpb	$0, (%rcx)
	jne	.LBB5_21
# %bb.16:
	cmpq	$-2147483648, %rax      # imm = 0x80000000
	jl	.LBB5_19
# %bb.17:
	movl	$2147483648, %ecx       # imm = 0x80000000
	cmpq	%rcx, %rax
	jge	.LBB5_19
# %bb.18:
                                        # kill: def $eax killed $eax killed $rax
	addq	$16, %rsp
	.cfi_def_cfa_offset 16
	popq	%rbx
	.cfi_def_cfa_offset 8
	retq
.LBB5_19:
	.cfi_def_cfa_offset 32
	movq	stderr(%rip), %rdi
	movl	$.str.9, %esi
	jmp	.LBB5_22
.LBB5_20:
	movq	stderr(%rip), %rdi
	movl	$.str.7, %esi
	xorl	%eax, %eax
	callq	fprintf
	movl	$1, %edi
	callq	exit
.LBB5_21:
	movq	stderr(%rip), %rdi
	movl	$.str.8, %esi
.LBB5_22:
	movq	%rbx, %rdx
	xorl	%eax, %eax
	callq	fprintf
	movl	$1, %edi
	callq	exit
.Lfunc_end5:
	.size	Object_inputInt32, .Lfunc_end5-Object_inputInt32
	.cfi_endproc
                                        # -- End function
	.globl	Object_new              # -- Begin function Object_new
	.p2align	4, 0x90
	.type	Object_new,@function
Object_new:                             # @Object_new
	.cfi_startproc
# %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	$8, %edi
	callq	malloc
	movq	%rax, %rdi
	callq	Object_init
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end6:
	.size	Object_new, .Lfunc_end6-Object_new
	.cfi_endproc
                                        # -- End function
	.globl	Object_init             # -- Begin function Object_init
	.p2align	4, 0x90
	.type	Object_init,@function
Object_init:                            # @Object_init
	.cfi_startproc
# %bb.0:
	movq	%rdi, %rax
	testq	%rdi, %rdi
	je	.LBB7_2
# %bb.1:
	movq	$Object_vtable, (%rax)
.LBB7_2:
	retq
.Lfunc_end7:
	.size	Object_init, .Lfunc_end7-Object_init
	.cfi_endproc
                                        # -- End function
	.p2align	4, 0x90         # -- Begin function read_until
	.type	read_until,@function
read_until:                             # @read_until
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%r15
	.cfi_def_cfa_offset 24
	pushq	%r14
	.cfi_def_cfa_offset 32
	pushq	%r12
	.cfi_def_cfa_offset 40
	pushq	%rbx
	.cfi_def_cfa_offset 48
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movq	%rdi, %r14
	movl	$1024, %r15d            # imm = 0x400
	movl	$1024, %edi             # imm = 0x400
	callq	malloc
	movq	%rax, %r12
	xorl	%ebx, %ebx
	testq	%r12, %r12
	jne	.LBB8_3
	jmp	.LBB8_2
	.p2align	4, 0x90
.LBB8_11:                               #   in Loop: Header=BB8_3 Depth=1
	incq	%rbx
	testq	%r12, %r12
	je	.LBB8_2
.LBB8_3:                                # =>This Inner Loop Header: Depth=1
	movq	stdin(%rip), %rdi
	callq	getc
	movl	%eax, %ebp
	cmpl	$-1, %eax
	je	.LBB8_5
# %bb.4:                                #   in Loop: Header=BB8_3 Depth=1
	movsbl	%bpl, %edi
	callq	*%r14
	testl	%eax, %eax
	jne	.LBB8_5
# %bb.9:                                #   in Loop: Header=BB8_3 Depth=1
	movb	%bpl, (%r12,%rbx)
	leaq	-1(%r15), %rax
	cmpq	%rax, %rbx
	jne	.LBB8_11
# %bb.10:                               #   in Loop: Header=BB8_3 Depth=1
	addq	%r15, %r15
	movq	%r12, %rdi
	movq	%r15, %rsi
	callq	realloc
	movq	%rax, %r12
	jmp	.LBB8_11
.LBB8_5:
	cmpl	$-1, %ebp
	je	.LBB8_7
# %bb.6:
	movq	stdin(%rip), %rsi
	movl	%ebp, %edi
	callq	ungetc
.LBB8_7:
	movb	$0, (%r12,%rbx)
	jmp	.LBB8_8
.LBB8_2:
	xorl	%r12d, %r12d
.LBB8_8:
	movq	%r12, %rax
	popq	%rbx
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r14
	.cfi_def_cfa_offset 24
	popq	%r15
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end8:
	.size	read_until, .Lfunc_end8-read_until
	.cfi_endproc
                                        # -- End function
	.p2align	4, 0x90         # -- Begin function is_eol
	.type	is_eol,@function
is_eol:                                 # @is_eol
	.cfi_startproc
# %bb.0:
	xorl	%eax, %eax
	cmpl	$10, %edi
	sete	%al
	retq
.Lfunc_end9:
	.size	is_eol, .Lfunc_end9-is_eol
	.cfi_endproc
                                        # -- End function
	.p2align	4, 0x90         # -- Begin function skip_while
	.type	skip_while,@function
skip_while:                             # @skip_while
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	pushq	%rax
	.cfi_def_cfa_offset 32
	.cfi_offset %rbx, -24
	.cfi_offset %rbp, -16
	movq	%rdi, %rbx
	jmp	.LBB10_1
	.p2align	4, 0x90
.LBB10_3:                               #   in Loop: Header=BB10_1 Depth=1
	movl	%ebp, %edi
	callq	*%rbx
	testl	%eax, %eax
	setne	%al
	testb	%al, %al
	je	.LBB10_5
.LBB10_1:                               # =>This Inner Loop Header: Depth=1
	movq	stdin(%rip), %rdi
	callq	getc
	movl	%eax, %ebp
	cmpl	$-1, %eax
	jne	.LBB10_3
# %bb.2:                                #   in Loop: Header=BB10_1 Depth=1
	xorl	%eax, %eax
	testb	%al, %al
	jne	.LBB10_1
.LBB10_5:
	cmpl	$-1, %ebp
	je	.LBB10_7
# %bb.6:
	movq	stdin(%rip), %rsi
	movl	%ebp, %edi
	callq	ungetc
.LBB10_7:
	addq	$8, %rsp
	.cfi_def_cfa_offset 24
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end10:
	.size	skip_while, .Lfunc_end10-skip_while
	.cfi_endproc
                                        # -- End function
	.globl	D_new                   # -- Begin function D_new
	.p2align	4, 0x90
	.type	D_new,@function
D_new:                                  # @D_new
	.cfi_startproc
# %bb.0:                                # %.2
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	$16, %edi
	callq	malloc
	movq	%rax, %rdi
	callq	D_init
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end11:
	.size	D_new, .Lfunc_end11-D_new
	.cfi_endproc
                                        # -- End function
	.globl	D_init                  # -- Begin function D_init
	.p2align	4, 0x90
	.type	D_init,@function
D_init:                                 # @D_init
	.cfi_startproc
# %bb.0:                                # %.3
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movq	%rdi, %rbx
	testq	%rdi, %rdi
	je	.LBB12_2
# %bb.1:                                # %.3.if
	movq	%rbx, %rdi
	callq	Object_init
	movq	$D_vtable, (%rbx)
	movq	%rsp, %r14
	leaq	-16(%r14), %rsp
	callq	Object_new
	movq	%rax, -16(%r14)
	movq	(%rax), %rcx
	movl	$str0, %esi
	movq	%rax, %rdi
	callq	*(%rcx)
	movq	%rsp, %r14
	leaq	-16(%r14), %rsp
	callq	Object_new
	movq	%rax, -16(%r14)
	movq	(%rax), %rcx
	movl	$str1, %esi
	movq	%rax, %rdi
	callq	*(%rcx)
	movl	$1, 8(%rbx)
.LBB12_2:                               # %.3.endif
	movq	%rbx, %rax
	leaq	-16(%rbp), %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end12:
	.size	D_init, .Lfunc_end12-D_init
	.cfi_endproc
                                        # -- End function
	.globl	E_new                   # -- Begin function E_new
	.p2align	4, 0x90
	.type	E_new,@function
E_new:                                  # @E_new
	.cfi_startproc
# %bb.0:                                # %.2
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	$16, %edi
	callq	malloc
	movq	%rax, %rdi
	callq	E_init
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end13:
	.size	E_new, .Lfunc_end13-E_new
	.cfi_endproc
                                        # -- End function
	.globl	E_init                  # -- Begin function E_init
	.p2align	4, 0x90
	.type	E_init,@function
E_init:                                 # @E_init
	.cfi_startproc
# %bb.0:                                # %.3
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset %rbx, -16
	movq	%rdi, %rbx
	testq	%rdi, %rdi
	je	.LBB14_2
# %bb.1:                                # %.3.if
	movq	%rbx, %rdi
	callq	D_init
	movq	$E_vtable, (%rbx)
.LBB14_2:                               # %.3.endif
	movq	%rbx, %rax
	popq	%rbx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end14:
	.size	E_init, .Lfunc_end14-E_init
	.cfi_endproc
                                        # -- End function
	.globl	Main_new                # -- Begin function Main_new
	.p2align	4, 0x90
	.type	Main_new,@function
Main_new:                               # @Main_new
	.cfi_startproc
# %bb.0:                                # %.2
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	$8, %edi
	callq	malloc
	movq	%rax, %rdi
	callq	Main_init
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end15:
	.size	Main_new, .Lfunc_end15-Main_new
	.cfi_endproc
                                        # -- End function
	.globl	Main_init               # -- Begin function Main_init
	.p2align	4, 0x90
	.type	Main_init,@function
Main_init:                              # @Main_init
	.cfi_startproc
# %bb.0:                                # %.3
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset %rbx, -16
	movq	%rdi, %rbx
	testq	%rdi, %rdi
	je	.LBB16_2
# %bb.1:                                # %.3.if
	movq	%rbx, %rdi
	callq	Object_init
	movq	$Main_vtable, (%rbx)
.LBB16_2:                               # %.3.endif
	movq	%rbx, %rax
	popq	%rbx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end16:
	.size	Main_init, .Lfunc_end16-Main_init
	.cfi_endproc
                                        # -- End function
	.globl	D_method_f              # -- Begin function D_method_f
	.p2align	4, 0x90
	.type	D_method_f,@function
D_method_f:                             # @D_method_f
	.cfi_startproc
# %bb.0:                                # %.3
	pushq	%rax
	.cfi_def_cfa_offset 16
	movq	%rdi, (%rsp)
	movq	(%rdi), %rax
	callq	*56(%rax)
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end17:
	.size	D_method_f, .Lfunc_end17-D_method_f
	.cfi_endproc
                                        # -- End function
	.globl	D_method_g              # -- Begin function D_method_g
	.p2align	4, 0x90
	.type	D_method_g,@function
D_method_g:                             # @D_method_g
	.cfi_startproc
# %bb.0:                                # %.3
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movq	%rdi, 16(%rsp)
	callq	Object_new
	movq	%rax, 8(%rsp)
	movq	(%rax), %rcx
	movl	$str2, %esi
	movq	%rax, %rdi
	callq	*(%rcx)
	movl	$1, %eax
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end18:
	.size	D_method_g, .Lfunc_end18-D_method_g
	.cfi_endproc
                                        # -- End function
	.globl	E_method_g              # -- Begin function E_method_g
	.p2align	4, 0x90
	.type	E_method_g,@function
E_method_g:                             # @E_method_g
	.cfi_startproc
# %bb.0:                                # %.3
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movq	%rdi, 16(%rsp)
	callq	Object_new
	movq	%rax, 8(%rsp)
	movq	(%rax), %rcx
	movl	$str3, %esi
	movq	%rax, %rdi
	callq	*(%rcx)
	movl	$2, %eax
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end19:
	.size	E_method_g, .Lfunc_end19-E_method_g
	.cfi_endproc
                                        # -- End function
	.globl	main                    # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %.3
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%rbx
	subq	$24, %rsp
	.cfi_offset %rbx, -24
	movq	%rdi, -24(%rbp)
	movl	$0, -12(%rbp)
	cmpl	$10, -12(%rbp)
	jg	.LBB20_3
	.p2align	4, 0x90
.LBB20_2:                               # %loop
                                        # =>This Inner Loop Header: Depth=1
	movq	%rsp, %rbx
	leaq	-16(%rbx), %rsp
	callq	Object_new
	movq	%rax, -16(%rbx)
	movq	(%rax), %rcx
	movl	-12(%rbp), %esi
	movq	%rax, %rdi
	callq	*16(%rcx)
	incl	-12(%rbp)
	cmpl	$10, -12(%rbp)
	jle	.LBB20_2
.LBB20_3:                               # %after_loop
	movl	$1, %eax
	leaq	-8(%rbp), %rsp
	popq	%rbx
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end20:
	.size	main, .Lfunc_end20-main
	.cfi_endproc
                                        # -- End function
	.type	.str,@object            # @.str
	.section	.rodata,"a",@progbits
	.globl	.str
.str:
	.asciz	"%s"
	.size	.str, 3

	.type	.str.1,@object          # @.str.1
	.globl	.str.1
.str.1:
	.asciz	"true"
	.size	.str.1, 5

	.type	.str.2,@object          # @.str.2
	.globl	.str.2
.str.2:
	.asciz	"false"
	.size	.str.2, 6

	.type	.str.3,@object          # @.str.3
	.globl	.str.3
.str.3:
	.asciz	"%d"
	.size	.str.3, 3

	.type	.str.4,@object          # @.str.4
	.globl	.str.4
.str.4:
	.zero	1
	.size	.str.4, 1

	.type	.str.5,@object          # @.str.5
	.globl	.str.5
	.p2align	4
.str.5:
	.asciz	"Object::inputBool: cannot read word!\n"
	.size	.str.5, 38

	.type	.str.6,@object          # @.str.6
	.globl	.str.6
	.p2align	4
.str.6:
	.asciz	"Object::inputBool: `%s` is not a valid boolean!\n"
	.size	.str.6, 49

	.type	.str.7,@object          # @.str.7
	.globl	.str.7
	.p2align	4
.str.7:
	.asciz	"Object::inputInt32: cannot read word!\n"
	.size	.str.7, 39

	.type	.str.8,@object          # @.str.8
	.globl	.str.8
	.p2align	4
.str.8:
	.asciz	"Object::inputInt32: `%s` is not a valid integer literal!\n"
	.size	.str.8, 58

	.type	.str.9,@object          # @.str.9
	.globl	.str.9
	.p2align	4
.str.9:
	.asciz	"Object::inputInt32: `%s` does not fit a 32-bit integer!\n"
	.size	.str.9, 57

	.type	Object_vtable,@object   # @Object_vtable
	.globl	Object_vtable
	.p2align	4
Object_vtable:
	.quad	Object_print
	.quad	Object_printBool
	.quad	Object_printInt32
	.quad	Object_inputLine
	.quad	Object_inputBool
	.quad	Object_inputInt32
	.size	Object_vtable, 48

	.type	D_vtable,@object        # @D_vtable
	.globl	D_vtable
	.p2align	4
D_vtable:
	.quad	Object_print
	.quad	Object_printBool
	.quad	Object_printInt32
	.quad	Object_inputLine
	.quad	Object_inputBool
	.quad	Object_inputInt32
	.quad	D_method_f
	.quad	D_method_g
	.size	D_vtable, 64

	.type	E_vtable,@object        # @E_vtable
	.globl	E_vtable
	.p2align	4
E_vtable:
	.quad	Object_print
	.quad	Object_printBool
	.quad	Object_printInt32
	.quad	Object_inputLine
	.quad	Object_inputBool
	.quad	Object_inputInt32
	.quad	D_method_f
	.quad	E_method_g
	.size	E_vtable, 64

	.type	Main_vtable,@object     # @Main_vtable
	.globl	Main_vtable
	.p2align	4
Main_vtable:
	.quad	Object_print
	.quad	Object_printBool
	.quad	Object_printInt32
	.quad	Object_inputLine
	.quad	Object_inputBool
	.quad	Object_inputInt32
	.quad	main
	.size	Main_vtable, 56

	.type	str0,@object            # @str0
	.globl	str0
str0:
	.asciz	"s"
	.size	str0, 2

	.type	str1,@object            # @str1
	.globl	str1
str1:
	.asciz	"sa"
	.size	str1, 3

	.type	str2,@object            # @str2
	.globl	str2
str2:
	.asciz	"d"
	.size	str2, 2

	.type	str3,@object            # @str3
	.globl	str3
str3:
	.asciz	"e"
	.size	str3, 2


	.section	".note.GNU-stack","",@progbits
