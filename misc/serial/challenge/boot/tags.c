#include "../kernel/types.h"

typedef struct {
    uint16_t type;
    uint16_t flags;
    uint32_t size;
} multiboot2_tag_t;

typedef struct {
    uint16_t type;
    uint16_t flags;
    uint32_t size;
    uint64_t framebuffer_addr;
    uint32_t framebuffer_pitch;
    uint32_t framebuffer_width;
    uint32_t framebuffer_height;
    uint8_t framebuffer_bpp;
    uint8_t framebuffer_type;
    uint8_t reserved;
} framebuffer_tag_t;

typedef struct {
    uint32_t type;
    uint32_t size;
    uint32_t entry_size;
    uint32_t entry_version;
} mmap_tag_t;

typedef struct {
    uint64_t base_addr;
    uint64_t length;
    uint32_t type;
    uint32_t reserved;
} mmap_entry_t;
