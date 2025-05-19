-----------------------------------------------------------------------------
-- Name:     USB HID dissector plugin
-- Author:   bberni
-- Modified:
-- Created:  2025-04-27
-----------------------------------------------------------------------------
-- based on https://github.com/hawkfeather/wireshark-usb_keyboard_dissector/


do

    local usb_mouse_protocol = Proto("usb_mouse", "USB mouse protocol")
    local button = ProtoField.uint8("usb_mouse.mouse_button", "MOUSE_BUTTON")
    local x = ProtoField.int8("usb_mouse.x", "X")
    local y = ProtoField.int8("usb_mouse.y", "Y")
    
    usb_mouse_protocol.fields = {
        button, x, y
    }

    local usb_keyboard_protocol = Proto("usb_keyboard",  "USB keyboard protocol")
    local key_shift = ProtoField.bool("usb_keyboard.key_shift", "SHIFT")
    local key_code = ProtoField.uint8("usb_keyboard.key_code", "KEY_CODE")
    local parsed_key_code = ProtoField.string("usb_keyboard.parsed_key_code", "PARSED_KEY_CODE")

    usb_keyboard_protocol.fields = {
        key_shift, key_code, parsed_key_code
    }

    local key_code_table = {
        [0x04] = "a",
        [0x05] = "b",
        [0x06] = "c",
        [0x07] = "d",
        [0x08] = "e",
        [0x09] = "f",
        [0x0A] = "g",
        [0x0B] = "h",
        [0x0C] = "i",
        [0x0D] = "j",
        [0x0E] = "k",
        [0x0F] = "l",
        [0x10] = "m",
        [0x11] = "n",
        [0x12] = "o",
        [0x13] = "p",
        [0x14] = "q",
        [0x15] = "r",
        [0x16] = "s",
        [0x17] = "t",
        [0x18] = "u",
        [0x19] = "v",
        [0x1A] = "w",
        [0x1B] = "x",
        [0x1C] = "y",
        [0x1D] = "z",
        [0x1E] = "1",
        [0x1F] = "2",
        [0x20] = "3",
        [0x21] = "4",
        [0x22] = "5",
        [0x23] = "6",
        [0x24] = "7",
        [0x25] = "8",
        [0x26] = "9",
        [0x27] = "0",
        [0x28] = "[ENTER]",
        [0x29] = "[ESC]",
        [0x2A] = "[BACKSPACE]",
        [0x2B] = "[TAB]",
        [0x2C] = "[SPACE]",
        [0x2D] = "-",
        [0x2E] = "=",
        [0x2F] = "[",
        [0x30] = "]",
        [0x31] = "\\",
        [0x33] = ";",
        [0x34] = "'",
        [0x36] = ",",
        [0x37] = ".",
        [0x38] = "/",
        [0x39] = "[CAPS LOCK]",
        [0x3A] = "F1",
        [0x3B] = "F2",
        [0x3C] = "F3",
        [0x3D] = "F4",
        [0x3E] = "F5",
        [0x3F] = "F6",
        [0x40] = "F7",
        [0x41] = "F8",
        [0x42] = "F9",
        [0x43] = "F10",
        [0x44] = "F11",
        [0x45] = "F12",
        [0x46] = "[PRINT SCREEN]",
        [0x47] = "[SCROLL LOCK]",
        [0x48] = "[PAUSE]",
        [0x49] = "[INSERT]",
        [0x4A] = "[HOME]",
        [0x4B] = "[PAGE UP]",
        [0x4C] = "[DELETE]",
        [0x4D] = "[END]",
        [0x4E] = "[PAGE DOWN]",
        [0x4F] = "[RIGHT ARROW]",
        [0x50] = "[LEFT ARROW]",
        [0x51] = "[DOWN ARROW]",
        [0x52] = "[UP ARROW]"
    }

    local shift_code_table = {
        [0x04] = "A",
        [0x05] = "B",
        [0x06] = "C",
        [0x07] = "D",
        [0x08] = "E",
        [0x09] = "F",
        [0x0A] = "G",
        [0x0B] = "H",
        [0x0C] = "I",
        [0x0D] = "J",
        [0x0E] = "K",
        [0x0F] = "L",
        [0x10] = "M",
        [0x11] = "N",
        [0x12] = "O",
        [0x13] = "P",
        [0x14] = "Q",
        [0x15] = "R",
        [0x16] = "S",
        [0x17] = "T",
        [0x18] = "U",
        [0x19] = "V",
        [0x1A] = "W",
        [0x1B] = "X",
        [0x1C] = "Y",
        [0x1D] = "Z",
        [0x1E] = "!",
        [0x1F] = "@",
        [0x20] = "#",
        [0x21] = "$",
        [0x22] = "%",
        [0x23] = "^",
        [0x24] = "&",
        [0x25] = "*",
        [0x26] = "(",
        [0x27] = ")",
        [0x28] = "[ENTER]",
        [0x29] = "[ESC]",
        [0x2A] = "[BACKSPACE]",
        [0x2B] = "[TAB]",
        [0x2C] = "[SPACE]",
        [0x2D] = "_",
        [0x2E] = "+",
        [0x2F] = "{",
        [0x30] = "}",
        [0x31] = "|",
        [0x33] = ":",
        [0x34] = "\"",
        [0x36] = "<",
        [0x37] = ">",
        [0x38] = "?",
        [0x39] = "[CAPS LOCK]",
        [0x3A] = "F1",
        [0x3B] = "F2",
        [0x3C] = "F3",
        [0x3D] = "F4",
        [0x3E] = "F5",
        [0x3F] = "F6",
        [0x40] = "F7",
        [0x41] = "F8",
        [0x42] = "F9",
        [0x43] = "F10",
        [0x44] = "F11",
        [0x45] = "F12",
        [0x46] = "[PRINT SCREEN]",
        [0x47] = "[SCROLL LOCK]",
        [0x48] = "[PAUSE]",
        [0x49] = "[INSERT]",
        [0x4A] = "[HOME]",
        [0x4B] = "[PAGE UP]",
        [0x4C] = "[DELETE]",
        [0x4D] = "[END]",
        [0x4E] = "[PAGE DOWN]",
        [0x4F] = "[RIGHT ARROW]",
        [0x50] = "[LEFT ARROW]",
        [0x51] = "[DOWN ARROW]",
        [0x52] = "[UP ARROW]"
    }

    function parse_key_code(pressed_shift, key_code_num)

        local key_table = key_code_table
        if pressed_shift then
            key_table = shift_code_table
        end

        if key_table[key_code_num] == nil then
            return "[UNKNOWN]"
        end

        return key_table[key_code_num]
    end

    function parse_mouse_button(num)
        local mapping = {
            [0x00] = "[NONE]",
            [0x01] = "[MOUSE1]",
            [0x02] = "[MOUSE2]",
            [0x03] = "[MOUSE3]",
        }

        if mapping[num] == nil then
            return "[UNKNOWN]"
        end

        return mapping[num]
    end

    function usb_mouse_protocol.dissector(tvb, pinfo, tree)
        local length = tvb:len()
        if length == 0 then return end
        local mouse_button = parse_mouse_button(tvb(0,1):le_int())
        local x_change = tvb(1,1):le_int()
        local y_change = tvb(2,1):le_int()

        pinfo.cols.protocol = usb_mouse_protocol.name

        local subtree = tree:add(usb_mouse_protocol, tvb(), "USB Mouse Data")
        subtree:add(button, tvb(0,1)):append_text(mouse_button)
        subtree:add(x, tvb(1,1))
        subtree:add(y, tvb(2,1))
    end

    function usb_keyboard_protocol.dissector(tvb, pinfo, tree)
        length = tvb:len()
        if length == 0 then return end

        local pressed_shift = tvb(1,1) == 2
        local key_code_num = tvb(3,1)
        pinfo.cols.protocol = usb_keyboard_protocol.name

        local subtree = tree:add(usb_keyboard_protocol, tvb(), "USB Keyboard Data")
        subtree:add(key_shift, pressed_shift)
        subtree:add(key_code, key_code_num)
        subtree:add(parsed_key_code, parse_key_code(pressed_shift, key_code_num:le_int()))
    end

    DissectorTable.get("usb.device"):add(0x9, usb_keyboard_protocol)
    DissectorTable.get("usb.device"):add(0x4, usb_mouse_protocol)


end