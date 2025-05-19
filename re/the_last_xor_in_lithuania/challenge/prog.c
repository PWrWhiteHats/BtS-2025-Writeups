#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <immintrin.h>
#include <stddef.h>

__attribute__((noinline))
void decrypt_next(void *code, const size_t len, const unsigned char key)
{
    unsigned char *ptr = (unsigned char *)code;
    for (size_t i = 0; i < len; i++)
    {
        ptr[i] ^= key;
    }
}
extern char *__stop_f_47_section;
extern char *__start_f_47_section;
__attribute__((section("f_47_section ,\"awx\",@progbits#")))
static void final_function() {
    char message[] = "Congwatuwations, you reached the final function :3";
    puts(message);
    exit(EXIT_SUCCESS);
}

extern char* __stop_f_46_section;
extern char* __start_f_46_section;
__attribute__((section("f_46_section ,\"awx\",@progbits#"))) static void f_46(const char flag)
{

    ptrdiff_t length = (char*)(&__stop_f_47_section) - (char*)(&__start_f_47_section); 
	decrypt_next(final_function, (size_t)length, flag);
    final_function();
}

extern char* __stop_f_45_section;
extern char* __start_f_45_section;

__attribute__((section("f_45_section ,\"awx\",@progbits#"))) static void f_45(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_45_section) - (char*)(&__start_f_45_section); 
	decrypt_next(f_46, (size_t)length, flag);
}
__attribute__((naked, used, section("f_45_section ,\"awx\",@progbits#"))) static void _unused_f_45()
{
    asm(".string \"9gaTrxPtinSK7POIM52o2\" ");
    asm(".string \"Zaszczepkami i kołkiem zaszczepki przetknięto.\" ");
    asm(".string \"3OKt3\" ");
}

extern char* __stop_f_44_section;
extern char* __start_f_44_section;

__attribute__((section("f_44_section ,\"awx\",@progbits#"))) static void f_44(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_44_section) - (char*)(&__start_f_44_section); 
	decrypt_next(f_45, (size_t)length, flag);
}
__attribute__((naked, used, section("f_44_section ,\"awx\",@progbits#"))) static void _unused_f_44()
{
    asm(".string \"mbR1Ya\" ");
    asm(".string \"We dworze pusto: bo drzwi od ganku zamknięto\" ");
    asm(".string \"T6Cq9A7nV6II\" ");
}

extern char* __stop_f_43_section;
extern char* __start_f_43_section;

__attribute__((section("f_43_section ,\"awx\",@progbits#"))) static void f_43(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_43_section) - (char*)(&__start_f_43_section); 
	decrypt_next(f_44, (size_t)length, flag);
}
__attribute__((naked, used, section("f_43_section ,\"awx\",@progbits#"))) static void _unused_f_43()
{
    asm(".string \"E2VLJej1Z3qsPdEm\" ");
    asm(".string \"Szczypiąc trawę ciągnęły powoli pod bramę.\" ");
    asm(".string \"3aUHulV\" ");
}

extern char* __stop_f_42_section;
extern char* __start_f_42_section;

__attribute__((section("f_42_section ,\"awx\",@progbits#"))) static void f_42(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_42_section) - (char*)(&__start_f_42_section); 
	decrypt_next(f_43, (size_t)length, flag);
}
__attribute__((naked, used, section("f_42_section ,\"awx\",@progbits#"))) static void _unused_f_42()
{
    asm(".string \"k9HHK13dNSFOpzdXO\" ");
    asm(".string \"Wysiadł z powozu; konie porzucone same,\" ");
    asm(".string \"ZE94fnSck7gRTAVEem\" ");
}

extern char* __stop_f_41_section;
extern char* __start_f_41_section;

