from random import shuffle
from pathlib import Path
from pwn import ELF, xor
import subprocess
import random, string


def randword():
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(random.randint(4, 24)))


PAN_TADEUSZ = [
    "Litwo! Ojczyzno moja! ty jesteś jak zdrowie:",
    "Ile cię trzeba cenić, ten tylko się dowie,",
    "Kto cię stracił. Dziś piękność twą w całej ozdobie",
    "Widzę i opisuję, bo tęsknię po tobie.",
    "Panno święta, co Jasnej bronisz Częstochowy",
    "I w Ostrej świecisz Bramie! Ty, co gród zamkowy",
    "Nowogródzki ochraniasz z jego wiernym ludem!",
    "Jak mnie dziecko do zdrowia powróciłaś cudem",
    "(Gdy od płaczącej matki, pod Twoją opiekę",
    "Ofiarowany, martwą podniosłem powiekę;",
    "I zaraz mogłem pieszo, do Twych świątyń progu",
    "Iść za wrócone życie podziękować Bogu),",
    "Tak nas powrócisz cudem na Ojczyzny łono.",
    "Tymczasem przenoś moją duszę utęsknioną",
    "Do tych pagórków leśnych, do tych łąk zielonych,",
    "Szeroko nad błękitnym Niemnem rozciągnionych;",
    "Do tych pól malowanych zbożem rozmaitem,",
    "Wyzłacanych pszenicą, posrebrzanych żytem;",
    "Gdzie bursztynowy świerzop, gryka jak śnieg biała,",
    "Gdzie panieńskim rumieńcem dzięcielina pała,",
    "A wszystko przepasane jakby wstęgą, miedzą",
    "Zieloną, na niej z rzadka ciche grusze siedzą.",
    "Śród takich pól przed laty, nad brzegiem ruczaju,",
    "Na pagórku niewielkim, we brzozowym gaju,",
    "Stał dwór szlachecki, z drzewa, lecz podmurowany;",
    "Świeciły się z daleka pobielane ściany,",
    "Tym bielsze, że odbite od ciemnej zieleni",
    "Topoli, co go bronią od wiatrów jesieni.",
    "Dom mieszkalny niewielki, lecz zewsząd chędogi,",
    "I stodołę miał wielką, i przy niej trzy stogi",
    "Użątku, co pod strzechą zmieścić się nie może.",
    "Widać, że okolica obfita we zboże,",
    "I widać z liczby kopic, co wzdłuż i wszerz smugów",
    "Świecą gęsto jak gwiazdy, widać z liczby pługów",
    "Orzących wcześnie łany ogromne ugoru,",
    "Czarnoziemne, zapewne należne do dworu,",
    "Uprawne dobrze na kształt ogrodowych grządek:",
    "Że w tym domu dostatek mieszka i porządek.",
    "Brama na wciąż otwarta przechodniom ogłasza,",
    "Że gościnna, i wszystkich w gościnę zaprasza.",
    "Właśnie dwukonną bryką wjechał młody panek",
    "I obiegłszy dziedziniec zawrócił przed ganek.",
    "Wysiadł z powozu; konie porzucone same,",
    "Szczypiąc trawę ciągnęły powoli pod bramę.",
    "We dworze pusto: bo drzwi od ganku zamknięto",
    "Zaszczepkami i kołkiem zaszczepki przetknięto.",
    "Podróżny do folwarku nie biegł sług zapytać,",
    "Odemknął, wbiegł do domu, pragnął go powitać.",
    "Dawno domu nie widział, bo w dalekim mieście",
    "Kończył nauki, końca doczekał nareszcie.",
    "Wbiega i okiem chciwie ściany starodawne",
    "Ogląda czule, jako swe znajome dawne.",
    "Też same widzi sprzęty, też same obicia,",
    "Z którymi się zabawiać lubił od powicia,",
    "Lecz mniej wielkie, mniej piękne niż się dawniej zdały.",
    "I też same portrety na ścianach wisiały:",
    "Tu Kościuszko w czamarce krakowskiej, z oczyma",
    "Podniesionymi w niebo, miecz oburącz trzyma;",
    "Takim był, gdy przysięgał na stopniach ołtarzów,",
    "Że tym mieczem wypędzi z Polski trzech mocarzów,",
    "Albo sam na nim padnie. Dalej w polskiej szacie",
    "Siedzi Rejtan, żałośny po wolności stracie;",
    "W ręku trzyma nóż ostrzem zwrócony do łona,",
    "A przed nim leży Fedon i żywot Katona.",
    "Dalej Jasiński, młodzian piękny i posępny;",
    "Obok Korsak, towarzysz jego nieodstępny:",
    "Stoją na szańcach Pragi, na stosach Moskali,",
    "Siekąc wrogów, a Praga już się wkoło pali.",
    "Nawet stary stojący zegar kurantowy",
    "W drewnianej szafie poznał, u wniścia alkowy;",
    "I z dziecinną radością pociągnął za sznurek,",
    "By stary Dąbrowskiego usłyszeć mazurek.",
]

