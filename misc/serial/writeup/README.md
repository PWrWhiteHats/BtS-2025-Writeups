## `misc/serial`

We found a serial connection on a weird embedded device. The device is running a custom firmware that we don't have the source code for. The firmware is a bit weird, and it doesn't seem to be doing anything useful. 

```bash
./sc -bind 4000 serial-dd3e5159cca716e4.chal.bts.wh.edu.pl
nc localhost 4000
```

I wrote a small operating system for x86_64 which has a single feature - toggleable PIC controller. The moment user logs in via netcat,
the system is seemingly sending nothing.

## Solution

Let's first connect to the challenge.

```bash
[rafisto@kitty ~]$ ./sc -bind 4000 serial-dd3e5159cca716e4.chal.bts.wh.edu.pl
[rafisto@kitty ~]$ nc localhost 4000

>>== 华威超级开关 Huei-wei NetworkSWE v1.00 ==<<
>>== 由华威网络安全实验室开发help ==<<
<观点view>
```

We can see some weird characters and a shell of what seems to be a network ethernet switch. Let's try to use help

```bash
<观点view>help
当前IP地址:10.0.0.10
☕️ 抱歉，这台机子只喝电，不喝咖啡。
欢迎使用 华威超级开关 Huei-wei NetworkSWE v1.00
>> 可用命令:
 - flag : 获取系统状态
 - help : 显示用户手册
 - ip : 显示当前IP地址
 - ping : 测试网络连接
```

We received a coffee and a few commands, including `flag`, let's try all of them:

```bash
<观点view>flag
当前IP地址:10.0.0.10
☕️ 抱歉，这台机子只喝电，不喝咖啡。
galf a ton si siht
```

This is nothing special, as well as the `ip` command, and the `ping` command.
What we know now is that the system has a barely usable CLI. 

There must be something else, something clever. Maybe what we see on the screen is not exactly what is sent by the switch.

```bash
nc localhost 4000 > file
<观点view>help 
<观点view>please
<观点view>flag
```

Then run to check for weird traffic.

```bash
xxd file
```

```bash
000001d0: e380 820a 6761 6c66 2061 2074 6f6e 2073  ....galf a ton s
000001e0: 6920 7369 6874 0a0a 3ce8 a782 e782 b976  i siht..<......v
000001f0: 6965 773e 0101                           iew>..
```

The `0x01` bytes are not normally visible in the CLI, but are sent by the switch.
Apparently the longer we keep the stream the more `0x01` bytes we are able to see

```bash
00000000: 0101 0101 0101                           ......
```

Let's run it interactively using `watch -n 0.1 xxd file`. But wait, now we see that these bytes are not arriving evenly, which may signal some encoding. Let's write a script to analyze the delays between the consecutive characters.

```py
import socket
import time

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4000
    CHAR = 0x1

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")
        
        prev_time = time.time()
        
        chars = []

        while True:
            data = s.recv(1)

            for byte in data:
                timestamp = time.time()
                relative_time = timestamp - prev_time
                prev_time = timestamp
                    
                print(f"Timer {relative_time:.2f} seconds", flush=True)
```

The output of which is

```py
Connected to localhost:4000
Timer 2.69 seconds
Timer 2.69 seconds
Timer 2.69 seconds
Timer 0.60 seconds
Timer 0.60 seconds
Timer 1.37 seconds
...
```

There are 3 different timings which stand out: 2.69, 0.6, 1.37 seconds (may depend on the latency, on our infra it was about 4.00, 2.00, 1.00) There are various encodings possible here, let's check the Morse for dots, dashes and spaces.

```py
import socket
import time

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4000
    CHAR = 0x1

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")
        
        prev_time = time.time()
        
        chars = []

        while True:
            data = s.recv(1)

            for byte in data:
                timestamp = time.time()
                relative_time = timestamp - prev_time
                prev_time = timestamp

                if relative_time < 0.8:
                    morse_char = "."
                elif relative_time < 1.6:
                    morse_char = "-"
                else:
                    morse_char = " "

                chars.append(morse_char)
                    
                # print(f"Timer {relative_time:.2f} seconds, char: {morse_char}", flush=True)
                print(f"message: {''.join(chars)}")
```