__attribute__((section("f_41_section ,\"awx\",@progbits#"))) static void f_41(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_41_section) - (char*)(&__start_f_41_section); 
	decrypt_next(f_42, (size_t)length, flag);
}
__attribute__((naked, used, section("f_41_section ,\"awx\",@progbits#"))) static void _unused_f_41()
{
    asm(".string \"5xSYzLqn\" ");
    asm(".string \"I obiegłszy dziedziniec zawrócił przed ganek.\" ");
    asm(".string \"SaGmNbauQp2RcAsIr\" ");
}

extern char* __stop_f_40_section;
extern char* __start_f_40_section;

__attribute__((section("f_40_section ,\"awx\",@progbits#"))) static void f_40(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_40_section) - (char*)(&__start_f_40_section); 
	decrypt_next(f_41, (size_t)length, flag);
}
__attribute__((naked, used, section("f_40_section ,\"awx\",@progbits#"))) static void _unused_f_40()
{
    asm(".string \"HMx8UjKfBvZqC2\" ");
    asm(".string \"Właśnie dwukonną bryką wjechał młody panek\" ");
    asm(".string \"T8NvDkttnelBGLifOwI\" ");
}

extern char* __stop_f_39_section;
extern char* __start_f_39_section;

__attribute__((section("f_39_section ,\"awx\",@progbits#"))) static void f_39(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_39_section) - (char*)(&__start_f_39_section); 
	decrypt_next(f_40, (size_t)length, flag);
}
__attribute__((naked, used, section("f_39_section ,\"awx\",@progbits#"))) static void _unused_f_39()
{
    asm(".string \"E4BS0RCXK7GUp2mvFP4n3LoI\" ");
    asm(".string \"Że gościnna, i wszystkich w gościnę zaprasza.\" ");
    asm(".string \"hHrOy\" ");
}

extern char* __stop_f_38_section;
extern char* __start_f_38_section;

__attribute__((section("f_38_section ,\"awx\",@progbits#"))) static void f_38(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_38_section) - (char*)(&__start_f_38_section); 
	decrypt_next(f_39, (size_t)length, flag);
}
__attribute__((naked, used, section("f_38_section ,\"awx\",@progbits#"))) static void _unused_f_38()
{
    asm(".string \"ymuMqSQPSthN\" ");
    asm(".string \"Brama na wciąż otwarta przechodniom ogłasza,\" ");
    asm(".string \"rgQo8HAdmXcnaUfJ8bZo5Z\" ");
}

extern char* __stop_f_37_section;
extern char* __start_f_37_section;

__attribute__((section("f_37_section ,\"awx\",@progbits#"))) static void f_37(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_37_section) - (char*)(&__start_f_37_section); 
	decrypt_next(f_38, (size_t)length, flag);
}
__attribute__((naked, used, section("f_37_section ,\"awx\",@progbits#"))) static void _unused_f_37()
{
    asm(".string \"iJ6X9wiloMJGeWfpeiO8\" ");
    asm(".string \"Że w tym domu dostatek mieszka i porządek.\" ");
    asm(".string \"dZbxntwFYj2YUV\" ");
}

extern char* __stop_f_36_section;
extern char* __start_f_36_section;

__attribute__((section("f_36_section ,\"awx\",@progbits#"))) static void f_36(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_36_section) - (char*)(&__start_f_36_section); 
	decrypt_next(f_37, (size_t)length, flag);
}
__attribute__((naked, used, section("f_36_section ,\"awx\",@progbits#"))) static void _unused_f_36()
{
    asm(".string \"LOjQrQtoep6\" ");
    asm(".string \"Uprawne dobrze na kształt ogrodowych grządek:\" ");
    asm(".string \"OEArjLNCfYE\" ");
}

extern char* __stop_f_35_section;
extern char* __start_f_35_section;

__attribute__((section("f_35_section ,\"awx\",@progbits#"))) static void f_35(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_35_section) - (char*)(&__start_f_35_section); 
	decrypt_next(f_36, (size_t)length, flag);
}
__attribute__((naked, used, section("f_35_section ,\"awx\",@progbits#"))) static void _unused_f_35()
{
    asm(".string \"ZA6yF5HHiNqmc61eMJCvuA\" ");
    asm(".string \"Czarnoziemne, zapewne należne do dworu,\" ");
    asm(".string \"JM43GCXULq5\" ");
}

