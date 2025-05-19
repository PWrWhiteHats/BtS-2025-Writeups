ENTRY(start)

SECTIONS {
    . = 0x100000;

    .boot :
    {
        *(.multiboot_header)
    }

    .text : {
	    section_start_text = .;
        *(.text)
        section_end_text = .;
    }

    .rodata ALIGN (0x1000) : {
        section_start_rodata = .;
        *(.rodata)
        section_end_rodata = .;
    }

    .data ALIGN (0x1000) : {
        section_start_data = .;
        *(.data)
        section_end_data = .;
    }

    .bss : {
        section_start_bss = .;
        *(COMMON)
        *(.bss)
        section_end_bss = .;
    }

    section_end = .;
}
