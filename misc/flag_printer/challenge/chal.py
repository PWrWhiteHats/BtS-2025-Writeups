#!/usr/bin/env python3
fLag="StBCTF{WROOOOONG}"
fLAg="tSBCTF{I_FORGOR_THE_FLAG_SORRY}"
Flag="SBtCTF{this_is_a_certified_fake_flag}"
FlAG="BStCTF{W0NG_FLAG_:3}"
flag="This CTF is organized by a Polish university, we decided to switch to Polish variable names, so we moved flag to flaga"
flaga="BtSCTF{Pyth0n_1D3nt1f1ers_ar3_W31rd}"

print("Available flags: fLag, fLAg, Flag, FlAG")
print("Unavailable flags: flag")
print("Which flag do you want to print?")
while True:
    user_choice=input("-> ")

    if (len(user_choice) != 4):
        print("input length needs to be 4")
        continue

    if user_choice == "flag":
        print("We are sorry, but this one is currently unavailable")
        continue

    try:
        exec(f"print({user_choice})")
    except Exception as e:
        print(e)