extern char* __stop_f_34_section;
extern char* __start_f_34_section;

__attribute__((section("f_34_section ,\"awx\",@progbits#"))) static void f_34(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_34_section) - (char*)(&__start_f_34_section); 
	decrypt_next(f_35, (size_t)length, flag);
}
__attribute__((naked, used, section("f_34_section ,\"awx\",@progbits#"))) static void _unused_f_34()
{
    asm(".string \"JtJ3ZGiInljo6A137\" ");
    asm(".string \"Orzących wcześnie łany ogromne ugoru,\" ");
    asm(".string \"aHqz9Alv9\" ");
}

extern char* __stop_f_33_section;
extern char* __start_f_33_section;

__attribute__((section("f_33_section ,\"awx\",@progbits#"))) static void f_33(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_33_section) - (char*)(&__start_f_33_section); 
	decrypt_next(f_34, (size_t)length, flag);
}
__attribute__((naked, used, section("f_33_section ,\"awx\",@progbits#"))) static void _unused_f_33()
{
    asm(".string \"6OvagscppeNg9Z4\" ");
    asm(".string \"Świecą gęsto jak gwiazdy, widać z liczby pługów\" ");
    asm(".string \"YHWBWE0QFLVfTPpLE1P\" ");
}

extern char* __stop_f_32_section;
extern char* __start_f_32_section;

__attribute__((section("f_32_section ,\"awx\",@progbits#"))) static void f_32(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_32_section) - (char*)(&__start_f_32_section); 
	decrypt_next(f_33, (size_t)length, flag);
}
__attribute__((naked, used, section("f_32_section ,\"awx\",@progbits#"))) static void _unused_f_32()
{
    asm(".string \"krLRVKaRi92FPZ75D\" ");
    asm(".string \"I widać z liczby kopic, co wzdłuż i wszerz smugów\" ");
    asm(".string \"lbtdAnx0ew8QF5UArOBj\" ");
}

extern char* __stop_f_31_section;
extern char* __start_f_31_section;

__attribute__((section("f_31_section ,\"awx\",@progbits#"))) static void f_31(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_31_section) - (char*)(&__start_f_31_section); 
	decrypt_next(f_32, (size_t)length, flag);
}
__attribute__((naked, used, section("f_31_section ,\"awx\",@progbits#"))) static void _unused_f_31()
{
    asm(".string \"UQcqd2hWTn3Z5YWIbFcoLxC7\" ");
    asm(".string \"Widać, że okolica obfita we zboże,\" ");
    asm(".string \"hKFSYA0doRs4h3J\" ");
}

extern char* __stop_f_30_section;
extern char* __start_f_30_section;

__attribute__((section("f_30_section ,\"awx\",@progbits#"))) static void f_30(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_30_section) - (char*)(&__start_f_30_section); 
	decrypt_next(f_31, (size_t)length, flag);
}
__attribute__((naked, used, section("f_30_section ,\"awx\",@progbits#"))) static void _unused_f_30()
{
    asm(".string \"UgyDWZlk9s\" ");
    asm(".string \"Użątku, co pod strzechą zmieścić się nie może.\" ");
    asm(".string \"sjT6ofGkbtHY\" ");
}

extern char* __stop_f_29_section;
extern char* __start_f_29_section;

__attribute__((section("f_29_section ,\"awx\",@progbits#"))) static void f_29(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_29_section) - (char*)(&__start_f_29_section); 
	decrypt_next(f_30, (size_t)length, flag);
}
__attribute__((naked, used, section("f_29_section ,\"awx\",@progbits#"))) static void _unused_f_29()
{
    asm(".string \"SQQuqmQmFQhTRho\" ");
    asm(".string \"I stodołę miał wielką, i przy niej trzy stogi\" ");
    asm(".string \"Y2fXm5fBegDbUKqS4JfZD\" ");
}

