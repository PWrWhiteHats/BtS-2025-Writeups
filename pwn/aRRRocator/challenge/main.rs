use core::slice;
use std::ptr;
use std::io::{self, Read, Write};

#[derive(Clone, Copy)]
struct Node {
    mem: *mut u8,
    idx: usize,
    depth: usize,
    next: Option<usize>,
    prev: Option<usize>,
    is_used: bool,
}

static mut TREE: [Node; 64] = [Node {
    mem: ptr::null_mut(),
    idx: 0,
    depth: 0,
    next: None,
    prev: None,
    is_used: false,
}; 64];

static mut FREE: [Option<usize>; 7] = [None; 7];

static mut MEM: [u8; 1024] = [0u8; 1024];

fn unlink(idx: usize) {
    unsafe {
        let depth = TREE[idx].depth;
        if FREE[depth] == Some(idx) {
            if TREE[idx].next.is_some() {
                FREE[depth] = TREE[idx].next;
            } else {
                FREE[depth] = TREE[idx].prev;
            }
        }
        if let Some(prev_idx) = TREE[idx].prev {
            TREE[prev_idx].next = TREE[idx].next;
        }
        if let Some(next_idx) = TREE[idx].next {
            TREE[next_idx].prev = TREE[idx].prev;
        }
    }
}

fn link(idx: usize) {
    unsafe {
        TREE[idx].is_used = false;
        let depth = TREE[idx].depth;
        if let Some(free_idx) = FREE[depth] {
            if let Some(prev) = TREE[free_idx].prev {
                TREE[prev].next = Some(idx);
                TREE[idx].prev = Some(prev);
            }
            TREE[free_idx].prev = Some(idx);
            TREE[idx].next = Some(free_idx);
        }
        FREE[depth] = Some(idx);
    }
}

fn alloc(size: usize) -> Option<&'static mut [u8]> {
    let size = size_align(size);
    let mut depth = size_to_depth(size);
    unsafe {
        while FREE[depth].is_none() && depth != 0 {
            depth -= 1;
        }
        if FREE[depth].is_none() {
            return None;
        }

        let mut idx = FREE[depth].unwrap();
        while TREE[idx].depth != size_to_depth(size) {
            // propagate
            unlink(idx);

            link(idx*2+1);
            link(idx*2);
            
            idx *= 2;
            depth += 1;
        }
        FREE[depth] = TREE[idx].next;
        TREE[idx].is_used = true;
        
        let ret = slice::from_raw_parts_mut(TREE[idx].mem, depth_to_size(depth));
        Some(ret)
    }
}

fn free(ptr: &mut [u8]) {
    let mut idx = ptr_to_idx(ptr);
    let mut depth = size_to_depth(ptr.len());
    unsafe {
        loop {
            TREE[idx].is_used = false;
            let l = idx;
            let r = idx ^ 1;
            if !TREE[l].is_used && !TREE[r].is_used {
                unlink(TREE[l].idx);
                unlink(TREE[r].idx);

                idx /= 2;
                depth -= 1;
                link(idx);
                if depth <= 1 {
                    break;
                }
            } else {
                link(idx);
                break;
            }
        }
    }
}

fn ptr_to_idx(ptr: &[u8]) -> usize {
    let depth = size_to_depth(ptr.len());
    let mut idx = 1;
    for _ in 0..(depth-1) {
        idx *= 2;
    }
    unsafe {
        let diff = ptr.as_ptr() as usize - MEM.as_ptr() as usize;
        let bucket = diff / ptr.len();
        idx+bucket
    }
}

fn idx_to_depth(mut idx: usize) -> usize {
    let mut depth = 0;
    while idx != 0 {
        depth += 1;
        idx /= 2;
    }

    depth
}

fn size_align(size: usize) -> usize {
    let mut new_size = 1;
    while new_size < size {
        new_size <<= 1;
    }
    if new_size < 32 {
        new_size = 32;
    }

    new_size
}

fn size_to_depth(size: usize) -> usize {
    let mut tmp_size: usize = 32;
    let mut depth: usize = 6;
    while tmp_size < size {
        depth -= 1;
        tmp_size <<= 1;
    }
    
    depth
}

fn depth_to_size(depth: usize) -> usize {
    let mut size = 32;
    if depth > 6 {
        return size;
    }
    for _ in 0..(6-depth) {
        size <<= 1;
    }

    size
}

fn init() {
    unsafe {
        for i in 0..TREE.len() {
            let depth = idx_to_depth(i);
            TREE[i].mem = MEM.as_mut_ptr();
            TREE[i].idx = i;
            TREE[i].depth = depth;
            TREE[i].next = None;
            TREE[i].prev = None;
            TREE[i].is_used = false;
        }
        
        FREE[1] = Some(1);
        init_mem(1, 1, MEM.as_mut_ptr());
    }
}

fn init_mem(idx: usize, depth: usize, addr: *mut u8) {
    if depth == 7 {
        return;
    }

    unsafe {
        TREE[idx].mem = addr;
        init_mem(idx*2, depth+1, addr);
        init_mem(idx*2+1, depth+1, addr.add(depth_to_size(depth+1)));
    }
}

fn menu() {
    println!("1. gimme flag");
    println!("2. teraz to już nie chce >:(");
}

fn get_flag() -> &'static mut [u8] {
    print!("Length: ");
    io::stdout().flush().unwrap();
    let mut line = String::new();
    io::stdin().read_line(&mut line).unwrap();
    let length = line.trim().parse().unwrap();

    let flag_mem = alloc(length).unwrap();

    print!("Write your own flag: ");
    io::stdout().flush().unwrap();
    let mut buffer = [0u8; 4096];
    let bytes_read = io::stdin().read(&mut buffer).unwrap();

    for i in 0..bytes_read {
        flag_mem[i] = buffer[i];
    }

    flag_mem
}

fn main() {
    init();
    
    println!("🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱");
    println!("🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱  FLAG  ALLOCATOR  🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱");
    println!("🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇯🇵🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱");
    println!("🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱  EVERYONE GETS A FLAG !!!  🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱");
    println!("🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱🇵🇱");
    println!("🇵🇱                                             🇵🇱");
    
    let mut flag = None;
    loop {
        println!("");
        menu();
        
        let mut line = String::new();
        io::stdin().read_line(&mut line).unwrap();
        let choice: i32 = line.trim().parse().unwrap();
        match choice {
            1 => {
                flag = Some(get_flag());
            },
            2 => {
                free(flag.as_mut().unwrap());
            },
            _ => {
                break;
            }
        }
    }
}