FILE_BEGIN = """#include <stdio.h>
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
}"""

RUNNER_TEMPLATE = """
typedef void (*func_ptr_t)(char);

typedef func_ptr_t func_ptr_array_t[];

static const func_ptr_array_t program = {names};
__attribute__((noinline))
static void runner(char * flag){{
    const func_ptr_t *program_ip = program;
    const func_ptr_t *program_end = program + sizeof(program);
    size_t length = (char*)(&__stop_{first_function_name}_section) - (char*)(&__start_{first_function_name}_section); 
    decrypt_next({first_function_name}, length, *flag++);
    for(; program != program_end; ++program_ip, ++flag)
        (*program_ip)(*flag);
}}
"""

FUNCTION_TEMPLATE = """
extern char* __stop_{function_name}_section;
extern char* __start_{function_name}_section;

__attribute__((section("{function_name}_section ,\\\"awx\\\",@progbits#"))) static void {function_name}(const char flag)
{{
    uint32_t loop;
    _rdrand32_step(&loop);
    loop %= 1024;
    while(loop-->0);
    ptrdiff_t length = (char*)(&__stop_{function_name}_section) - (char*)(&__start_{function_name}_section); 
	decrypt_next({next_function_name}, (size_t)length, flag);
}}
__attribute__((naked, used, section("{function_name}_section ,\\\"awx\\\",@progbits#"))) static void _unused_{function_name}()
{{
    asm(\".string \\\"{junk1}\\\" \");
    asm(\".string \\\"{line}\\\" \");
    asm(\".string \\\"{junk2}\\\" \");
}}
"""
END_FUNCTION = """
extern char *__stop_{final}_section;
extern char *__start_{final}_section;
__attribute__((section("{final}_section ,\\\"awx\\\",@progbits#")))
static void final_function() {{
    char message[] = "Congwatuwations, you reached the final function :3";
    puts(message);
    exit(EXIT_SUCCESS);
}}

extern char* __stop_{function_name}_section;
extern char* __start_{function_name}_section;
__attribute__((section("{function_name}_section ,\\\"awx\\\",@progbits#"))) static void {function_name}(const char flag)
{{

    ptrdiff_t length = (char*)(&__stop_{final}_section) - (char*)(&__start_{final}_section); 
	decrypt_next(final_function, (size_t)length, flag);
    final_function();
}}
"""

MAIN = """
int main(int, char *argv[])
{{
    runner(argv[1]);
    return EXIT_SUCCESS;
}}
"""


def gen_program(flag, source_file):
    functions = [
        FUNCTION_TEMPLATE.format(
            function_name=f"f_{name}",
            next_function_name=f"f_{name+1}",
            line=f"{PAN_TADEUSZ[name]}",
            junk1=randword(),
            junk2=randword(),
        )
        for name in range(len(flag) - 2)
    ]

    functions.append(
        END_FUNCTION.format(
            function_name=f"f_{len(flag) - 2}", final=f"f_{len(flag) - 1}"
        ),
    )

    runner = RUNNER_TEMPLATE.format(
        names="{" + ",".join(f"f_{n}" for n in range(len(flag) - 1)) + "}",
        first_function_name="f_0",
    )

    program = "".join(FILE_BEGIN)
    program += "".join(reversed(functions))
    program += "".join(runner)
    program += "".join(MAIN)
    Path(source_file).write_text(program)


def compile(source_file):
    subprocess.run(["gcc", "-fPIC", "-pie", "-mrdrnd", source_file], check=True)


def encrypt(flag):
    elf = ELF("a.out")
    data = Path("a.out").read_bytes()
    l_start = len(data)
    for i, char in enumerate(flag):
        s = elf.get_section_by_name(f"f_{i}_section")
        enc = xor(s.data(), char)
        data = data.replace(s.data(), enc)
        assert enc in data

    assert l_start == Path("a.out").write_bytes(data)


def strip(sects):
    subprocess.run(["strip", "a.out"], check=True)
    names = [f"f_{i}_section" for i in range(sects)]
    names_shuffled = names.copy()
    shuffle(names_shuffled)

    args = []
    for name, shuffled in zip(names, names_shuffled):
        args.extend([f"--rename-section", f"{name}={shuffled}"])

    subprocess.run(["objcopy", *args, "a.out"], check=True)


source_file = "prog.c"
flag = r"BtSCTF{D3CRYPT1NG_P4N_T4D3USZ_ON3_X0R_4T_4_T1M3}"
gen_program(flag, source_file)
compile(source_file)
encrypt(flag)
strip(len(flag))