extern char* __stop_f_28_section;
extern char* __start_f_28_section;

__attribute__((section("f_28_section ,\"awx\",@progbits#"))) static void f_28(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_28_section) - (char*)(&__start_f_28_section); 
	decrypt_next(f_29, (size_t)length, flag);
}
__attribute__((naked, used, section("f_28_section ,\"awx\",@progbits#"))) static void _unused_f_28()
{
    asm(".string \"x6eeWLSRt32bKA7H5YW0P\" ");
    asm(".string \"Dom mieszkalny niewielki, lecz zewsząd chędogi,\" ");
    asm(".string \"0MMAe4Gk1IATpjdzhBoRzNYF\" ");
}

extern char* __stop_f_27_section;
extern char* __start_f_27_section;

__attribute__((section("f_27_section ,\"awx\",@progbits#"))) static void f_27(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_27_section) - (char*)(&__start_f_27_section); 
	decrypt_next(f_28, (size_t)length, flag);
}
__attribute__((naked, used, section("f_27_section ,\"awx\",@progbits#"))) static void _unused_f_27()
{
    asm(".string \"5rB340dA\" ");
    asm(".string \"Topoli, co go bronią od wiatrów jesieni.\" ");
    asm(".string \"eM41BnuWU7nQl8yCOW2QL\" ");
}

extern char* __stop_f_26_section;
extern char* __start_f_26_section;

__attribute__((section("f_26_section ,\"awx\",@progbits#"))) static void f_26(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_26_section) - (char*)(&__start_f_26_section); 
	decrypt_next(f_27, (size_t)length, flag);
}
__attribute__((naked, used, section("f_26_section ,\"awx\",@progbits#"))) static void _unused_f_26()
{
    asm(".string \"2kPdWJ\" ");
    asm(".string \"Tym bielsze, że odbite od ciemnej zieleni\" ");
    asm(".string \"YOja8cGRkA\" ");
}

extern char* __stop_f_25_section;
extern char* __start_f_25_section;

__attribute__((section("f_25_section ,\"awx\",@progbits#"))) static void f_25(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_25_section) - (char*)(&__start_f_25_section); 
	decrypt_next(f_26, (size_t)length, flag);
}
__attribute__((naked, used, section("f_25_section ,\"awx\",@progbits#"))) static void _unused_f_25()
{
    asm(".string \"sisscwR1qooS44knQj\" ");
    asm(".string \"Świeciły się z daleka pobielane ściany,\" ");
    asm(".string \"2r3D\" ");
}

extern char* __stop_f_24_section;
extern char* __start_f_24_section;

__attribute__((section("f_24_section ,\"awx\",@progbits#"))) static void f_24(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_24_section) - (char*)(&__start_f_24_section); 
	decrypt_next(f_25, (size_t)length, flag);
}
__attribute__((naked, used, section("f_24_section ,\"awx\",@progbits#"))) static void _unused_f_24()
{
    asm(".string \"hqWkKtQpu7TvnvqI\" ");
    asm(".string \"Stał dwór szlachecki, z drzewa, lecz podmurowany;\" ");
    asm(".string \"cF3IXJKEXonBg3IzyNh7RtC\" ");
}

extern char* __stop_f_23_section;
extern char* __start_f_23_section;

__attribute__((section("f_23_section ,\"awx\",@progbits#"))) static void f_23(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_23_section) - (char*)(&__start_f_23_section); 
	decrypt_next(f_24, (size_t)length, flag);
}
__attribute__((naked, used, section("f_23_section ,\"awx\",@progbits#"))) static void _unused_f_23()
{
    asm(".string \"4mCN19JeN0EBbx7IpzLNHu5\" ");
    asm(".string \"Na pagórku niewielkim, we brzozowym gaju,\" ");
    asm(".string \"UFk2Mx\" ");
}