We will eventually see the following output of the script:

```
.-.. .--- ..- ... -   -.. --- -. -   ..- ... .   - .... .   -.. .. ... .- -... .-.. ...-- .--. .. -.-.   -.-. --- -- -- .- -. -.. .--- ..- ... -   -.. --- -. -   ..- ... .   - .... .   -.. .. ..
```

Let's decode it using https://morsecodetranslator.com/

```plaintext
LJUSTDONTUSETHEDISABL3PICCOMMANDJUSTDONTUSETHEDII
... JUST DONT USE THE DISABL3PIC COMMAND JUST DONT USE THE DI...
```

The message is a warning not to use the `DISABL3PIC` command. Let's use it.
Can be either uppercase or lowercase.

```bash
<观点view>DISABL3PIC
当前IP地址:10.0.0.10
☕️ 抱歉，这台机子只喝电，不喝咖啡。

<观点view>disabl3pic
!!! 警告: PIC锁定已关闭
<观点view> 控制台管理员模式已开启... 输入 'help' 获取帮助
```

The lowercase version did the trick; let's now seek `help`.

```bash
<观点view>help
当前IP地址:10.0.0.10
☕️ 抱歉，这台机子只喝电，不喝咖啡。
>> 管理员模式命令:
 - disabl3pic : 关闭保护模式 PIC
 - enabl3pic : 返回安全状态
 - help : 获取命令帮助
 - dumpmem : 内存分析工具
 - peekmem <a> : 查看内存地址 <a>
```

Let's try to dump the memory.

```bash
观点view>dumpmem 
当前IP地址:10.0.0.10
☕️ 抱歉，这台机子只喝电，不喝咖啡。
>>== 内存扫描器 MEMORY SCANNER ==<<
 - @代码段 text: 0x00100030
 - @数据段 data: 0x00102000
 - @未初始化数据段 bss: 0x00102040
```

The memory dump is not very useful, but we can see the text section. Let's try to print it

```bash
peekmem 100030
```

Nothing special, but we can visit the `0x00100030-0x00102000` range and see if there is anything interesting. At some point in the text section, we find the flag.

```bash
<观点view>peekmem 0100ff0
当前IP地址:10.0.0.10disabl3pic
!!! 警告: PIC锁定已关闭
<观点view> 控制台管理员模式已开启... 输入 'help' 获取帮助
☕️ 抱歉，这台机子只喝电，不喝咖啡。
[!] Memory dump:

0x00100ff0: C  � S � E � � U � � C 
                                    � S 
0x00101000: 0 x       B t S C T F { q 
0x00101010: e m u _ m p r i n t _ s 0 0 0 _ 
0x00101020: e a s s s s y _ i s n t _ i t } 
0x00101030:     > > = =   � � � � � � � 
0x00101040: � � � � � � � � � � �   H u e i 
0x00101050: - w e i   N e t w o r k S W E   
0x00101060: v 1 . 0 0   = = < < 
  > > = = 
0x00101070:   � � � � � � � � � � � � � � � 
0x00101080: � � � � � � � � � � � � � � � � 
0x00101090: � � � � � h e l p   = = < < 
  
0x001010a0: < � � � � � � v i e w >  [ ! ] 
0x001010b0:   M e m o r y   d u m p : 
  
 
0x001010c0:  :         I n v a l i d   
0x001010d0: c o m m a n d   f o r m a t .   
0x001010e0: U s e :   m p r i n t   < a d d 
```

The memory dump now shows us a flag

```bash
0x00101000: 0 x       B t S C T F { q 
0x00101010: e m u _ m p r i n t _ s 0 0 0 _ 
0x00101020: e a s s s s y _ i s n t _ i t } 
```

```plaintext
BtSCTF{qemu_mprint_s000_eassssy_isnt_it}
```