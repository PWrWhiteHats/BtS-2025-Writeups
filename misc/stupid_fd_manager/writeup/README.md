# Write-up

the solve was about abusing two facts:
- stdio in libc is buffered.
- Opening a file opens the file in the lowest possible file descriptor.

So the solve to write in one line `3 0 2 ./flag`.
The program buffers the whole line -> it closes file descriptor 0 (which is standard input) ->
it opens ./flag as file descriptor 0 -> scanf() and family now will do io operations
on the flag instead of standard input, which shows us the flag.