extern char* __stop_f_22_section;
extern char* __start_f_22_section;

__attribute__((section("f_22_section ,\"awx\",@progbits#"))) static void f_22(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_22_section) - (char*)(&__start_f_22_section); 
	decrypt_next(f_23, (size_t)length, flag);
}
__attribute__((naked, used, section("f_22_section ,\"awx\",@progbits#"))) static void _unused_f_22()
{
    asm(".string \"dobwz9RJXn4\" ");
    asm(".string \"Śród takich pól przed laty, nad brzegiem ruczaju,\" ");
    asm(".string \"o7rMg5SHfZlvo9QIsOKS\" ");
}

extern char* __stop_f_21_section;
extern char* __start_f_21_section;

__attribute__((section("f_21_section ,\"awx\",@progbits#"))) static void f_21(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_21_section) - (char*)(&__start_f_21_section); 
	decrypt_next(f_22, (size_t)length, flag);
}
__attribute__((naked, used, section("f_21_section ,\"awx\",@progbits#"))) static void _unused_f_21()
{
    asm(".string \"WJdEfr\" ");
    asm(".string \"Zieloną, na niej z rzadka ciche grusze siedzą.\" ");
    asm(".string \"r1da2Gc4gK\" ");
}

extern char* __stop_f_20_section;
extern char* __start_f_20_section;

__attribute__((section("f_20_section ,\"awx\",@progbits#"))) static void f_20(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_20_section) - (char*)(&__start_f_20_section); 
	decrypt_next(f_21, (size_t)length, flag);
}
__attribute__((naked, used, section("f_20_section ,\"awx\",@progbits#"))) static void _unused_f_20()
{
    asm(".string \"EN0YiK\" ");
    asm(".string \"A wszystko przepasane jakby wstęgą, miedzą\" ");
    asm(".string \"5V8ESgUxGnp\" ");
}

extern char* __stop_f_19_section;
extern char* __start_f_19_section;

__attribute__((section("f_19_section ,\"awx\",@progbits#"))) static void f_19(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_19_section) - (char*)(&__start_f_19_section); 
	decrypt_next(f_20, (size_t)length, flag);
}
__attribute__((naked, used, section("f_19_section ,\"awx\",@progbits#"))) static void _unused_f_19()
{
    asm(".string \"PBfDsTWJhYowQ5T76ZAkj\" ");
    asm(".string \"Gdzie panieńskim rumieńcem dzięcielina pała,\" ");
    asm(".string \"sSnvTrNV3oicCOZeOsFXXY\" ");
}

extern char* __stop_f_18_section;
extern char* __start_f_18_section;

__attribute__((section("f_18_section ,\"awx\",@progbits#"))) static void f_18(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_18_section) - (char*)(&__start_f_18_section); 
	decrypt_next(f_19, (size_t)length, flag);
}
__attribute__((naked, used, section("f_18_section ,\"awx\",@progbits#"))) static void _unused_f_18()
{
    asm(".string \"2E4HK\" ");
    asm(".string \"Gdzie bursztynowy świerzop, gryka jak śnieg biała,\" ");
    asm(".string \"cCzEL1NboksLb3rs\" ");
}

extern char* __stop_f_17_section;
extern char* __start_f_17_section;

__attribute__((section("f_17_section ,\"awx\",@progbits#"))) static void f_17(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_17_section) - (char*)(&__start_f_17_section); 
	decrypt_next(f_18, (size_t)length, flag);
}
__attribute__((naked, used, section("f_17_section ,\"awx\",@progbits#"))) static void _unused_f_17()
{
    asm(".string \"b05YpynzdZVpP37RBt6c\" ");
    asm(".string \"Wyzłacanych pszenicą, posrebrzanych żytem;\" ");
    asm(".string \"9DmrjTdkUpC4ipjM0G4fMXA3\" ");
}

extern char* __stop_f_16_section;
extern char* __start_f_16_section;

__attribute__((section("f_16_section ,\"awx\",@progbits#"))) static void f_16(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_16_section) - (char*)(&__start_f_16_section); 
	decrypt_next(f_17, (size_t)length, flag);
}
__attribute__((naked, used, section("f_16_section ,\"awx\",@progbits#"))) static void _unused_f_16()
{
    asm(".string \"TjAxc4Mqwcgw8QDhLk\" ");
    asm(".string \"Do tych pól malowanych zbożem rozmaitem,\" ");
    asm(".string \"urNRrauFyion\" ");
}

extern char* __stop_f_15_section;
extern char* __start_f_15_section;

__attribute__((section("f_15_section ,\"awx\",@progbits#"))) static void f_15(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_15_section) - (char*)(&__start_f_15_section); 
	decrypt_next(f_16, (size_t)length, flag);
}
__attribute__((naked, used, section("f_15_section ,\"awx\",@progbits#"))) static void _unused_f_15()
{
    asm(".string \"sg9Zqnq1e00MZiggPhR9X\" ");
    asm(".string \"Szeroko nad błękitnym Niemnem rozciągnionych;\" ");
    asm(".string \"OotST\" ");
}

extern char* __stop_f_14_section;
extern char* __start_f_14_section;

__attribute__((section("f_14_section ,\"awx\",@progbits#"))) static void f_14(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_14_section) - (char*)(&__start_f_14_section); 
	decrypt_next(f_15, (size_t)length, flag);
}
__attribute__((naked, used, section("f_14_section ,\"awx\",@progbits#"))) static void _unused_f_14()
{
    asm(".string \"mU6SJZ\" ");
    asm(".string \"Do tych pagórków leśnych, do tych łąk zielonych,\" ");
    asm(".string \"3uWPzgPYtpx4\" ");
}

extern char* __stop_f_13_section;
extern char* __start_f_13_section;

__attribute__((section("f_13_section ,\"awx\",@progbits#"))) static void f_13(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_13_section) - (char*)(&__start_f_13_section); 
	decrypt_next(f_14, (size_t)length, flag);
}
__attribute__((naked, used, section("f_13_section ,\"awx\",@progbits#"))) static void _unused_f_13()
{
    asm(".string \"jLtUb\" ");
    asm(".string \"Tymczasem przenoś moją duszę utęsknioną\" ");
    asm(".string \"qvy3obTz7vzJR1mDVXbCZVY\" ");
}

extern char* __stop_f_12_section;
extern char* __start_f_12_section;

__attribute__((section("f_12_section ,\"awx\",@progbits#"))) static void f_12(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_12_section) - (char*)(&__start_f_12_section); 
	decrypt_next(f_13, (size_t)length, flag);
}
__attribute__((naked, used, section("f_12_section ,\"awx\",@progbits#"))) static void _unused_f_12()
{
    asm(".string \"kCg1FV8vJ331gT57SoWxSX1p\" ");
    asm(".string \"Tak nas powrócisz cudem na Ojczyzny łono.\" ");
    asm(".string \"8jBIfqK\" ");
}

extern char* __stop_f_11_section;
extern char* __start_f_11_section;

__attribute__((section("f_11_section ,\"awx\",@progbits#"))) static void f_11(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_11_section) - (char*)(&__start_f_11_section); 
	decrypt_next(f_12, (size_t)length, flag);
}
__attribute__((naked, used, section("f_11_section ,\"awx\",@progbits#"))) static void _unused_f_11()
{
    asm(".string \"OpJF1UynaTi7KZvJg1JNh\" ");
    asm(".string \"Iść za wrócone życie podziękować Bogu),\" ");
    asm(".string \"QwWznXuRrGx3HHupqjaHA\" ");
}

extern char* __stop_f_10_section;
extern char* __start_f_10_section;

__attribute__((section("f_10_section ,\"awx\",@progbits#"))) static void f_10(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_10_section) - (char*)(&__start_f_10_section); 
	decrypt_next(f_11, (size_t)length, flag);
}
__attribute__((naked, used, section("f_10_section ,\"awx\",@progbits#"))) static void _unused_f_10()
{
    asm(".string \"4P1ot0nMJyBN0dGkR\" ");
    asm(".string \"I zaraz mogłem pieszo, do Twych świątyń progu\" ");
    asm(".string \"VEJG6zM\" ");
}

extern char* __stop_f_9_section;
extern char* __start_f_9_section;

__attribute__((section("f_9_section ,\"awx\",@progbits#"))) static void f_9(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_9_section) - (char*)(&__start_f_9_section); 
	decrypt_next(f_10, (size_t)length, flag);
}
__attribute__((naked, used, section("f_9_section ,\"awx\",@progbits#"))) static void _unused_f_9()
{
    asm(".string \"N1tjurQWcZClkW2Sag8ASLJ\" ");
    asm(".string \"Ofiarowany, martwą podniosłem powiekę;\" ");
    asm(".string \"MiT8DGoohui06p5xP\" ");
}

extern char* __stop_f_8_section;
extern char* __start_f_8_section;

__attribute__((section("f_8_section ,\"awx\",@progbits#"))) static void f_8(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_8_section) - (char*)(&__start_f_8_section); 
	decrypt_next(f_9, (size_t)length, flag);
}
__attribute__((naked, used, section("f_8_section ,\"awx\",@progbits#"))) static void _unused_f_8()
{
    asm(".string \"RASepLC70Je0dcQMEyWW\" ");
    asm(".string \"(Gdy od płaczącej matki, pod Twoją opiekę\" ");
    asm(".string \"LFT8e\" ");
}

extern char* __stop_f_7_section;
extern char* __start_f_7_section;

__attribute__((section("f_7_section ,\"awx\",@progbits#"))) static void f_7(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_7_section) - (char*)(&__start_f_7_section); 
	decrypt_next(f_8, (size_t)length, flag);
}
__attribute__((naked, used, section("f_7_section ,\"awx\",@progbits#"))) static void _unused_f_7()
{
    asm(".string \"3HddQ\" ");
    asm(".string \"Jak mnie dziecko do zdrowia powróciłaś cudem\" ");
    asm(".string \"CcI1wn2gv\" ");
}

extern char* __stop_f_6_section;
extern char* __start_f_6_section;

__attribute__((section("f_6_section ,\"awx\",@progbits#"))) static void f_6(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_6_section) - (char*)(&__start_f_6_section); 
	decrypt_next(f_7, (size_t)length, flag);
}
__attribute__((naked, used, section("f_6_section ,\"awx\",@progbits#"))) static void _unused_f_6()
{
    asm(".string \"VK6B4agKAWyMgcVG\" ");
    asm(".string \"Nowogródzki ochraniasz z jego wiernym ludem!\" ");
    asm(".string \"GPjqWHUuohCXn\" ");
}

extern char* __stop_f_5_section;
extern char* __start_f_5_section;

__attribute__((section("f_5_section ,\"awx\",@progbits#"))) static void f_5(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_5_section) - (char*)(&__start_f_5_section); 
	decrypt_next(f_6, (size_t)length, flag);
}
__attribute__((naked, used, section("f_5_section ,\"awx\",@progbits#"))) static void _unused_f_5()
{
    asm(".string \"kF907\" ");
    asm(".string \"I w Ostrej świecisz Bramie! Ty, co gród zamkowy\" ");
    asm(".string \"5VDDxftvgZ\" ");
}

extern char* __stop_f_4_section;
extern char* __start_f_4_section;

__attribute__((section("f_4_section ,\"awx\",@progbits#"))) static void f_4(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_4_section) - (char*)(&__start_f_4_section); 
	decrypt_next(f_5, (size_t)length, flag);
}
__attribute__((naked, used, section("f_4_section ,\"awx\",@progbits#"))) static void _unused_f_4()
{
    asm(".string \"Vbh5kOb7aSjiL9Hm\" ");
    asm(".string \"Panno święta, co Jasnej bronisz Częstochowy\" ");
    asm(".string \"TpdN7ftmRkI0HW9AK6\" ");
}

extern char* __stop_f_3_section;
extern char* __start_f_3_section;

__attribute__((section("f_3_section ,\"awx\",@progbits#"))) static void f_3(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_3_section) - (char*)(&__start_f_3_section); 
	decrypt_next(f_4, (size_t)length, flag);
}
__attribute__((naked, used, section("f_3_section ,\"awx\",@progbits#"))) static void _unused_f_3()
{
    asm(".string \"9xEQlJ5V\" ");
    asm(".string \"Widzę i opisuję, bo tęsknię po tobie.\" ");
    asm(".string \"o3OwkQ1LxIADAkzSM3R\" ");
}

extern char* __stop_f_2_section;
extern char* __start_f_2_section;

__attribute__((section("f_2_section ,\"awx\",@progbits#"))) static void f_2(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_2_section) - (char*)(&__start_f_2_section); 
	decrypt_next(f_3, (size_t)length, flag);
}
__attribute__((naked, used, section("f_2_section ,\"awx\",@progbits#"))) static void _unused_f_2()
{
    asm(".string \"ntW3j7qDVPDKKYSEB3eaoN\" ");
    asm(".string \"Kto cię stracił. Dziś piękność twą w całej ozdobie\" ");
    asm(".string \"o4I8vXphgYje0Oz\" ");
}

extern char* __stop_f_1_section;
extern char* __start_f_1_section;

__attribute__((section("f_1_section ,\"awx\",@progbits#"))) static void f_1(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_1_section) - (char*)(&__start_f_1_section); 
	decrypt_next(f_2, (size_t)length, flag);
}
__attribute__((naked, used, section("f_1_section ,\"awx\",@progbits#"))) static void _unused_f_1()
{
    asm(".string \"zzIsJErl5DthNa\" ");
    asm(".string \"Ile cię trzeba cenić, ten tylko się dowie,\" ");
    asm(".string \"oLXAIZ9SKWdDKv04mw4\" ");
}

extern char* __stop_f_0_section;
extern char* __start_f_0_section;

__attribute__((section("f_0_section ,\"awx\",@progbits#"))) static void f_0(const char flag)
{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_f_0_section) - (char*)(&__start_f_0_section); 
	decrypt_next(f_1, (size_t)length, flag);
}
__attribute__((naked, used, section("f_0_section ,\"awx\",@progbits#"))) static void _unused_f_0()
{
    asm(".string \"Q9XM1tSj1dfQNKFviYpLH\" ");
    asm(".string \"Litwo! Ojczyzno moja! ty jesteś jak zdrowie:\" ");
    asm(".string \"HYbLWyuJQo\" ");
}

typedef void (*func_ptr_t)(char);

typedef func_ptr_t func_ptr_array_t[];

static const func_ptr_array_t program = {f_0,f_1,f_2,f_3,f_4,f_5,f_6,f_7,f_8,f_9,f_10,f_11,f_12,f_13,f_14,f_15,f_16,f_17,f_18,f_19,f_20,f_21,f_22,f_23,f_24,f_25,f_26,f_27,f_28,f_29,f_30,f_31,f_32,f_33,f_34,f_35,f_36,f_37,f_38,f_39,f_40,f_41,f_42,f_43,f_44,f_45,f_46};
__attribute__((noinline))
static void runner(char * flag){
    const func_ptr_t *program_ip = program;
    const func_ptr_t *program_end = program + sizeof(program);
    size_t length = (char*)(&__stop_f_0_section) - (char*)(&__start_f_0_section); 
    decrypt_next(f_0, length, *flag++);
    for(; program != program_end; ++program_ip, ++flag)
        (*program_ip)(*flag);
}

int main(int, char *argv[])
{{
    runner(argv[1]);
    return EXIT_SUCCESS;
}}
